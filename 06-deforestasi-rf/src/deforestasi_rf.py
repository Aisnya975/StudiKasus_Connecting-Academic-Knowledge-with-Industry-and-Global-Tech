import os

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

FITUR = ["Delta_NDVI", "Delta_NBR", "Patch_Size_Ha", "Distance_to_Road_km", "Elevation_m"]
NAMA_KELAS = ["Pertanian", "Logging", "Kebakaran"]

# 1. Simulasi dataset fitur ekstraksi citra satelit
np.random.seed(42)
n_samples = 300

delta_ndvi = np.random.uniform(-0.8, -0.1, n_samples)
delta_nbr = np.random.uniform(-0.7, -0.2, n_samples)
patch_size = np.random.exponential(scale=5.0, size=n_samples)
dist_road = np.random.exponential(scale=2.0, size=n_samples)
elevation = np.random.uniform(50, 1200, n_samples)

X = pd.DataFrame(
    {
        "Delta_NDVI": delta_ndvi,
        "Delta_NBR": delta_nbr,
        "Patch_Size_Ha": patch_size,
        "Distance_to_Road_km": dist_road,
        "Elevation_m": elevation,
    }
)

# Label target pemicu deforestasi:
# 0 = Pertanian/Perkebunan skala kecil, 1 = Penebangan komersial, 2 = Kebakaran hutan
conditions = [
    (patch_size < 3) & (dist_road < 2),
    (patch_size >= 3) & (delta_nbr < -0.4),
    (patch_size >= 5) & (dist_road >= 2),
]
choices = [0, 2, 1]
y = pd.Series(np.select(conditions, choices, default=0), name="Pemicu")

os.makedirs("data", exist_ok=True)
pd.concat([X, y], axis=1).to_csv("data/data_deforestasi.csv", index=False)

print("Jumlah sampel per kelas:")
print(y.map(dict(enumerate(NAMA_KELAS))).value_counts().to_string())

# 2. Bagi data latih dan data uji (stratify agar semua kelas ada di data uji)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3. Latih model Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 4. Evaluasi model
y_pred = rf_model.predict(X_test)

print("\n--- HASIL EVALUASI MODEL ---")
print(f"Akurasi Model: {accuracy_score(y_test, y_pred) * 100:.1f}%")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=[0, 1, 2]))
print("\nLaporan Klasifikasi:")
print(
    classification_report(
        y_test,
        y_pred,
        labels=[0, 1, 2],
        target_names=NAMA_KELAS,
        zero_division=0,
    )
)

# 5. Feature importance
importance = pd.DataFrame(
    {"Fitur": FITUR, "Importance": rf_model.feature_importances_}
).sort_values("Importance", ascending=False)
print("Feature Importance:")
print(importance.to_string(index=False))

# 6. Prediksi untuk sampel peringatan deforestasi baru
sampel_baru = pd.DataFrame([[-0.65, -0.55, 4.2, 1.5, 300.0]], columns=FITUR)
prediksi = rf_model.predict(sampel_baru)

nama_pemicu = ["Pertanian / Perkebunan", "Penebangan Komersial", "Kebakaran Hutan"]
print(f"\nHasil Prediksi Pemicu untuk Alert Baru: {nama_pemicu[prediksi[0]]}")