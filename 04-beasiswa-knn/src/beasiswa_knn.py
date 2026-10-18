import os

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

# 1. Simulasi Data Historis (Dataset)
data = {
    "IPK": [3.85, 2.70, 3.50, 2.90, 3.90, 2.65, 3.75, 2.80],
    "Pendapatan_Ortu_Juta": [2.5, 8.0, 3.0, 7.5, 2.0, 9.0, 3.5, 6.0],
    "Skor_Organisasi": [85, 40, 70, 30, 90, 20, 80, 50],
    "Status_Beasiswa": [1, 0, 1, 0, 1, 0, 1, 0],  # 1 = Layak, 0 = Tidak Layak
}

df = pd.DataFrame(data)

os.makedirs("data", exist_ok=True)
df.to_csv("data/data_beasiswa.csv", index=False)

# 2. Pemisahan Fitur (X) dan Target (y)
X = df[["IPK", "Pendapatan_Ortu_Juta", "Skor_Organisasi"]]
y = df["Status_Beasiswa"]

# 3. Bagi data latih dan data uji (stratify agar kedua kelas ada di data uji)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 4. Preprocessing: normalisasi fitur dengan StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Pelatihan model K-Nearest Neighbors
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train_scaled, y_train)

# 6. Evaluasi model
y_pred = model.predict(X_test_scaled)

print("--- HASIL EVALUASI MODEL ---")
print(f"Akurasi Model: {accuracy_score(y_test, y_pred) * 100:.1f}%")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=[0, 1]))
print("\nLaporan Klasifikasi:")
print(
    classification_report(
        y_test,
        y_pred,
        labels=[0, 1],
        target_names=["Tidak Layak", "Layak"],
        zero_division=0,
    )
)

# 7. Prediksi untuk mahasiswa baru
# Format: [IPK, Pendapatan Ortu (Juta), Skor Organisasi]
data_mahasiswa_baru = pd.DataFrame(
    [[3.60, 3.0, 75]], columns=["IPK", "Pendapatan_Ortu_Juta", "Skor_Organisasi"]
)
data_baru_scaled = scaler.transform(data_mahasiswa_baru)
prediksi_status = model.predict(data_baru_scaled)

hasil = (
    "Layak Menerima Beasiswa"
    if prediksi_status[0] == 1
    else "Tidak Layak Menerima Beasiswa"
)
print(f"\nPrediksi untuk mahasiswa baru: {hasil}")