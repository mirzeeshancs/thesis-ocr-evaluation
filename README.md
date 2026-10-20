# Performance Evaluation of State-of-the-Art Large Multimodal Models Using the Katib’s Pashto Text Imagebase
**Code Author:** Zeeshan Rahman (31301)  
**Supervisor:** Dr. Riaz Ahmad, Assistant Professor  
**Department:** Computer Sciences, Shaheed Benazir Bhutto University, Sheringal

---

## About This Project

This repository contains the code and results for a final-year thesis project evaluating how well four modern Large Multimodal Models (LMMs) recognize handwritten Pashto text without task-specific training (zero-shot evaluation).

To the best of our knowledge, this is the first systematic zero-shot evaluation of LMMs on real handwritten Pashto data.

The four models evaluated in this study are Gemini, ChatGPT, Grok, and DeepSeek. The study uses the KPTI dataset (Katib's Pashto Text Imagebase), which contains 17,015 handwritten Pashto text-line images from historical books. The official test split of 2,553 images was used for the evaluation.

---

## Repository Structure

```text
thesis-ocr-evaluation/
├── scripts/
│   ├── chatgpt.py
│   ├── gemini.py
│   ├── grok.py
│   ├── deepseek.py
│   ├── findCERWER.py
│   └── config.example.py
├── data/
│   ├── testSetKPTI.txt
│   ├── trainSetKPTI.txt
│   └── validSetKPTI.txt
├── prompts/
│   └── ocr_prompt.txt
├── results/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Models Evaluated

| Model | Version | Provider |
|---|---|---|
| Gemini | `gemini-2.0-flash` | Google |
| ChatGPT | `gpt-5.2` | OpenAI |
| Grok | `grok-2-vision-1212` | xAI |
| DeepSeek | `deepseek-chat` | DeepSeek AI |

These are the model identifiers documented for this study. Their availability may vary by provider.

---

## About the KPTI Dataset

The KPTI (Katib's Pashto Text Imagebase) dataset was introduced in 2016 and contains handwritten text lines from six historical Pashto books written by traditional calligraphers.

**Official sources:**

- [KPTI dataset on GitHub](https://github.com/rahmad77/KPTI)
- [Original KPTI research paper](https://ieeexplore.ieee.org/document/7814106/)

**Important:** The dataset's image files are not included in this repository. The test-set filenames are provided in `data/testSetKPTI.txt`.

Download the dataset from its official source and place the test images in `data/KPTI-TestData/`. Each `.txt` ground-truth file must have a corresponding `.jpg` image with the matching filename, as expected by the scripts.

Please consult the official dataset documentation for its terms of use and citation requirements.

---

## Setup Instructions

Follow these steps to set up the project.

### 1. Clone the Repository

```bash
git clone https://github.com/mirzeeshancs/thesis-ocr-evaluation.git
cd thesis-ocr-evaluation
```

### 2. Install the Dependencies

Python 3.10 or later is recommended, subject to compatibility with the dependencies used by the scripts.

Create and activate a virtual environment.

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux or macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Each model requires access to its corresponding provider's API. API keys are not included in this repository.

1. Copy `scripts/config.example.py` to `scripts/config.py`.
2. Open `scripts/config.py`.
3. Add your own API keys using the variable names expected by the scripts.

The required configuration variables are:

- `GEMINI_API_KEY` — Google AI Studio
- `OPENAI_API_KEY` — OpenAI Platform
- `XAI_API_KEY` — xAI Console
- `DEEPSEEK_API_KEY` — DeepSeek Platform

The file `scripts/config.py` should be excluded through `.gitignore`. Never commit API keys or other secret credentials to GitHub.

API access, model availability, rate limits, and usage charges depend on the respective providers.

### 4. Download and Prepare the KPTI Dataset

Download the dataset from the official KPTI GitHub repository:

https://github.com/rahmad77/KPTI

Place the test images and corresponding `.txt` ground-truth files in the directory structure expected by the scripts. Ensure that filenames match correctly.

The test split is listed in `data/testSetKPTI.txt`.

---

## How to Run the Experiments

After configuring the API keys and preparing the dataset, run the desired model script from the repository's root directory.

**ChatGPT:**

```bash
python scripts/chatgpt.py
```

**Gemini:**

```bash
python scripts/gemini.py
```

**Grok:**

```bash
python scripts/grok.py
```

**DeepSeek:**

```bash
python scripts/deepseek.py
```

Each script saves its experiment log to the `results/` directory.

The output filenames are:

| Model | Output File |
|---|---|
| ChatGPT | `results/kpti_log_chatgpt.txt` |
| Gemini | `results/kpti_log_gemini.txt` |
| Grok | `results/kpti_log_grok.txt` |
| DeepSeek | `results/kpti_log_deepseek.txt` |

The log format is tab-separated and contains the following fields:

```text
image_path    ground_truth    prediction    WER    CER
```

### Calculate CER and WER

To calculate the mean Character Error Rate (CER) and Word Error Rate (WER) from the experiment logs, run:

```bash
python scripts/findCERWER.py
```

The mean is calculated by averaging the per-image CER and WER values. The reported sample counts are 2,553 images for ChatGPT, Gemini, and Grok, and 100 images for DeepSeek.

---

## Results Summary

The following results were obtained in the reported experiments.

| Model | Images | Mean CER (%) | Mean WER (%) |
|---|---:|---:|---:|
| ChatGPT (`gpt-5.2`) | 2,553 | 48.6 | 89.8 |
| Gemini (`gemini-2.0-flash`) | 2,553 | 49.2 | 81.5 |
| Grok (`grok-2-vision-1212`) | 2,553 | 99.2 | 121.6 |
| DeepSeek (`deepseek-chat`) | 100 | Failed | Failed |

### Interpretation of Results

- ChatGPT achieved the lowest CER (48.6%), indicating the lowest character-level error rate among the evaluated models.
- Gemini achieved the lowest WER (81.5%), indicating the lowest word-level error rate.
- Grok achieved a CER of 99.2%, indicating extremely poor character-level recognition performance.
- DeepSeek produced outputs containing random symbols, English text, and meaningless strings instead of valid Pashto transcriptions. Testing was stopped after 100 images with supervisor approval because the failure persisted during the initial evaluation.

None of the evaluated models achieved an accuracy level suitable for reliable real-world handwritten Pashto OCR applications under the experimental conditions used in this study.

---

## The Prompt Used

Every model received the same OCR instruction, stored in `prompts/ocr_prompt.txt`:

```text
Extract ONLY the exact text visible in the image. Return ONE plain text line. Do NOT explain. Do NOT add headings or lists.
```

The prompt instructs each model to return only the visible text without explanations or additional formatting. This helps maintain a consistent transcription task across models.

---

## Reproducibility

Chapter 5 of the thesis documents the experimental methodology and technical decisions. This repository provides the implementation and supporting files used in the study.

Reproducing the reported results may depend on access to the same model versions, API behavior, dataset split, prompts, dependencies, and evaluation procedure. Hosted models and APIs may change over time.

For questions about the research, please refer to the thesis or contact the Department of Computer Sciences at Shaheed Benazir Bhutto University, Sheringal.

---

## License

This repository is shared for academic and research purposes. No formal open-source license is specified here. Please contact the author regarding reuse and redistribution permissions.