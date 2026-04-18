from __future__ import annotations

from textwrap import dedent

from job_application_agent.models import AgentOutput, JobAnalysis
from job_application_agent.rules import (
    compare_resume_to_job,
    compute_match_score,
    extract_keywords,
    extract_skills,
    summarize_match,
)


class JobApplicationAgent:
    def __init__(self, language: str = "de") -> None:
        self.language = language

    def run(
        self,
        job_description: str,
        resume_text: str,
        candidate_name: str,
        company_name: str,
        role_title: str,
    ) -> AgentOutput:
        analysis = self._analyze(job_description, resume_text)
        report = self._build_analysis_report(analysis)
        bullets = self._build_tailored_bullets(analysis, resume_text)
        cover_letter = self._build_cover_letter(analysis, candidate_name, company_name, role_title)
        return AgentOutput(
            analysis_report=report,
            tailored_bullets=bullets,
            cover_letter=cover_letter,
        )

    def _analyze(self, job_description: str, resume_text: str) -> JobAnalysis:
        extracted_skills = extract_skills(job_description)
        extracted_keywords = extract_keywords(job_description)
        matched_skills, missing_skills = compare_resume_to_job(job_description, resume_text)
        score = compute_match_score(matched_skills, missing_skills)
        summary = summarize_match(score, self.language)
        return JobAnalysis(
            extracted_skills=extracted_skills,
            extracted_keywords=extracted_keywords,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            match_score=score,
            summary=summary,
        )

    def _build_analysis_report(self, analysis: JobAnalysis) -> str:
        if self.language == "de":
            return dedent(
                f"""
                # Analysebericht

                ## Match Score
                **{analysis.match_score}/100**

                ## Kurzfazit
                {analysis.summary}

                ## Erkannte Skills in der Stellenanzeige
                {self._markdown_list(analysis.extracted_skills)}

                ## Häufige Keywords in der Stellenanzeige
                {self._markdown_list(analysis.extracted_keywords)}

                ## Bereits passende Skills im Lebenslauf
                {self._markdown_list(analysis.matched_skills)}

                ## Fehlende oder nicht klar sichtbare Skills
                {self._markdown_list(analysis.missing_skills)}
                """
            ).strip()

        return dedent(
            f"""
            # Analysis Report

            ## Match Score
            **{analysis.match_score}/100**

            ## Summary
            {analysis.summary}

            ## Skills detected in the job description
            {self._markdown_list(analysis.extracted_skills)}

            ## Frequent keywords in the job description
            {self._markdown_list(analysis.extracted_keywords)}

            ## Skills already visible in the resume
            {self._markdown_list(analysis.matched_skills)}

            ## Missing or weakly visible skills
            {self._markdown_list(analysis.missing_skills)}
            """
        ).strip()

    def _build_tailored_bullets(self, analysis: JobAnalysis, resume_text: str) -> str:
        visible_strengths = analysis.matched_skills[:5]
        if self.language == "de":
            lines = ["# Vorschläge für angepasste Lebenslauf-Bullets", ""]
            lines.append("## Formulierungen, die du für deinen Lebenslauf anpassen kannst")
            lines.append("")
            lines.append(
                f"- Entwickelte praxisnahe Lösungen mit Schwerpunkt auf {', '.join(visible_strengths) if visible_strengths else 'Softwareentwicklung und strukturierter Problemlösung'}."
            )
            lines.append(
                "- Analysierte technische Anforderungen, strukturierte komplexe Aufgaben und setzte Lösungen eigenständig um."
            )
            lines.append(
                "- Arbeitete mit APIs, Entwicklungswerkzeugen und automatisierten Workflows zur effizienten Umsetzung technischer Aufgaben."
            )
            lines.append(
                "- Nutzte Python zur Automatisierung, Datenverarbeitung und Unterstützung technischer Entwicklungsprozesse."
            )
            if analysis.missing_skills:
                lines.append("")
                lines.append("## Keywords, die du – falls ehrlich belegbar – stärker sichtbar machen solltest")
                lines.append("")
                for skill in analysis.missing_skills[:8]:
                    lines.append(f"- {skill}")
            return "\n".join(lines)

        lines = ["# Tailored Resume Bullet Suggestions", ""]
        lines.append("## Suggested bullet points")
        lines.append("")
        lines.append(
            f"- Built practical solutions with a focus on {', '.join(visible_strengths) if visible_strengths else 'software engineering and structured problem solving'}."
        )
        lines.append(
            "- Analyzed technical requirements, structured complex tasks, and implemented solutions independently."
        )
        lines.append(
            "- Worked with APIs, development tools, and automated workflows to deliver technical solutions efficiently."
        )
        lines.append(
            "- Used Python for automation, data processing, and support of engineering workflows."
        )
        if analysis.missing_skills:
            lines.append("")
            lines.append("## Keywords to emphasize more clearly if you can support them honestly")
            lines.append("")
            for skill in analysis.missing_skills[:8]:
                lines.append(f"- {skill}")
        return "\n".join(lines)

    def _build_cover_letter(
        self,
        analysis: JobAnalysis,
        candidate_name: str,
        company_name: str,
        role_title: str,
    ) -> str:
        strengths = ", ".join(analysis.matched_skills[:5]) if analysis.matched_skills else "Python, strukturierte Arbeitsweise und schnelle Lernfähigkeit"

        if self.language == "de":
            return dedent(
                f"""
                # Anschreiben-Entwurf

                Sehr geehrtes Team von {company_name},

                hiermit bewerbe ich mich für die Position **{role_title}**. Besonders interessant an dieser Stelle finde ich die Verbindung von technischer Umsetzung, strukturiertem Arbeiten und modernen digitalen Werkzeugen.

                Ich bringe bereits relevante Kenntnisse mit, insbesondere in den Bereichen {strengths}. Darüber hinaus arbeite ich mich schnell in neue Themen ein und gehe Aufgaben analytisch, zuverlässig und eigenständig an.

                An der Position reizt mich besonders, dass ich meine technischen Fähigkeiten gezielt einsetzen und gleichzeitig weiter ausbauen kann. Ich arbeite gerne strukturiert, interessiere mich für praxisnahe Lösungen und möchte ein Team aktiv unterstützen.

                Über die Möglichkeit, mich persönlich vorzustellen, freue ich mich sehr.

                Mit freundlichen Grüßen  
                {candidate_name}
                """
            ).strip()

        return dedent(
            f"""
            # Cover Letter Draft

            Dear {company_name} Team,

            I am writing to apply for the position **{role_title}**. What particularly interests me about this role is the combination of technical implementation, structured problem solving, and the use of modern digital tools.

            I already bring relevant strengths, especially in {strengths}. In addition, I learn new topics quickly and approach tasks in an analytical, reliable, and independent way.

            I am especially motivated by the opportunity to apply my technical skills in a practical setting while continuing to grow. I enjoy working in a structured way, building useful solutions, and contributing actively to a team.

            I would be very happy for the opportunity to introduce myself in a personal interview.

            Sincerely,  
            {candidate_name}
            """
        ).strip()

    @staticmethod
    def _markdown_list(items: list[str]) -> str:
        if not items:
            return "- None"
        return "\n".join(f"- {item}" for item in items)
