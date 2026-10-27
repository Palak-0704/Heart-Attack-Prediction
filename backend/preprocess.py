"""Re-creates the notebook preprocessing (IQR clipping + StandardScaler on numeric cols)."""
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
FEATURES = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
            "thalach", "exang", "oldpeak", "slope", "ca", "thal"]


class Preprocessor:
    def __init__(self, csv_path: Path = ROOT / "heart.csv"):
        df = pd.read_csv(csv_path)
        # same rule as notebook: categorical = <= 10 unique values
        self.num_cols = [c for c in FEATURES if df[c].nunique() > 10]
        self.bounds = {}
        for c in self.num_cols:
            q1, q3 = df[c].quantile(0.25), df[c].quantile(0.75)
            iqr = q3 - q1
            self.bounds[c] = (q1 - 1.5 * iqr, q3 + 1.5 * iqr)
        clipped = df[self.num_cols].copy()
        for c in self.num_cols:
            clipped[c] = clipped[c].clip(*self.bounds[c])
        self.scaler = StandardScaler().fit(clipped)

    def transform(self, row: dict) -> pd.DataFrame:
        x = pd.DataFrame([row], columns=FEATURES).astype(float)
        for c in self.num_cols:
            x[c] = x[c].clip(*self.bounds[c])
        x[self.num_cols] = self.scaler.transform(x[self.num_cols])
        return x
