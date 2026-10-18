# Pemodelan Prakiraan Polusi Udara (PM 2.5) Berbasis Parallel Computing

Nama: Aisyah Azzahrah
NPM: G1A024033

## Latar Belakang
Pemodelan kualitas udara membutuhkan komputasi besar karena volume data sensor yang banyak. Proyek ini memakai pemrosesan paralel (multiprocessing) untuk mempercepat perhitungan dan membandingkan waktu eksekusi pada jumlah worker berbeda.

## Struktur
- `src/parallel_processing.py` : pemrosesan paralel + benchmark 1, 2, 4 worker
- `src/visualize.py` : grafik waktu dan speedup
- `jobs/hpc_job.sh` : script Slurm untuk HPC cluster
- `data/` : sampel data dan hasil benchmark

## Cara Menjalankan
```bash
pip install -r requirements.txt
python src/parallel_processing.py
python src/visualize.py
```

## Hasil
Isi dengan tabel dari `data/benchmark.csv` dan tempel gambar `data/benchmark.png`, lalu tulis analisis singkatnya.