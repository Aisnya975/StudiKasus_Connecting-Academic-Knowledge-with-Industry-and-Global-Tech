import matplotlib

matplotlib.use("Agg")  # supaya jalan juga di server tanpa layar
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/benchmark.csv")

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].plot(df["workers"], df["time_sec"], marker="o")
axes[0].set_title("Waktu Eksekusi vs Jumlah Worker")
axes[0].set_xlabel("Jumlah Worker")
axes[0].set_ylabel("Waktu (detik)")
axes[0].grid(True)

axes[1].plot(df["workers"], df["speedup"], marker="o", label="Speedup aktual")
axes[1].plot(df["workers"], df["workers"], "--", label="Speedup ideal")
axes[1].set_title("Speedup vs Jumlah Worker")
axes[1].set_xlabel("Jumlah Worker")
axes[1].set_ylabel("Speedup (x)")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig("data/benchmark.png", dpi=150)
print("Grafik disimpan ke data/benchmark.png")