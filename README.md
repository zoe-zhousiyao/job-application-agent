# Job Application Agent

## 🚀 Project Overview

This project is a simple Agentic AI system that automates job application tasks:

- Extract skills from job descriptions
- Match them with candidate resumes
- Generate tailored resume improvements
- Generate cover letters automatically

## 🧠 Agentic Workflow

Input → Analysis → Matching → Generation

A simple **Agentic AI** project for tailoring job applications.

This project takes a **job description** and a **resume**, then runs a multi-step workflow to:

1. extract important skills from the job description
2. analyze how well the resume matches
3. identify missing skills / keywords
4. generate tailored resume bullet suggestions
5. generate a draft cover letter (`Anschreiben` or English cover letter)

It works in two modes:

- **rule-based mode** (default, no API key required)
- **LLM mode** (optional, if you later want to connect an OpenAI-compatible API)

## Why this counts as Agentic AI

This is not a normal chatbot. It performs a **task chain**:

**read input -> extract -> analyze -> decide -> generate outputs**

That is a simple agent workflow.

## Project structure

```bash
job-application-agent/
├── README.md
├── requirements.txt
├── main.py
├── .env.example
├── examples/
│   ├── sample_job_description.txt
│   └── sample_resume.txt
├── outputs/
└── job_application_agent/
    ├── __init__.py
    ├── agent.py
    ├── models.py
    ├── io_utils.py
    ├── rules.py
    └── llm.py
```

## Quick start

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run in rule-based mode

```bash
python main.py \
  --job examples/sample_job_description.txt \
  --resume examples/sample_resume.txt \
  --language de
```

### 4. Check outputs

The program writes files into `outputs/`:

- `analysis_report.md`
- `tailored_bullets.md`
- `cover_letter.md`

## Optional arguments

```bash
python main.py \
  --job examples/sample_job_description.txt \
  --resume examples/sample_resume.txt \
  --language en \
  --candidate-name "Siyao Zhou" \
  --company-name "Example GmbH" \
  --role-title "Working Student AI Automation"
```

## Optional LLM mode

This repository includes a placeholder module for later extension. The current default project is intentionally simple and beginner-friendly.

When you are ready, you can extend `job_application_agent/llm.py` to call an OpenAI-compatible API.

## Good GitHub description

> A simple agentic AI project in Python that analyzes a job description, compares it with a resume, identifies missing keywords, and generates tailored resume bullets and a draft cover letter.

## Ideas for next upgrades

- add PDF/DOCX parsing
- add URL scraping for job descriptions
- add Streamlit web UI
- add OpenAI API support
- add scoring with embeddings
- add multilingual output

