import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import os


def prepare_ranking_data(df_resumes, df_jobs):
    """Prepare data for resume-job ranking (fit/no-fit)."""
    texts = []
    labels = []
    feature_vectors = []

    for _, resume in df_resumes.iterrows():
        resume_skills = set(s.strip().lower() for s in resume['skills'].split(','))

        for _, job in df_jobs.iterrows():
            job_skills = set(s.strip().lower() for s in job['skills'].split(','))

            skill_match = len(resume_skills & job_skills) / len(job_skills) if len(job_skills) > 0 else 0.0

            text = f"{resume['skills']} {resume['education']} experience_years {resume['experience_years']} {job['description']} {job['skills']}"
            texts.append(text)

            labels.append(1 if skill_match > 0.35 else 0)

            exp_diff = abs(int(resume['experience_years']) - 3)
            feature_vectors.append([
                skill_match,
                exp_diff / 10.0,
                len(resume_skills) / 15.0,
                len(job_skills) / 15.0,
            ])

    return texts, np.array(labels), np.array(feature_vectors)


def train():
    print("Loading data...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df_resumes = pd.read_csv(os.path.join(base_dir, "datasets", "raw", "resumes.csv"))
    df_jobs = pd.read_csv(os.path.join(base_dir, "datasets", "raw", "jobs.csv"))
    print(f"Loaded {len(df_resumes)} resumes and {len(df_jobs)} jobs")

    texts, labels, feature_vectors = prepare_ranking_data(df_resumes, df_jobs)
    print(f"Created {len(texts)} ranking samples")
    print(f"Positive: {sum(labels)}, Negative: {len(labels) - sum(labels)}")

    print("Vectorizing...")
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 1), stop_words='english')
    X_text = vectorizer.fit_transform(texts)
    print(f"Text features shape: {X_text.shape}")

    X_combined = np.hstack([X_text.toarray(), feature_vectors])
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_combined)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, labels, test_size=0.2, random_state=42, stratify=labels
    )

    print("Training GradientBoostingClassifier for ranking...")
    model = GradientBoostingClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Ranking Accuracy: {acc:.3f}")
    print(classification_report(y_test, y_pred, target_names=['Poor Fit', 'Good Fit']))

    model.fit(X_scaled, labels)

    os.makedirs(os.path.join(base_dir, "artifacts", "ranking_model"), exist_ok=True)
    joblib.dump(model, os.path.join(base_dir, "artifacts", "ranking_model", "model.pkl"))
    joblib.dump(vectorizer, os.path.join(base_dir, "artifacts", "ranking_model", "vectorizer.pkl"))
    joblib.dump(scaler, os.path.join(base_dir, "artifacts", "ranking_model", "scaler.pkl"))

    print("Models saved to ml/artifacts/ranking_model/")


if __name__ == "__main__":
    train()
