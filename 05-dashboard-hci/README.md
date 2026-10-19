# Dashboard Pemantauan Kualitas Air dan Produksi Pakan Ternak (HCI dan Visualisasi Data)

Nama: Aisyah Azzahrah
NPM: G1A024033

## Latar Belakang
Data produksi dan kualitas lingkungan sering dicatat dalam tabel angka mentah sehingga sulit dibaca cepat dan menimbulkan beban kognitif. Proyek ini merancang dashboard interaktif dengan prinsip Human-Computer Interaction dan visualisasi data.

## Prinsip HCI yang Diterapkan
- Reduksi beban kognitif: kartu metrik ringkas di bagian atas
- Hirarki visual dan warna: hijau untuk normal, oranye untuk di luar batas aman
- Umpan balik visual: garis ambang batas pH pada grafik
- Kontrol pengguna: filter rentang tanggal dan hover interaktif
- Progressive disclosure: data mentah disembunyikan dalam expander

## Tampilan
![Screenshot dashboard](screenshot.png)

## Struktur
- `src/app.py` : aplikasi dashboard Streamlit

## Cara Menjalankan
```bash
pip install -r requirements.txt
python -m streamlit run src/app.py
```

## Keterbatasan
Data pada dashboard adalah data simulasi, bukan hasil pengukuran nyata.