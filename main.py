from __future__ import annotations

import argparse
from pathlib import Path

from job_application_agent.agent import JobApplicationAgent
from job_application_agent.io_utils import ensure_output_dir, read_text_file, write_text_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple Job Application Agent")
    parser.add_argument("--job", required=True, help="Path to the job description text file")
    parser.add_argument("--resume", required=True, help="Path to the resume text file")
    parser.add_argument("--language", choices=["de", "en"], default="de", help="Output language")
    parser.add_argument("--candidate-name", default="Your Name", help="Candidate name")
    parser.add_argument("--company-name", default="Target Company", help="Target company name")
    parser.add_argument("--role-title", default="Target Role", help="Role title")
    parser.add_argument("--output-dir", default="outputs", help="Directory for generated files")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    job_text = read_text_file(Path(args.job))
    resume_text = read_text_file(Path(args.resume))

    output_dir = Path(args.output_dir)
    ensure_output_dir(output_dir)

    agent = JobApplicationAgent(language=args.language)
    result = agent.run(
        job_description=job_text,
        resume_text=resume_text,
        candidate_name=args.candidate_name,
        company_name=args.company_name,
        role_title=args.role_title,
    )

    write_text_file(output_dir / "analysis_report.md", result.analysis_report)
    write_text_file(output_dir / "tailored_bullets.md", result.tailored_bullets)
    write_text_file(output_dir / "cover_letter.md", result.cover_letter)

    print("\nDone. Files generated:")
    print(f"- {output_dir / 'analysis_report.md'}")
    print(f"- {output_dir / 'tailored_bullets.md'}")
    print(f"- {output_dir / 'cover_letter.md'}")


if __name__ == "__main__":
    main()
