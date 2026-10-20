import os
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
    api_key=config.DEEPSEEK_API_KEY,
    base_url=config.DEEPSEEK_BASE_URL
)
# =========================
# STRICT OCR PROMPT
# =========================
PROMPT = (
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
# OCR (TEXT-ONLY BASE64)
# =========================
def deepseek_ocr(image_path):
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    message = PROMPT + "\nIMAGE:\n" + b64

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": message}]
    )

    text = response.choices[0].message.content.strip()
    text = text.replace("\n", " ").strip()

    # # ---- STRICT FILTER (VERY IMPORTANT) ----
    # bad_phrases = [
    #     "quick brown fox",
    #     "not a robot",
    #     "cannot assist",
    #     "image contains",
    #     "visible in the image"
    # ]
    # if any(p in text.lower() for p in bad_phrases):
    #     text = ""

    # # If mostly English, drop it
    # english_chars = sum(c.isascii() and c.isalpha() for c in text)
    # if len(text) > 0 and english_chars / len(text) > 0.3:
    #     text = ""

    # # Length sanity check
    # if len(text) < 5:
    #     text = ""

    return text

# =========================
# FILE HANDLES (UTF-8 SAFE)
# =========================
log_file = open("kpti_log.txt", "a", encoding="utf-8")
visit_file = open("kpti_visited_test_images.txt", "a+", encoding="utf-8")

visit_file.seek(0)
visited = set(l.strip() for l in visit_file.readlines())

# =========================
# DATASET (0–3)
# =========================
gt_files = sorted(glob.glob("KPTI-TestData/*.txt"))[:100]

# =========================
# MAIN LOOP (NO PRINT OCR)
# =========================
for gt_path in gt_files:

    if gt_path in visited:
        continue

    with open(gt_path, "r", encoding="utf-8") as f:
        reference = f.readline().strip()

    img_path = gt_path.replace(".txt", ".jpg")

    try:
        prediction = deepseek_ocr(img_path)

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

        # ONLY filename printed (safe)
        print(gt_path)

        time.sleep(1)

    except Exception as e:
        print("Error:", e)

# =========================
# CLOSE
# =========================
log_file.close()
visit_file.close()

print("DeepSeek OCR Experiment Completed.")
