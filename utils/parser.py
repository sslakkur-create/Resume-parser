import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
SECTION_HEADERS = {
    "education":   r"(education|academic|qualification)",
    "experience":  r"(experience|work history|employment|career)",
    "skills":      r"(skills|technical skills|competencies|technologies)",
    "projects":    r"(projects|personal projects|academic projects)",
    "certifications": r"(certifications?|courses?|licenses?)",
}

SKILLS_DB = [
    "python", "java", "c++", "c#", "javascript", "typescript", "html", "css",
    "react", "angular", "vue", "node", "django", "flask", "fastapi", "spring",
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "git", "docker", "kubernetes", "aws", "gcp", "azure", "linux",
    "rest api", "graphql", "ci/cd", "agile", "scrum",
    "tableau", "power bi", "excel", "r", "matlab",
]

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else ""

def extract_phone(text):
    match = re.search(r"(\+?\d{1,3}[\s\-]?)?(\(?\d{3}\)?[\s\-]?)(\d{3}[\s\-]?\d{4})", text)
    return match.group(0).strip() if match else ""

def extract_linkedin(text):
    match = re.search(r"(linkedin\.com/in/[A-Za-z0-9\-_]+)", text)
    return match.group(0) if match else ""

def extract_github(text):
    match = re.search(r"(github\.com/[A-Za-z0-9\-_]+)", text)
    return match.group(0) if match else ""

def extract_name(text):
    doc = nlp(text[:300])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    for line in text.splitlines():
        line = line.strip()
        if line and not re.search(r"@|http|www|resume|cv", line, re.I):
            return line
    return ""

def extract_skills(text):
    lower = text.lower()
    found = [skill for skill in SKILLS_DB if skill in lower]
    return sorted(set(found))

def split_sections(text):
    lines = text.splitlines()
    sections = {k: [] for k in SECTION_HEADERS}
    sections["other"] = []
    current = "other"
    for line in lines:
        lower = line.lower().strip()
        matched = False
        for section, pattern in SECTION_HEADERS.items():
            if re.search(pattern, lower) and len(lower) < 40:
                current = section
                matched = True
                break
        if not matched:
            sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}

def extract_education(section_text):
    results = []
    degree_pattern = re.compile(
        r"(b\.?tech|m\.?tech|b\.?e|m\.?e|b\.?sc|m\.?sc|mba|phd|bachelor|master|doctor)", re.I)
    for line in section_text.splitlines():
        if degree_pattern.search(line) or len(line.strip()) > 10:
            cleaned = line.strip()
            if cleaned:
                results.append(cleaned)
    return results[:6]

def extract_experience(section_text):
    results = []
    for line in section_text.splitlines():
        cleaned = line.strip()
        if cleaned and len(cleaned) > 5:
            results.append(cleaned)
    return results[:10]

def parse_resume(text):
    sections = split_sections(text)
    return {
        "name":           extract_name(text),
        "email":          extract_email(text),
        "phone":          extract_phone(text),
        "linkedin":       extract_linkedin(text),
        "github":         extract_github(text),
        "skills":         extract_skills(text),
        "education":      extract_education(sections.get("education", "")),
        "experience":     extract_experience(sections.get("experience", "")),
        "certifications": sections.get("certifications", "").strip(),
        "projects":       sections.get("projects", "").strip(),
    }
