from __future__ import annotations

import re
from collections import Counter

SKILL_KEYWORDS = {
    "python",
    "java",
    "c++",
    "c",
    "docker",
    "kubernetes",
    "linux",
    "git",
    "gitlab",
    "github",
    "aws",
    "azure",
    "gcp",
    "sql",
    "postgresql",
    "rest",
    "api",
    "fastapi",
    "flask",
    "django",
    "javascript",
    "typescript",
    "html",
    "css",
    "jira",
    "testing",
    "pytest",
    "automation",
    "llm",
    "chatgpt",
    "prompting",
    "data structures",
    "algorithms",
    "oop",
    "sap",
    "abap",
    "cap",
    "ui5",
    "networking",
    "devops",
    "ci/cd",
    "cloud",
}

STOPWORDS = {
    "and", "the", "for", "with", "you", "your", "are", "will", "our", "from", "that",
    "eine", "einer", "einem", "und", "der", "die", "das", "mit", "für", "von", "du", "dein",
    "deine", "ein", "in", "zu", "oder", "im", "auf", "den", "des", "ist", "als", "bei",
}


def normalize_text(text: str) -> str:
    return text.lower().strip()


def extract_skills(text: str) -> list[str]:
    lowered = normalize_text(text)
    found = []
    for skill in sorted(SKILL_KEYWORDS):
        pattern = re.escape(skill)
        if re.search(rf"\b{pattern}\b", lowered):
            found.append(skill)
    return found


def extract_keywords(text: str, max_items: int = 15) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z+/#.-]{2,}", text.lower())
    filtered = [w for w in words if w not in STOPWORDS and len(w) > 2]
    counts = Counter(filtered)
    ranked = [word for word, _count in counts.most_common(max_items)]
    return ranked


def compare_resume_to_job(job_text: str, resume_text: str) -> tuple[list[str], list[str]]:
    job_skills = set(extract_skills(job_text))
    resume_skills = set(extract_skills(resume_text))
    matched = sorted(job_skills & resume_skills)
    missing = sorted(job_skills - resume_skills)
    return matched, missing


def compute_match_score(matched_skills: list[str], missing_skills: list[str]) -> int:
    total = len(matched_skills) + len(missing_skills)
    if total == 0:
        return 50
    score = round(len(matched_skills) / total * 100)
    return max(0, min(score, 100))


def summarize_match(score: int, language: str) -> str:
    if language == "de":
        if score >= 75:
            return "Dein Profil passt bereits gut zur Stelle. Die Bewerbung sollte die vorhandenen Stärken klar hervorheben."
        if score >= 50:
            return "Dein Profil passt teilweise gut. Eine gezielte Anpassung der Formulierungen und Schlüsselwörter kann die Bewerbung deutlich verbessern."
        return "Es gibt einige passende Elemente, aber auch erkennbare Lücken. Der Fokus sollte auf übertragbaren Fähigkeiten und einer guten Positionierung liegen."

    if score >= 75:
        return "Your profile already matches the role quite well. The application should emphasize your existing strengths clearly."
    if score >= 50:
        return "Your profile is a partial match. Targeted wording and stronger keyword alignment can improve the application significantly."
    return "There are some relevant elements, but also visible gaps. The application should focus on transferable skills and clear positioning."
