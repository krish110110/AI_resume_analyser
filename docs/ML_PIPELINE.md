# ML Pipeline

## Stages

### 1. Parsing
- **TextCleaner**: Normalizes and cleans raw text
- **SectionDetector**: Identifies resume sections using regex
- **ResumeParser**: Orchestrates parsing

### 2. Extraction
- **SkillExtractor**: Matches skills against known database
- **EducationExtractor**: Finds degrees and institutions
- **ExperienceExtractor**: Extracts work history with dates
- **ProjectExtractor**: Identifies project entries
- **CertificationExtractor**: Finds certifications

### 3. Classification
- **ResumeClassifier**: Predicts category and seniority level
- **QualityClassifier**: Predicts resume quality score and issues

### 4. Scoring
- **ATSPredictor**: Predicts ATS compatibility score
- **ScoreExplainer**: Generates human-readable feedback
- **SimilarityService**: Computes text similarity using embeddings
- **SkillMatcher**: Calculates skills match percentage
- **MissingSkillDetector**: Identifies skill gaps

### 5. Recommendations
- **SuggestionGenerator**: Creates actionable improvement suggestions
- **ResourceRetriever**: Finds learning resources for missing skills
- **FaissIndex**: Vector search for similar resumes

### 6. Interview Prep
- **QuestionGenerator**: Generates interview questions from resume + job
- **QuestionRetriever**: Retrieves relevant questions by skill

## Models
- Skill extraction: Rule-based + pattern matching
- Classification: Random Forest / Naive Bayes
- ATS prediction: Linear regression / ensemble
- Similarity: Sentence Transformers + FAISS
- Quality: Random Forest classifier

## Training
Scripts in `ml/training/` train each model on datasets in `ml/datasets/`.
Trained artifacts are saved to `ml/artifacts/`.

## Evaluation
Scripts in `ml/evaluation/` compute precision, recall, F1, and accuracy.
