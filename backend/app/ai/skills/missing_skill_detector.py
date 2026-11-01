from typing import List, Optional

# Recommended skills per resume category, using canonical catalog names.
CATEGORY_RECOMMENDED_SKILLS = {
    "Software Engineering": ["Python", "Java", "JavaScript", "React.js", "Node.js", "SQL", "Docker", "AWS", "Git", "TypeScript", "Spring Boot", "Django", "Flask", "Kubernetes", "Microservices", "GraphQL"],
    "Data Science": ["Python", "SQL", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "R", "Tableau", "Matplotlib", "Machine Learning", "Seaborn", "Plotly"],
    "Data Engineering": ["Python", "SQL", "Airflow", "Apache Spark", "Apache Kafka", "Hadoop", "AWS", "Microsoft Azure", "Google Cloud Platform", "MongoDB", "SQL"],
    "DevOps": ["AWS", "Kubernetes", "Docker", "Terraform", "Ansible", "Jenkins", "Git", "Python", "Linux", "Bash", "GitHub Actions"],
    "Mobile Development": ["Swift", "Kotlin", "Dart", "Flutter", "C++", "Firebase", "TypeScript"],
    "AI/ML": ["Python", "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "OpenCV", "Natural Language Processing", "Machine Learning", "NumPy", "Pandas", "Hugging Face Transformers"],
    "Frontend Engineering": ["JavaScript", "TypeScript", "React.js", "Angular", "Vue.js", "HTML", "CSS", "Tailwind CSS", "Redux", "Bootstrap", "Webpack"],
    "Backend Engineering": ["Python", "Java", "Go", "Rust", "Node.js", "Django", "Flask", "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes", "GraphQL", "FastAPI"],
    "Game Development": ["C++", "Unreal Engine", "Unity", "C#", "Git"],
    "Blockchain": ["Solidity", "Python", "JavaScript", "Hardhat", "Rust", "Smart Contracts"],
    "Systems Programming": ["C", "C++", "Rust", "Assembly", "Go", "Linux"],
    "Security Engineering": ["Python", "OWASP", "Burp Suite", "Metasploit", "Splunk", "Penetration Testing", "Vulnerability Assessment"],
    "Embedded Systems": ["C", "C++", "Assembly", "ARM", "Arduino", "Raspberry Pi"],
    "Data Analysis": ["Python", "SQL", "Excel", "Tableau", "Pandas", "NumPy", "R", "Matplotlib"],
}

LEVEL_REQUIRED_SKILLS = {
    "Junior": ["Git", "Unit Testing", "Debugging", "Agile"],
    "Mid": ["System Design", "Microservices", "REST API", "Docker"],
    "Senior": ["System Design", "AWS", "Kubernetes", "Technical Leadership", "Mentoring"],
    "Lead": ["System Design", "Technical Leadership", "Mentoring", "Cloud Platforms"],
}

LEVEL_SKILL_MIN_COUNTS = {
    "Junior": 3,
    "Mid": 5,
    "Senior": 8,
    "Lead": 10,
}

EXPERIENCE_BASED_SKILLS = {
    "internship": ["Git", "Agile", "Unit Testing", "Debugging", "Code Review", "Python", "SQL", "Docker", "Jenkins"],
    "trainee": ["Python", "Git", "Linux", "SQL", "Bash", "Technical Documentation"],
    "fresher": ["Git", "Unit Testing", "Debugging", "Agile", "Technical Documentation", "Linux", "SQL", "Python", "HTML", "CSS"],
    "entry level": ["Git", "Unit Testing", "Debugging", "Agile", "Technical Documentation", "SQL"],
    "company": ["Code Review", "CI/CD Practices", "Docker", "Kubernetes", "System Design", "Mentoring"],
}

EXPERIENCE_KEYWORDS = {
    "internship": ["intern", "internship", "internships"],
    "trainee": ["trainee", "training", "co-op"],
    "fresher": ["fresher", "entry", "beginner", "0 years"],
    "company": ["company", "worked at", "employed at", "full-time", "part-time"],
}


class MissingSkillDetector:
    async def detect(
        self,
        skills: List[str],
        job_skills: List[str],
        category: Optional[str] = None,
        level: Optional[str] = None,
        experience: Optional[List[dict]] = None,
    ) -> List[str]:
        """Detect missing skills in a resume.

        Compares extracted skills against:
        - Job description skills (if provided)
        - Category-recommended skills (if category provided)
        - Level-based skills (junior, mid, senior, lead)
        - Experience-based skills (internship, trainee, company work, etc.)
        Only returns meaningful technical skills, not random words.
        """
        found_skills_lower = {s.lower().strip() for s in skills}
        missing = set()

        def add_all(candidates: List[str]) -> None:
            for skill in candidates:
                lowered = skill.lower().strip()
                if not lowered:
                    continue
                if lowered in found_skills_lower:
                    continue
                # Skip if an already-known skill partially overlaps this one.
                if any(
                    lowered in found or found in lowered
                    for found in found_skills_lower
                    if len(found) > 2 and len(lowered) > 2
                ):
                    continue
                missing.add(skill)

        # Compare against job description skills
        if job_skills:
            add_all(job_skills)

        # Compare against category-recommended skills
        if category:
            add_all(CATEGORY_RECOMMENDED_SKILLS.get(category, []))

        # Level-based skill recommendations
        if level:
            add_all(LEVEL_REQUIRED_SKILLS.get(level, []))

            # Check minimum skill count for level
            min_count = LEVEL_SKILL_MIN_COUNTS.get(level, 0)
            if len(found_skills_lower) < min_count:
                add_all(["Git", "Unit Testing", "Debugging"])

        # Experience-based skill recommendations
        if experience:
            exp_text = " ".join(str(e.get("raw", "")) for e in experience).lower()
            for exp_type, keywords in EXPERIENCE_KEYWORDS.items():
                if any(kw in exp_text for kw in keywords):
                    add_all(EXPERIENCE_BASED_SKILLS.get(exp_type, []))

        return sorted(missing)
