import pandas as pd
import numpy as np
import os
import random

np.random.seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "datasets", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

SKILL_CATEGORIES = {
    "programming": ["python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
                    "swift", "kotlin", "php", "ruby", "scala", "r", "matlab", "julia",
                    "elixir", "haskell", "lua", "vb.net", "assembly", "dart", "groovy", "perl", "vba"],
    "frontend": ["react", "angular", "vue.js", "svelte", "next.js", "sveltekit", "remix",
                 "node.js", "express", "fastify", "jquery", "redux", "ngrx", "rxjs"],
    "backend": ["django", "flask", "fastapi", "spring boot", "rails", "laravel", "phoenix",
                "actix", "yesod", "nestjs", ".net", "express", "go", "fiber"],
    "database": ["sql", "postgresql", "mysql", "mongodb", "redis", "cassandra", "elasticsearch",
                 "dynamodb", "sqlite", "oracle", "firebase", "supabase"],
    "cloud": ["aws", "azure", "gcp", "lambda", "cloudformation", "terraform", "kubernetes",
              "docker", "serverless", "cloud run", "ec2", "s3"],
    "devops": ["git", "github", "gitlab", "jenkins", "github actions", "gitlab ci",
               "ansible", "terraform", "prometheus", "grafana", "datadog", "splunk"],
    "ai_ml": ["machine learning", "deep learning", "tensorflow", "pytorch", "keras",
              "scikit-learn", "xgboost", "lightgbm", "opencv", "nlp", "transformers", "hugging face"],
    "data": ["pandas", "numpy", "tableau", "power bi", "excel", "airflow", "spark",
             "kafka", "flink", "hadoop", "hive", "pyspark", "sql"],
    "mobile": ["swift", "swiftui", "xcode", "kotlin", "android", "jetpack compose", "room",
             "retrofit", "flutter", "dart", "firebase", "react native", "ionic"],
    "testing": ["testing", "unit testing", "integration testing", "e2e testing",
                "selenium", "cypress", "playwright", "jest", "vitest", "pytest", "unittest"],
    "security": ["burp suite", "metasploit", "owasp", "penetration testing",
                 "vulnerability assessment", "splunk"],
    "game": ["c++", "unreal engine", "blueprints", "unity", "csharp", "git"],
    "embedded": ["c", "c++", "assembly", "arm", "x86", "stm32", "arduino", "raspberry pi"],
}

CATEGORIES = ["Software Engineering", "Data Science", "Data Engineering", "DevOps", "Mobile Development",
              "AI/ML", "Frontend Engineering", "Backend Engineering", "Game Development",
              "Blockchain", "Systems Programming", "Security Engineering", "Embedded Systems"]

LEVELS = ["Junior", "Mid", "Senior", "Lead"]

EDUCATIONS = ["Bachelor's CS", "Bachelor's IT", "Bachelor's Software Engineering",
              "Master's CS", "Master's Data Science", "Master's Engineering",
              "PhD Computer Science", "Bachelor's Information Systems"]

JOBS = [
    ("Software Engineer", "Develop web applications using Python and React. Build scalable backend services.",
     ["python", "react", "sql", "aws", "docker"]),
    ("Data Scientist", "Analyze data and build ML models. Work with large datasets and create predictive models.",
     ["python", "machine learning", "sql", "pandas", "scikit-learn"]),
    ("Senior Backend Developer", "Design and implement microservices using Java and Spring Boot. Deploy on AWS with Docker.",
     ["java", "spring boot", "hibernate", "postgresql", "aws"]),
    ("Frontend Developer", "Create responsive UIs with React, Redux, and TypeScript. Optimize for performance.",
     ["javascript", "react", "redux", "typescript", "node.js"]),
    ("ML Engineer", "Build and deploy ML models using TensorFlow/PyTorch. Computer vision and NLP tasks.",
     ["python", "tensorflow", "pytorch", "keras", "opencv"]),
    ("Data Engineer", "Build ETL pipelines with Airflow and Spark. Manage Kafka streams and data warehouses.",
     ["sql", "python", "airflow", "spark", "kafka"]),
    ("DevOps Engineer", "Manage Kubernetes clusters, CI/CD pipelines with Terraform. Monitoring with Prometheus/Grafana.",
     ["go", "kubernetes", "terraform", "prometheus", "grafana"]),
    ("iOS Developer", "Build iOS apps with Swift and SwiftUI. Integrate with Core Data and CloudKit.",
     ["swift", "swiftui", "xcode", "core data", "ios"]),
    ("Full Stack Developer", "Build end-to-end features with Ruby on Rails and PostgreSQL.",
     ["ruby", "rails", "postgresql", "redis", "sidekiq"]),
    ("Android Developer", "Build Android apps with Kotlin and Jetpack Compose.",
     ["kotlin", "android", "jetpack compose", "room", "retrofit"]),
    ("Cloud Architect", "Design cloud architectures. Kubernetes, Terraform, serverless with Lambda.",
     ["aws", "kubernetes", "terraform", "lambda", "cloudformation"]),
    ("Security Engineer", "Application security, penetration testing. OWASP compliance.",
     ["python", "burp suite", "metasploit", "splunk", "owasp"]),
    ("Embedded Systems Engineer", "Real-time systems with C and ARM. Control systems with MATLAB.",
     ["c", "assembly", "arm", "x86", "matlab"]),
    ("Blockchain Developer", "Smart contracts with Solidity. Web3 integration with Hardhat.",
     ["solidity", "web3", "hardhat", "ethers.js", "ipfs"]),
    ("Systems Programmer", "High-performance systems with Rust. Async programming with Tokio.",
     ["rust", "tokio", "actix", "postgres", "diesel"]),
]

CAT_SKILLS = {
    "Software Engineering": ["python", "java", "javascript", "typescript", "react", "django", "spring boot",
                             "sql", "postgresql", "aws", "docker", "node.js", "flask", "ruby", "rails"],
    "Data Science": ["python", "machine learning", "sql", "pandas", "scikit-learn", "tensorflow",
                     "pytorch", "r", "tableau", "numpy"],
    "Data Engineering": ["python", "sql", "airflow", "spark", "kafka", "hadoop", "pyspark",
                         "java", "scala", "aws", "azure", "gcp"],
    "DevOps": ["aws", "kubernetes", "docker", "terraform", "ansible", "jenkins", "git",
               "python", "go", "linux", "bash"],
    "Mobile Development": ["swift", "kotlin", "react native", "flutter", "kotlin",
                           "android", "xcode", "firebase"],
    "AI/ML": ["python", "tensorflow", "pytorch", "keras", "scikit-learn", "opencv",
              "nlp", "machine learning", "deep learning", "numpy", "pandas"],
    "Frontend Engineering": ["javascript", "typescript", "react", "angular", "vue.js",
                            "html", "css", "redux", "sass", "webpack"],
    "Backend Engineering": ["python", "java", "go", "rust", "node.js", "django", "flask",
                           "postgresql", "mongodb", "redis", "docker", "kubernetes"],
    "Game Development": ["c++", "unreal engine", "unity", "csharp", "git", "blueprints"],
    "Blockchain": ["solidity", "web3", "python", "javascript", "hardhat", "ethers.js", "ipfs"],
    "Systems Programming": ["c", "c++", "rust", "assembly", "go", "linux", "x86", "arm"],
    "Security Engineering": ["python", "solidity", "owasp", "burp suite", "metasploit", "splunk"],
    "Embedded Systems": ["c", "c++", "assembly", "arm", "x86", "stm32", "arduino"],
}


def generate_resume(i):
    category = random.choice(CATEGORIES)
    level = random.choice(LEVELS)

    skills_pool = CAT_SKILLS[category]
    n_skills = random.randint(4, 8)
    skills = random.sample(skills_pool, min(n_skills, len(skills_pool)))
    # Add some extra skills sometimes
    if random.random() > 0.5:
        extra_cat = random.choice(list(CAT_SKILLS.keys()))
        extra_skills = random.sample(CAT_SKILLS[extra_cat], min(2, len(CAT_SKILLS[extra_cat])))
        skills = list(set(skills + extra_skills))

    skills_str = ", ".join(sorted(skills))

    exp_map = {"Junior": (0, 2), "Mid": (3, 5), "Senior": (6, 10), "Lead": (8, 15)}
    exp_years = random.randint(*exp_map[level])

    education = random.choice(EDUCATIONS)

    # Derive quality score deterministically from features
    edu_map = {"phd": 3, "master": 2, "bachelor": 1}
    edu_lower = education.lower()
    edu_val = 0
    for k, v in edu_map.items():
        if k in edu_lower:
            edu_val = v
            break

    # More skills, more experience, higher education = higher quality
    skill_score = (len(skills) - 4) / 4.0 * 25  # 0-25
    exp_score = (exp_years - 0) / 15.0 * 15  # 0-15
    edu_score = edu_val / 3.0 * 10  # 0-10
    # Add category-specific bonus
    cat_bonus = {"AI/ML": 10, "Data Science": 8, "DevOps": 7, "Security Engineering": 8,
                 "Blockchain": 7, "Systems Programming": 8, "Embedded Systems": 7}.get(category, 5)

    quality_score = int(55 + skill_score + exp_score + edu_score + cat_bonus)
    quality_score = min(max(quality_score, 55), 98)
    ats_base = quality_score

    year = 2024 + (i // 12)
    month = 1 + (i % 12)
    created_at = f"{year}-{month:02d}-{1 + (i % 28):02d}"

    names = ["John", "Jane", "Alex", "Maria", "David", "Sarah", "Michael", "Emily",
             "James", "Lisa", "Robert", "Amanda", "Christopher", "Nicole", "Daniel",
             "Michelle", "Kevin", "Ashley", "Matthew", "Samantha", "Andrew", "Stephanie",
             "Joshua", "Lauren", "Brandon", "Rebecca", "Tyler", "Danielle", "Sean", "Kristen",
             "Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia", "Mason", "Isabella"]
    last_names = ["Doe", "Smith", "Johnson", "Brown", "Davis", "Miller", "Wilson", "Taylor",
                  "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson",
                  "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez"]
    name = f"{random.choice(names)} {random.choice(last_names)}"
    email = f"{name.split()[0].lower()}{i}@example.com"

    return {
        "id": i,
        "name": name,
        "email": email,
        "skills": skills_str,
        "experience_years": exp_years,
        "education": education,
        "created_at": created_at,
        "ats_score": ats_base,
        "category": category,
        "level": level,
        "quality_score": quality_score,
    }


def generate_jobs(start_id):
    rows = []
    for i, (title, desc, skills) in enumerate(JOBS):
        rows.append({
            "id": start_id + i,
            "title": title,
            "company": random.choice(["TechCorp", "DataInc", "CloudSystems", "WebAgency",
                                     "AIStartup", "BigDataCorp", "GameStudio", "MobileAppCo",
                                     "InfraTech", "StartupXYZ"]),
            "description": desc,
            "skills": ", ".join(skills),
            "created_at": f"2024-01-{10 + i:02d}",
        })
    return rows


def main():
    resumes = [generate_resume(i + 1) for i in range(150)]
    df_resumes = pd.DataFrame(resumes)
    df_resumes.to_csv(os.path.join(RAW_DIR, "resumes.csv"), index=False)
    print(f"Generated {len(df_resumes)} resumes")

    jobs = generate_jobs(1)
    df_jobs = pd.DataFrame(jobs)
    df_jobs.to_csv(os.path.join(RAW_DIR, "jobs.csv"), index=False)
    print(f"Generated {len(df_jobs)} jobs")

    df_skills = pd.read_csv(os.path.join(RAW_DIR, "skills.csv"))
    print(f"Skills CSV has {len(df_skills)} entries")

    if not os.path.exists(os.path.join(RAW_DIR, "interview_questions.csv")):
        questions = []
        for cat in CATEGORIES:
            for q in ["What are your greatest strengths?", "Tell me about yourself.",
                      "Why do you want to work here?", "Describe a challenging project.",
                      "How do you handle failure?", "Where do you see yourself in 5 years?"]:
                questions.append({"category": cat, "question": q})
        df_questions = pd.DataFrame(questions)
        df_questions.to_csv(os.path.join(RAW_DIR, "interview_questions.csv"), index=False)
        print(f"Generated {len(df_questions)} interview questions")

    print("\nResumes by category:")
    print(df_resumes["category"].value_counts().to_dict())
    print("\nResumes by level:")
    print(df_resumes["level"].value_counts().to_dict())
    print(f"\nATS score range: {df_resumes['ats_score'].min()}-{df_resumes['ats_score'].max()}")
    print(f"Quality score range: {df_resumes['quality_score'].min()}-{df_resumes['quality_score'].max()}")


if __name__ == "__main__":
    main()
