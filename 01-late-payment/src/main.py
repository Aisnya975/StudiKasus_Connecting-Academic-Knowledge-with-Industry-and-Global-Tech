import os

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# ==========================================
# 1. GENERASI SYNTHETIC DATASET (PT Maju Bersama)
# ==========================================
np.random.seed(42)
n_samples = 1000

data = {
    "invoice_id": [f"INV-{1000+i}" for i in range(n_samples)],
    "customer_segment": np.random.choice(
        ["Enterprise", "SMB", "Retail"], size=n_samples, p=[0.2, 0.5, 0.3]
    ),
    "payment_terms_days": np.random.choice(
        [15, 30, 60], size=n_samples, p=[0.3, 0.5, 0.2]
    ),
    "invoice_amount": np.random.exponential(scale=15000000, size=n_samples),
    "historical_late_count": np.random.poisson(lam=1.5, size=n_samples),
    "discount_applied": np.random.choice(
        [0, 0.05, 0.10], size=n_samples, p=[0.6, 0.3, 0.1]
    ),
}

df = pd.DataFrame(data)

# Logika penentuan keterlambatan (Target) berdasarkan fitur
prob_late = (
    0.1
    + (df["customer_segment"] == "SMB") * 0.15
    + (df["payment_terms_days"] == 60) * 0.2
    + (df["historical_late_count"] > 2) * 0.3
    - (df["discount_applied"] > 0) * 0.1
)
df["is_late"] = (np.random.rand(n_samples) < prob_late.clip(0, 1)).astype(int)

# Simpan dataset ke CSV
os.makedirs("data", exist_ok=True)
df.to_csv("data/synthetic_invoice_data.csv", index=False)

# ==========================================
# 2. DATA PREPARATION & FEATURE ENGINEERING
# ==========================================
# Encoding variabel kategorikal
encoder = OneHotEncoder(sparse_output=False, drop="first")
encoded_segment = encoder.fit_transform(df[["customer_segment"]])
encoded_segment_df = pd.DataFrame(
    encoded_segment, columns=encoder.get_feature_names_out(["customer_segment"])
)

# Penggabungan fitur (menghindari data leakage)
X = pd.concat(
    [
        df[
            [
                "payment_terms_days",
                "invoice_amount",
                "historical_late_count",
                "discount_applied",
            ]
        ],
        encoded_segment_df,
    ],
    axis=1,
)
y = df["is_late"]

# Split Data (Train: 80%, Test: 20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ==========================================
# 3. PEMODELAN (Random Forest Classifier)
# ==========================================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ==========================================
# 4. EVALUASI MODEL
# ==========================================
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("=== EVALUASI MODEL DETEKSI LATE PAYMENT ===")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

# Importansi Fitur
importance = pd.DataFrame(
    {"Feature": X.columns, "Importance": model.feature_importances_}
).sort_values("Importance", ascending=False)
print("\nFeature Importance:")
print(importance)