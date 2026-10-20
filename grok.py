import base64
import glob
import time
import os
from PIL import Image
import jiwer
from openai import OpenAI

# =============================
# API CONFIGURATION
# =============================
# Note: Always keep your API keys private!
import config

client = OpenAI(
    api_key=config.XAI_API_KEY,
    base_url=config.XAI_BASE_URL
)
# =============================
# OCR PROMPT
# =============================
OCR_PROMPT = (
    "Extract ONLY the exact text visible in the image. "
    "Return ONE plain text line. Do NOT explain. "
    "Do NOT add headings or lists."
)

# =============================
# METRICS FUNCTION
# =============================
def wer_cer(ref, hyp):
    # Handle empty hypothesis to avoid errors
    if not hyp:
        return 1.0, 1.0
    wer = jiwer.wer(ref, hyp)
    cer = jiwer.cer(ref, hyp)
    return wer, cer

# =============================
# GROK OCR FUNCTION (FIXED)
# =============================
def grok_ocr(image_path):
    # 1. Properly encode image to base64
    with open(image_path, "rb") as f:
        b64_image = base64.b64encode(f.read()).decode("utf-8")

    # 2. Use the Multi-modal message format
    # Using 'grok-4' which is vision-capable
    response = client.chat.completions.create(
        model="grok-2-vision-1212",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": OCR_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}",
                            "detail": "high"  # Ensures best OCR accuracy
                        },
                    },
                ],
            }
        ],
        max_tokens=150
    )

    extracted = response.choices[0].message.content.strip()
    # Clean up any accidental newlines for the log file
    return extracted.replace("\n", " ").strip()

# =============================
# MAIN EXPERIMENT LOOP
# =============================
log_file_path = "kpti_log_grok.txt"
visit_file_path = "kpti_visited_test_images_grok.txt"

# Open files with encoding for Urdu/Special characters
log_file = open(log_file_path, "a", encoding="utf-8")
visit_file = open(visit_file_path, "a+", encoding="utf-8")

visit_file.seek(0)
visited = set(line.strip() for line in visit_file.readlines())

# Get all ground truth text files
gt_files = sorted(glob.glob("KPTI-TestData/*.txt"))
TOTAL_IMAGES = len(gt_files)

print("Starting Grok OCR Experiment...")

for gt_path in gt_files[:TOTAL_IMAGES]:
    if gt_path in visited:
        continue

    # Read the reference text
    with open(gt_path, "r", encoding="utf-8") as f:
        reference = f.readline().strip()

    # Determine image path
    img_path = gt_path.replace(".txt", ".jpg")
    
    # Check if image actually exists
    if not os.path.exists(img_path):
        print(f"Skipping: Image not found for {gt_path}")
        continue

    try:
        print(f"Processing: {img_path}")
        
        # Get prediction from Grok
        prediction = grok_ocr(img_path)
        
        # Calculate Error Rates
        wer, cer = wer_cer(reference, prediction)

        # Write to log (Tab separated)
        log_entry = f"{gt_path}\t{reference}\t{prediction}\t{wer:.4f}\t{cer:.4f}\n"
        log_file.write(log_entry)
        log_file.flush() # Ensure it writes immediately
        
        # Mark as visited
        visit_file.write(gt_path + "\n")
        visit_file.flush()

        print(f"  -> WER: {wer:.4f}, CER: {cer:.4f}")
        
        # Small delay to respect rate limits
        time.sleep(1)

    except Exception as e:
        print(f"Error processing {gt_path}: {e}")
        # Optional: Break if it's an Authentication/Balance error
        if "401" in str(e) or "insufficient_quota" in str(e):
            break

log_file.close()
visit_file.close()
print("\nGrok OCR experiment completed successfully.")