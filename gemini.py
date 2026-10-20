import google.generativeai as genai
from PIL import Image
import jiwer
import glob

def wer_cer(reference, hypothesis):
  # Calculate WER
  wer = jiwer.wer(reference, hypothesis)
  print(f"Word Error Rate (WER): {wer:.4f}")
  # Calculate CER
  cer = jiwer.cer(reference, hypothesis)
  print(f"Character Error Rate (CER): {cer:.4f}")

  return wer, cer

def ocr_modul(prompt, image, model):
  # Generate content (perform OCR)
  response = model.generate_content([prompt, image])
  return response



cer_list =[]
wer_list =[]
total_wr =[]
total_ch =[]

visit_file = open('kpti_visited_test_images.txt', 'a+')
log_file = open('kpti_log.txt', 'a+', encoding='utf-8')
#testFiles=open('testSetKPTI.txt','r',encoding=='utf-8')


visit_file.seek(0)
visit_images = visit_file.readlines()
# Configure your API key
#genai.configure(api_key="YOUR_API_KEY")
import config

genai.configure(api_key=config.GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash') 

# Define the prompt for OCR
prompt = (
    "Extract ONLY the exact text visible in the image. "
    "Return ONE plain text line. Do NOT explain. "
    "Do NOT add headings or lists."
)
img_files = glob.glob('KPTI-TestData/*.txt')
TOTAL_IMAGES = len(img_files)
for i in range(TOTAL_IMAGES):
  if img_files[i]+'\n'  not in visit_images:
    gt_path = img_files[i]
    print(gt_path)
    #print(gt_path)
    gt = open(gt_path, 'r',encoding='utf-8')
    print(gt)
    reference = gt.readline().strip()

    img_path= gt_path.replace('.txt', '.jpg')

    # Load the image
    image = Image.open(img_path)

    try:
      response = ocr_modul(prompt, image, model)

      wer, cer = wer_cer(reference, response.text)
      wer_list.append(wer)
      cer_list.append(cer)
      #total_ch.append(len(reference))
      #total_wr.append(len(reference.split()))

      log_entry = img_files[i] +'\t'+reference+"\t" + response.text+"\t"
      log_file.write(log_entry)
      #log_file.write(img_files[i]+'\n')
      log_file.write("{}".format(wer) +"\t")
      log_file.write("{}".format(cer)+"\n")
      visit_file.write(img_files[i])
      visit_file.write("\n")
    except:
      log_file.close()
      visit_file.close()

#print('CER', sum(cer_list)/len(cer_list))
#print('WER', sum(wer_list)/len(wer_list))
print("The experiment is completed...")
log_file.close()
visit_file.close()