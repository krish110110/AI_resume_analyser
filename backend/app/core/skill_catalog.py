"""Canonical skill catalog for the resume analyzer.

This is the single source of truth for which skills the system recognizes,
extracts from resumes, recommends as missing, and has interview questions for.
"""

SKILL_CATALOG = {
    # Programming
    "Python": "Programming",
    "Java": "Programming",
    "JavaScript": "Programming",
    "TypeScript": "Programming",
    "C": "Programming",
    "C++": "Programming",
    "C#": "Programming",
    "Go": "Programming",
    "Rust": "Programming",
    "PHP": "Programming",
    "Ruby": "Programming",
    "Kotlin": "Programming",
    "Swift": "Programming",
    "Dart": "Programming",
    "R": "Data Science",
    "MATLAB": "Scientific Computing",
    "Scala": "Programming",
    "Perl": "Programming",
    "SQL": "Database",
    "Bash": "Scripting",
    # Web
    "HTML": "Web",
    "CSS": "Web",
    "React.js": "Frontend",
    "Next.js": "Full Stack",
    "Angular": "Frontend",
    "Vue.js": "Frontend",
    "Svelte": "Frontend",
    "Node.js": "Backend",
    "Express.js": "Backend",
    "FastAPI": "Backend",
    "Django": "Backend",
    "Flask": "Backend",
    "Spring Boot": "Backend",
    ".NET": "Backend",
    "Laravel": "Backend",
    "Tailwind CSS": "CSS Framework",
    "Bootstrap": "CSS Framework",
    "Redux": "State Management",
    "GraphQL": "API",
    "REST API": "API",
    "RESTful Services": "Backend",
    "Microservices": "Architecture",
    "System Design": "Software Engineering",
    # Databases
    "PostgreSQL": "Database",
    "MySQL": "Database",
    "MongoDB": "Database",
    "SQLite": "Database",
    "Redis": "Database/Cache",
    "ClickHouse": "Analytics Database",
    "Elasticsearch": "Search",
    "Cassandra": "Database",
    "Oracle Database": "Database",
    "Microsoft SQL Server": "Database",
    # Data science libraries
    "NumPy": "Data Science",
    "Pandas": "Data Science",
    "Matplotlib": "Data Visualization",
    "Seaborn": "Data Visualization",
    "Plotly": "Data Visualization",
    # Machine learning
    "Scikit-learn": "Machine Learning",
    "TensorFlow": "Deep Learning",
    "PyTorch": "Deep Learning",
    "Keras": "Deep Learning",
    "XGBoost": "Machine Learning",
    "LightGBM": "Machine Learning",
    "CatBoost": "Machine Learning",
    "Hugging Face Transformers": "NLP/AI",
    "spaCy": "NLP",
    "NLTK": "NLP",
    "OpenCV": "Computer Vision",
    "FAISS": "Vector Search",
    "Sentence Transformers": "NLP/Embeddings",
    "LangChain": "Generative AI",
    "LlamaIndex": "Generative AI",
    # AI concepts
    "Machine Learning": "AI",
    "Deep Learning": "AI",
    "Natural Language Processing": "AI",
    "Computer Vision": "AI",
    "Generative AI": "AI",
    "Reinforcement Learning": "AI",
    "Recommendation Systems": "AI",
    "Time Series Analysis": "Data Science",
    "Feature Engineering": "Machine Learning",
    "Model Evaluation": "Machine Learning",
    "MLOps": "Machine Learning/DevOps",
    # DevOps and tooling
    "Git": "Version Control",
    "GitHub": "Development",
    "Docker": "DevOps",
    "Kubernetes": "DevOps",
    "Jenkins": "CI/CD",
    "GitHub Actions": "CI/CD",
    "Linux": "Operating System",
    "AWS": "Cloud",
    "Microsoft Azure": "Cloud",
    "Google Cloud Platform": "Cloud",
    "Terraform": "Infrastructure",
    "Apache Spark": "Big Data",
    "Apache Kafka": "Data Engineering",
    "Airflow": "Data Engineering",
    "Selenium": "Automation",
    "BeautifulSoup": "Web Scraping",
}

CANONICAL_SKILLS = list(SKILL_CATALOG.keys())

# Variants written in resumes mapped to the canonical catalog name.
SKILL_ALIASES = {
    "python3": "Python",
    "py": "Python",
    "java8": "Java",
    "java 8": "Java",
    "js": "JavaScript",
    "ecmascript": "JavaScript",
    "es6": "JavaScript",
    "ts": "TypeScript",
    "golang": "Go",
    "c++11": "C++",
    "c++14": "C++",
    "c++17": "C++",
    "cpp": "C++",
    "c sharp": "C#",
    "csharp": "C#",
    "dotnet": ".NET",
    "asp.net": ".NET",
    "aspnet": ".NET",
    "node": "Node.js",
    "nodejs": "Node.js",
    "express": "Express.js",
    "reactjs": "React.js",
    "react js": "React.js",
    "nextjs": "Next.js",
    "next js": "Next.js",
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "vue 3": "Vue.js",
    "springboot": "Spring Boot",
    "spring boot": "Spring Boot",
    "laravel framework": "Laravel",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "postgres": "PostgreSQL",
    "postgresql database": "PostgreSQL",
    "psql": "PostgreSQL",
    "mongo": "MongoDB",
    "mssql": "Microsoft SQL Server",
    "sql server": "Microsoft SQL Server",
    "microsoft sqlserver": "Microsoft SQL Server",
    "oracle db": "Oracle Database",
    "plsql": "Oracle Database",
    "pl/sql": "Oracle Database",
    "click house": "ClickHouse",
    "elastic search": "Elasticsearch",
    "apache kafka": "Apache Kafka",
    "kafka streams": "Apache Kafka",
    "spark": "Apache Spark",
    "pyspark": "Apache Spark",
    "apache airflow": "Airflow",
    "docker compose": "Docker",
    "containerization": "Docker",
    "containers": "Docker",
    "k8s": "Kubernetes",
    "amazon web services": "AWS",
    "azure cloud": "Microsoft Azure",
    "gcp": "Google Cloud Platform",
    "google cloud": "Google Cloud Platform",
    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "sk learn": "Scikit-learn",
    "tf-idf": "Machine Learning",
    "huggingface": "Hugging Face Transformers",
    "hugging face": "Hugging Face Transformers",
    "transformers": "Hugging Face Transformers",
    "nltk toolkit": "NLTK",
    "open cv": "OpenCV",
    "faiss library": "FAISS",
    "sentence-transformers": "Sentence Transformers",
    "sentence bert": "Sentence Transformers",
    "langgraph": "LangChain",
    "llama index": "LlamaIndex",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "genai": "Generative AI",
    "gen ai": "Generative AI",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "rl": "Reinforcement Learning",
    "recommender systems": "Recommendation Systems",
    "recommendation system": "Recommendation Systems",
    "bash scripting": "Bash",
    "shell scripting": "Bash",
    "shell": "Bash",
    "r language": "R",
    "matlab programming": "MATLAB",
    "ruby on rails": "Ruby",
    "rails": "Ruby",
    "rest": "REST API",
    "rest apis": "REST API",
    "restful api": "RESTful Services",
    "restful architecture": "RESTful Services",
    "microservice architecture": "Microservices",
    "system design patterns": "System Design",
    "selenium testing": "Selenium",
    "web scraping": "BeautifulSoup",
    "beautiful soup": "BeautifulSoup",
    "data analysis": "Pandas",
    "data visualization": "Matplotlib",
}

# Skills grouped by category, used by question seeding and the frontend filters.
SKILLS_BY_CATEGORY = {}
for _skill, _category in SKILL_CATALOG.items():
    SKILLS_BY_CATEGORY.setdefault(_category, []).append(_skill)


def canonical_skills() -> list:
    """Return the canonical skill names."""
    return list(CANONICAL_SKILLS)


def categorize(skill: str) -> str:
    """Return the category for a canonical skill, or 'Other'."""
    return SKILL_CATALOG.get(skill, "Other")


def normalize_skill(name: str) -> str:
    """Map a raw detected skill name onto the canonical catalog name."""
    if not name:
        return ""
    cleaned = name.strip()
    if cleaned in SKILL_CATALOG:
        return cleaned
    lowered = cleaned.lower()
    if lowered in SKILL_ALIASES:
        return SKILL_ALIASES[lowered]
    for canonical in CANONICAL_SKILLS:
        if canonical.lower() == lowered:
            return canonical
    return ""
