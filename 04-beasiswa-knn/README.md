# Prediksi Kelayakan Beasiswa Mahasiswa dengan Machine Learning

Nama: Aisyah Azzahrah
NPM: G1A024033

## Latar Belakang
Perguruan tinggi ingin mengotomatisasi seleksi beasiswa prestasi agar lebih transparan dan objektif. Model dilatih dari data historis pendaftar (IPK, pendapatan orang tua, skor organisasi) memakai Supervised Learning (klasifikasi) dengan algoritma K-Nearest Neighbors.

## Workflow
1. Data Collection : data historis mahasiswa
2. Preprocessing : normalisasi fitur dengan StandardScaler
3. Training : K-Nearest Neighbors (k = 3)
4. Evaluation : Accuracy, Confusion Matrix, Classification Report

## Struktur
- `src/beasiswa_knn.py` : kode utama
- `data/data_beasiswa.csv` : dataset simulasi

## Cara Menjalankan
```bash
pip install -r requirements.txt
python src/beasiswa_knn.py
```

## Keterbatasan
Dataset hanya 8 sampel (simulasi), sehingga hasil evaluasi tidak mewakili performa di data nyata.