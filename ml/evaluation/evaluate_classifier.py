import pandas as pd


def evaluate():
    df = pd.read_csv("ml/datasets/raw/resumes.csv")
    print("Evaluating classifier...")
    print(f"Loaded {len(df)} records")


if __name__ == "__main__":
    evaluate()
