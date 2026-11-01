import pandas as pd


def evaluate():
    df = pd.read_csv("ml/datasets/raw/resumes.csv")
    print("Evaluating ATS model...")
    print(f"Loaded {len(df)} records")


if __name__ == "__main__":
    evaluate()
