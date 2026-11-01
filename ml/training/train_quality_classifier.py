import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder
import joblib
import os


def prepare_quality_data(df_resumes):
    """Prepare data for quality classification."""
    texts = []
    quality_scores = []
    quality_labels = []

    for _, row in df_resumes.iterrows():
        skill_text = row['skills'].replace(',', ' ')
        edu_text = row['education']
        exp_text = f"experience_{row['experience_years']}_years"
        text = f"{skill_text} {edu_text} {exp_text}"

        texts.append(text)
        score = float(row.get('quality_score', 75))
        quality_scores.append(score)

        if score >= 85:
            quality_labels.append("High")
        elif score >= 70:
            quality_labels.append("Medium")
        else:
            quality_labels.append("Low")

    return texts, quality_scores, quality_labels


def train():
    print("Loading data...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df_resumes = pd.read_csv(os.path.join(base_dir, "datasets", "raw", "resumes.csv"))
    print(f"Loaded {len(df_resumes)} resumes")

    texts, quality_scores, quality_labels = prepare_quality_data(df_resumes)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(quality_labels)

    print(f"Quality classes: {list(label_encoder.classes_)}")
    print(f"Score range: {min(quality_scores)}-{max(quality_scores)}")

    print("Vectorizing...")
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 1), stop_words='english')
    X = vectorizer.fit_transform(texts)
    print(f"Features shape: {X.shape}")

    X_train, X_test, y_train, y_test, score_train, score_test = train_test_split(
        X, y, quality_scores, test_size=0.2, random_state=42, stratify=y
    )

    print("Training quality classifier (RandomForest)...")
    model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Quality Classification Accuracy: {acc:.3f}")

    print("Training quality regressor (RandomForest)...")
    reg_model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
    reg_model.fit(X_train, np.array(score_train))
    score_pred = reg_model.predict(X_test)
    mse = mean_squared_error(score_test, score_pred)
    rmse = np.sqrt(mse)
    print(f"Quality Score MSE: {mse:.2f}, RMSE: {rmse:.2f}")

    model.fit(X, y)
    reg_model.fit(X, np.array(quality_scores))

    os.makedirs(os.path.join(base_dir, "artifacts", "quality_classifier"), exist_ok=True)
    joblib.dump(model, os.path.join(base_dir, "artifacts", "quality_classifier", "classifier.pkl"))
    joblib.dump(reg_model, os.path.join(base_dir, "artifacts", "quality_classifier", "regressor.pkl"))
    joblib.dump(vectorizer, os.path.join(base_dir, "artifacts", "quality_classifier", "vectorizer.pkl"))
    joblib.dump(label_encoder, os.path.join(base_dir, "artifacts", "quality_classifier", "label_encoder.pkl"))

    print("Models saved to ml/artifacts/quality_classifier/")


if __name__ == "__main__":
    train()
