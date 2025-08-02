# 📜 Grandma Letters Archive

A personal project to preserve, explore, and share the lifetime correspondence of my grandmother — over 300 handwritten letters exchanged with family and friends.  
The goal is to digitize, transcribe, and enrich these letters using AI, and eventually make them accessible via an interactive website or Streamlit app.

---

## 🎯 Project Goals

1. **Digitization**  
   - Sync scanned letters from Google Drive.
   - Organize them into a structured archive.

2. **Transcription (OCR)**  
   - Use GPT‑4o Vision to transcribe handwriting.
   - Store both:
     - **Raw transcription** — faithful to original.
     - **Clean transcription** — modernized for readability.

3. **Enrichment**  
   - Topic modeling to identify themes.
   - Named-entity recognition (NER) for people, places, events.
   - Sentiment & tone analysis over time.
   - Retrieval-Augmented Generation (RAG) for search/chat.

4. **Presentation**  
   - Explore in notebooks.
   - Build a public/private Streamlit web app to browse & search.

---

## 🗂 Project Structure

```
.
├── app/                 # Streamlit app (future)
├── notebooks/           # Data exploration, OCR evaluation, topic modeling
├── scripts/              # Automation scripts
│   ├── drive_sync.py     # Pull scans from Google Drive
│   └── gpt_ocr.py        # Run GPT OCR on images
├── data/                 # Small sample data for testing
├── archive/              # Large data (ignored by git)
│   ├── originals/        # Raw scans from Drive
│   └── ocr/              # OCR JSON outputs
├── requirements.txt
├── .env.example          # Example env variables
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.11+**
- **GitHub Codespaces** or local dev environment
- **Google Cloud Service Account** with Drive API access  
  - JSON key stored in `GDRIVE_SERVICE_ACCOUNT_JSON` secret
- **OpenAI API key** stored in `OPENAI_API_KEY` secret

### 2. Setup

Clone the repo and open it in a [GitHub Codespace](https://docs.github.com/en/codespaces).

**Install dependencies** (Codespaces will do this automatically if using `devcontainer.json`):
```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

These must be set as **GitHub Codespaces Secrets** or in a local `.env` file:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key for GPT-4o Vision |
| `GDRIVE_SERVICE_ACCOUNT_JSON` | Contents of your Google Drive Service Account JSON key |

---

## 📥 Sync Letters from Google Drive

```bash
python scripts/drive_sync.py --drive-folder "Letters/RawScans" --local-root "archive/originals"
```

---

## 📝 Run OCR

```bash
python scripts/gpt_ocr.py
```

Outputs JSON files like:

```json
{
  "raw": "Dear Mary,\nI hope this letter finds you well...",
  "clean": "Dear Mary, I hope you are doing well..."
}
```

---

## 📊 Next Steps

- **Pilot transcription** on ~20 letters.
- Evaluate raw vs clean text accuracy.
- Start topic modeling & enrichment.
- Prototype browsing/search in Streamlit.

---

## 🧾 License

Personal / Private use only until further decision.

---

## ❤️ Acknowledgements

- [OpenAI](https://openai.com) for GPT‑4o Vision.
- [PyDrive2](https://github.com/iterative/PyDrive2) for Drive access.
- Inspiration: preserving family history through technology.
