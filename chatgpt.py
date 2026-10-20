import base64
import glob
import time
import jiwer
from openai import OpenAI

# =========================
# API CONFIG
# =========================
import config

client = OpenAI(
    api_key=config.OPENAI_API_KEY,
    base_url=config.OPENAI_BASE_URL
)  

# =========================
# OCR PROMPT (STRICT)
# =========================
OCR_PROMPT = (
    "Extract ONLY the exact text visible in the image.\n"
    "Return ONE plain text line.\n"
    "Do NOT explain.\n"
    "Do NOT add headings or lists."
)

# =========================
# METRICS
# =========================
def wer_cer(ref, hyp):
    return jiwer.wer(ref, hyp), jiwer.cer(ref, hyp)

# =========================
# tu
# CHATGPT OCR (VISION)
# =========================
def chatgpt_ocr(image_path):
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    response = client.responses.create(
        model="gpt-5.2",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": OCR_PROMPT},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{b64}"
                }
            ]
        }]
    )

    text = response.output_text.strip()
    text = text.replace("\n", " ").strip()
    return text

# =========================
# FILE HANDLES
# =========================
log_file = open("kpti_log_chatgpt.txt", "a", encoding="utf-8")
visit_file = open("kpti_visited_test_images_chatgpt.txt", "a+", encoding="utf-8")

visit_file.seek(0)
visited = set(l.strip() for l in visit_file.readlines())

# =========================
# DATASET
# =========================
gt_files = sorted(glob.glob("KPTI-TestData/*.txt"))
TOTAL_IMAGES = len(gt_files)
# =========================
# MAIN LOOP
# =========================
for gt_path in gt_files:

    if gt_path in visited:
        continue

    with open(gt_path, "r", encoding="utf-8") as f:
        reference = f.readline().strip()

    img_path = gt_path.replace(".txt", ".jpg")

    try:
        prediction = chatgpt_ocr(img_path)
        wer, cer = wer_cer(reference, prediction)

        log_entry = (
            f"{gt_path}\t"
            f"{reference}\t"
            f"{prediction}\t"
            f"{wer:.4f}\t"
            f"{cer:.4f}\n"
        )

        log_file.write(log_entry)
        visit_file.write(gt_path + "\n")

        print(gt_path)
        time.sleep(1)

    except Exception as e:
        print("Error:", e)

# =========================
# CLOSE
# =========================
log_file.close()
visit_file.close()

print("ChatGPT OCR Experiment Completed.")
