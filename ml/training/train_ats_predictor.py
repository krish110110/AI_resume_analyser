import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import os


def extract_edu_level(text):
    edu_lower = text.lower()
    if any(kw in edu_lower for kw in ['phd', 'doctorate']):
        return 3
    elif any(kw in edu_lower for kw in ['master', 'mba', 'ms', 'm.s.']):
        return 2
    elif any(kw in edu_lower for kw in ['bachelor', 'bs', 'b.s.', 'degree']):
        return 1
    return 0


def create_features(df_resumes, df_jobs):
    """Create features for ATS prediction from resume and job data."""
    features = []
    targets = []

    for _, resume in df_resumes.iterrows():
        resume_skills = set(s.strip().lower() for s in resume['skills'].split(','))
        ats_score = float(resume.get('ats_score', 75))

        for _, job in df_jobs.iterrows():
            job_skills = set(s.strip().lower() for s in job['skills'].split(','))

            skill_match = len(resume_skills & job_skills) / len(job_skills) if len(job_skills) > 0 else 0.0
            exp_years = float(resume['experience_years'])
            exp_years_norm = min(exp_years / 10.0, 1.0)
            edu_level = extract_edu_level(resume['education'])
            num_skills = len(resume_skills)
            overlap_count = len(resume_skills & job_skills)
            skill_diversity = len(resume_skills)

            target_score = min(max(ats_score * (0.5 + 0.5 * skill_match), 0), 100)

            features.append([
                skill_match,
                exp_years_norm,
                edu_level,
                num_skills,
                overlap_count,
                skill_diversity,
            ])
            targets.append(target_score)

    return np.array(features), np.array(targets)


def train():
    print("Loading data...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df_resumes = pd.read_csv(os.path.join(base_dir, "datasets", "raw", "resumes.csv"))
    df_jobs = pd.read_csv(os.path.join(base_dir, "datasets", "raw", "jobs.csv"))
    print(f"Loaded {len(df_resumes)} resumes and {len(df_jobs)} jobs")

    X, y = create_features(df_resumes, df_jobs)
    print(f"Created {len(X)} training samples with {X.shape[1]} features")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Training GradientBoostingRegressor...")
    model = GradientBoostingRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Test MSE: {mse:.2f}, R2: {r2:.3f}")

    model.fit(X_train_scaled, y_train)

    os.makedirs(os.path.join(base_dir, "artifacts", "ats_predictor"), exist_ok=True)
    joblib.dump(model, os.path.join(base_dir, "artifacts", "ats_predictor", "model.pkl"))
    joblib.dump(scaler, os.path.join(base_dir, "artifacts", "ats_predictor", "scaler.pkl"))

    feature_names = ['skill_match', 'exp_years', 'edu_level', 'num_skills', 'overlap_count', 'skill_diversity']
    joblib.dump(feature_names, os.path.join(base_dir, "artifacts", "ats_predictor", "feature_names.pkl"))

    print("Model saved to ml/artifacts/ats_predictor/model.pkl")
    for name, coef in zip(feature_names, model.feature_importances_):
        print(f"  {name}: {coef:.4f}")


if __name__ == "__main__":
    train()
