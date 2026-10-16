import os
import time
from multiprocessing import Pool

import numpy as np
import pandas as pd


def process_sensor_chunk(data_chunk):
    """Simulasi kalkulasi beban berat per chunk data sensor PM2.5."""
    results = []
    for val in data_chunk:
        calc = np.sin(val) ** 2 + np.cos(val) ** 2 + (val * 1.05)
        results.append(calc)
    return results


def run_with_workers(data, num_workers):
    """Jalankan pemrosesan dengan num_workers proses, kembalikan hasil & waktu."""
    chunks = np.array_split(data, num_workers)
    start = time.time()
    if num_workers == 1:
        results = [process_sensor_chunk(chunks[0])]  # serial
    else:
        with Pool(processes=num_workers) as pool:
            results = pool.map(process_sensor_chunk, chunks)
    final = np.concatenate(results)
    return final, time.time() - start


def main():
    print("=== PIPELINE PEMROSESAN PM2.5 BERBASIS PARALEL (HPC) ===")

    np.random.seed(42)
    n_samples = 1_000_000
    raw_data = np.random.uniform(low=10.0, high=150.0, size=n_samples)

    os.makedirs("data", exist_ok=True)
    pd.DataFrame({"pm25": raw_data[:1000]}).to_csv("data/pm25_sample.csv", index=False)

    max_cpu = os.cpu_count()
    print(f"Jumlah core tersedia : {max_cpu}")
    print(f"Total data           : {n_samples} sampel\n")

    worker_options = [w for w in (1, 2, 4, 8) if w <= max_cpu]
    rows = []
    base_time = None

    for w in worker_options:
        final, elapsed = run_with_workers(raw_data, w)
        if w == 1:
            base_time = elapsed
        speedup = base_time / elapsed
        efficiency = speedup / w
        rows.append(
            {
                "workers": w,
                "time_sec": round(elapsed, 4),
                "speedup": round(speedup, 2),
                "efficiency": round(efficiency, 2),
            }
        )
        print(
            f"Worker: {w} | Waktu: {elapsed:.4f} dtk | "
            f"Speedup: {speedup:.2f}x | Efisiensi: {efficiency:.2f}"
        )

    pd.DataFrame(rows).to_csv("data/benchmark.csv", index=False)
    print("\nHasil benchmark disimpan ke data/benchmark.csv")


if __name__ == "__main__":
    main()