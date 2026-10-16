# Otomatisasi Ekstraksi Data Spasial dan Analisis Titik Koordinat dengan Python

Nama: Aisyah Azzahrah
NPM: G1A024033

## Latar Belakang
Pengelolaan data geospasial secara manual tidak efisien. Proyek ini mengotomatisasi pembacaan data koordinat aset fasilitas publik, mengubahnya menjadi data spasial dengan GeoPandas, dan mengekspor ringkasan secara otomatis memakai pustaka open-source.

## Struktur
- `src/gis_processor.py` : pemrosesan data spasial
- `data/data_aset_sample.csv` : data input (nama_aset, kategori, latitude, longitude)
- `data/output_aset_terpetakan.geojson` : hasil ekspor GeoJSON
- `data/ringkasan_kategori.csv` : jumlah aset per kategori

## Cara Menjalankan
```bash
pip install -r requirements.txt
python src/gis_processor.py
```