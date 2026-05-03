# 📄 Resume Parser

An NLP-based resume parser built with **spaCy** and **Streamlit**.  
Extracts structured information from PDF/DOCX resumes.

---

## 🚀 Setup & Run

### 1. Clone / download the project
```
cd resume_parser
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Run the app
```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
resume_parser/
│
├── app.py                  # Streamlit UI
├── requirements.txt        # Dependencies
├── README.md
│
└── utils/
    ├── extractor.py        # PDF/DOCX text extraction
    └── parser.py           # NLP parsing logic (spaCy + regex)
```

---

## ✅ Features

| Feature | Method |
|---|---|
| Name extraction | spaCy NER (PERSON entity) |
| Email / Phone | Regex |
| LinkedIn / GitHub | Regex |
| Skills detection | Keyword matching (50+ skills) |
| Education | Section splitting + degree regex |
| Experience | Section splitting |
| Projects | Section splitting |
| JSON export | Download button in UI |

---

## 🧪 Test It

Use any resume PDF from:  
👉 https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
