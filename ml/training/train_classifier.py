import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os


def prepare_classification_data(df_resumes):
    """Prepare data for category and level classification."""
    texts = []
    categories = []
    levels = []

    for _, row in df_resumes.iterrows():
        skill_text = row['skills'].replace(',', ' ')
        edu_text = row['education']
        exp_text = f"experience_{row['experience_years']}_years"
        ats_text = f"ats_score_{row.get('ats_score', 75)}"
        text = f"{skill_text} {edu_text} {exp_text} {ats_text}"

        texts.append(text)
        categories.append(row.get('category', 'Software Engineering'))
        levels.append(row.get('level', 'Mid'))

    return texts, categories, levels


def train():
    print("Loading data...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df_resumes = pd.read_csv(os.path.join(base_dir, "datasets", "raw", "resumes.csv"))
    print(f"Loaded {len(df_resumes)} resumes")

    texts, categories, levels = prepare_classification_data(df_resumes)

    cat_encoder = LabelEncoder()
    level_encoder = LabelEncoder()

    y_cat = cat_encoder.fit_transform(categories)
    y_level = level_encoder.fit_transform(levels)

    print(f"Categories: {list(cat_encoder.classes_)}")
    print(f"Levels: {list(level_encoder.classes_)}")

    print("Vectorizing...")
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 1), stop_words='english')
    X = vectorizer.fit_transform(texts)
    print(f"Features shape: {X.shape}")

    X_train, X_test, y_cat_train, y_cat_test, y_level_train, y_level_test = train_test_split(
        X, y_cat, y_level, test_size=0.2, random_state=42, stratify=y_cat
    )

    print("Training category classifier (RandomForest)...")
    cat_model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
    cat_model.fit(X_train, y_cat_train)
    cat_pred = cat_model.predict(X_test)
    cat_acc = accuracy_score(y_cat_test, cat_pred)
    print(f"Category Accuracy: {cat_acc:.3f}")

    print("Training level classifier (RandomForest)...")
    level_model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
    level_model.fit(X_train, y_level_train)
    level_pred = level_model.predict(X_test)
    level_acc = accuracy_score(y_level_test, level_pred)
    print(f"Level Accuracy: {level_acc:.3f}")

    # Retrain on full data
    cat_model.fit(X, y_cat)
    level_model.fit(X, y_level)

    os.makedirs(os.path.join(base_dir, "artifacts", "classifier"), exist_ok=True)
    joblib.dump(cat_model, os.path.join(base_dir, "artifacts", "classifier", "category_model.pkl"))
    joblib.dump(level_model, os.path.join(base_dir, "artifacts", "classifier", "level_model.pkl"))
    joblib.dump(vectorizer, os.path.join(base_dir, "artifacts", "classifier", "vectorizer.pkl"))
    joblib.dump(cat_encoder, os.path.join(base_dir, "artifacts", "classifier", "cat_encoder.pkl"))
    joblib.dump(level_encoder, os.path.join(base_dir, "artifacts", "classifier", "level_encoder.pkl"))

    print("Models saved to ml/artifacts/classifier/")


if __name__ == "__main__":
    train()
