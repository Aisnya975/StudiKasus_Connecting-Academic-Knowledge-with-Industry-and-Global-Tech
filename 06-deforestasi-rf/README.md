# Klasifikasi Pemicu Deforestasi Berbasis Citra Satelit dan Machine Learning

Nama: Aisyah Azzahrah
NPM: G1A024033

## Latar Belakang
Peringatan dini deforestasi dari citra satelit umumnya hanya menunjukkan lokasi hilangnya tutupan pohon, tanpa menjelaskan aktivitas pemicunya. Proyek ini mengklasifikasikan pemicu deforestasi (pertanian, penebangan komersial, kebakaran hutan) dengan algoritma Random Forest.

## Alur Kerja
1. Preprocessing spektral : indeks NDVI dan NBR sebelum dan sesudah kerusakan
2. Ekstraksi fitur : perubahan spektral dan metrik spasial (ukuran patch, jarak ke jalan, elevasi)
3. Pemodelan : Random Forest Classifier
4. Evaluasi dan prediksi : Accuracy, Confusion Matrix, Classification Report, Feature Importance

## Struktur
- `src/deforestasi_rf.py` : kode utama
- `data/data_deforestasi.csv` : dataset simulasi

## Cara Menjalankan
```bash
pip install -r requirements.txt
python src/deforestasi_rf.py
```

## Keterbatasan
Dataset adalah simulasi dan labelnya dibuat dari aturan pada fitur yang sama, sehingga akurasi tinggi tidak mewakili performa pada data satelit nyata.