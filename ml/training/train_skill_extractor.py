import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from collections import Counter


def prepare_skill_data(df_resumes, df_jobs, df_skills):
    """Prepare training data for skill extraction."""
    known_skills = set(s.strip().lower() for s in df_skills['name'].tolist())

    texts = []
    labels = []

    for _, row in df_resumes.iterrows():
        skill_list = [s.strip().lower() for s in row['skills'].split(',')]
        for skill in skill_list:
            if skill in known_skills:
                texts.append(skill)
                labels.append(skill)

    for _, row in df_jobs.iterrows():
        skill_list = [s.strip().lower() for s in row['skills'].split(',')]
        for skill in skill_list:
            if skill in known_skills:
                texts.append(skill)
                labels.append(skill)

    return texts, labels, known_skills


def create_negative_examples(known_skills, n_negative=1000):
    """Create negative examples (non-skills) for training."""
    non_skills = [
        "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by",
        "a", "an", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
        "do", "does", "did", "will", "would", "could", "should", "may", "might", "must",
        "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they",
        "experience", "years", "work", "project", "team", "company", "role", "position",
        "responsible", "developed", "managed", "led", "created", "built", "designed",
        "implemented", "collaborated", "participated", "contributed", "achieved", "improved",
        "bachelor", "master", "phd", "degree", "university", "college", "education",
        "certification", "certified", "course", "training", "workshop", "seminar",
        "january", "february", "march", "april", "june", "july", "august",
        "september", "october", "november", "december", "2020", "2021", "2022", "2023", "2024",
    ]

    rng = np.random.RandomState(42)
    negative_texts = []
    negative_labels = []

    for _ in range(n_negative):
        n_words = rng.randint(1, 4)
        words = rng.choice(non_skills, n_words, replace=False)
        text = " ".join(words)
        negative_texts.append(text)
        negative_labels.append("NOT_SKILL")

    return negative_texts, negative_labels


def train():
    print("Loading data...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df_resumes = pd.read_csv(os.path.join(base_dir, "datasets", "raw", "resumes.csv"))
    df_jobs = pd.read_csv(os.path.join(base_dir, "datasets", "raw", "jobs.csv"))
    df_skills = pd.read_csv(os.path.join(base_dir, "datasets", "raw", "skills.csv"))

    print(f"Loaded {len(df_resumes)} resumes, {len(df_jobs)} jobs, {len(df_skills)} skills")

    texts, labels, known_skills = prepare_skill_data(df_resumes, df_jobs, df_skills)
    print(f"Positive examples: {len(texts)}")

    neg_texts, neg_labels = create_negative_examples(known_skills, n_negative=2000)
    texts.extend(neg_texts)
    labels.extend(neg_labels)
    print(f"Total examples: {len(texts)}")

    label_counts = Counter(labels)
    if min(label_counts.values()) < 2:
        print(f"Warning: Some classes have only {min(label_counts.values())} member(s). Skipping stratification.")
        X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
    else:
        X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42, stratify=labels)

    print("Vectorizing...")
    vectorizer = CountVectorizer(ngram_range=(1, 2), max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training MultinomialNB for skill extraction...")
    model = MultinomialNB(alpha=1.0)
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.3f}")

    # Retrain on full data
    model.fit(vectorizer.fit_transform(texts), labels)

    os.makedirs(os.path.join(base_dir, "artifacts", "skill_model"), exist_ok=True)
    joblib.dump(model, os.path.join(base_dir, "artifacts", "skill_model", "model.pkl"))
    joblib.dump(vectorizer, os.path.join(base_dir, "artifacts", "skill_model", "vectorizer.pkl"))
    joblib.dump(list(known_skills), os.path.join(base_dir, "artifacts", "skill_model", "known_skills.pkl"))

    print("Model saved to ml/artifacts/skill_model/")
    print(f"Known skills: {len(known_skills)}")


if __name__ == "__main__":
    train()
