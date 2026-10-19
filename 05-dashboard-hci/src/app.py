import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------
# KONFIGURASI HALAMAN (HCI: aksesibilitas dan tata letak)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Monitor Produksi & Kualitas",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Monitoring Ekosistem Produksi & Kualitas Lingkungan")
st.caption("Implementasi antarmuka interaktif berbasis Human-Computer Interaction (HCI)")

# ---------------------------------------------------------
# SIMULASI DATA
# ---------------------------------------------------------
BATAS_BAWAH_PH = 6.5
BATAS_ATAS_PH = 7.5

np.random.seed(42)
dates = pd.date_range(start="2026-01-01", periods=30, freq="D")
data = pd.DataFrame(
    {
        "Tanggal": dates,
        "Produksi_Pakan_Ton": np.random.normal(loc=12, scale=2, size=30).round(1),
        "pH_Air": np.random.uniform(low=6.2, high=8.1, size=30).round(2),
        "Suhu_Lingkungan_C": np.random.uniform(low=25.0, high=32.0, size=30).round(1),
    }
)
data["Status_pH"] = np.where(
    data["pH_Air"].between(BATAS_BAWAH_PH, BATAS_ATAS_PH), "Normal", "Di luar batas"
)

# ---------------------------------------------------------
# SIDEBAR: filter rentang tanggal (HCI: kontrol pengguna)
# ---------------------------------------------------------
st.sidebar.header("Filter Data")
rentang = st.sidebar.date_input(
    "Rentang tanggal",
    value=(dates.min().date(), dates.max().date()),
    min_value=dates.min().date(),
    max_value=dates.max().date(),
)
if len(rentang) == 2:
    mulai, akhir = pd.to_datetime(rentang[0]), pd.to_datetime(rentang[1])
    data = data[(data["Tanggal"] >= mulai) & (data["Tanggal"] <= akhir)]

if data.empty:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
    st.stop()

# ---------------------------------------------------------
# METRIK UTAMA (HCI: reduksi beban kognitif)
# ---------------------------------------------------------
total_produksi = data["Produksi_Pakan_Ton"].sum()
rata_ph = data["pH_Air"].mean()
rata_suhu = data["Suhu_Lingkungan_C"].mean()
hari_ph_buruk = int((data["Status_pH"] == "Di luar batas").sum())

# Perubahan: paruh kedua dibanding paruh pertama dari data yang tampil
setengah = len(data) // 2
delta_produksi = None
delta_suhu = None
if setengah > 0:
    awal = data.iloc[:setengah]
    akhir_ = data.iloc[setengah:]
    prod_awal = awal["Produksi_Pakan_Ton"].sum()
    if prod_awal != 0:
        persen = (akhir_["Produksi_Pakan_Ton"].sum() - prod_awal) / prod_awal * 100
        delta_produksi = f"{persen:+.1f}% vs paruh pertama"
    selisih_suhu = akhir_["Suhu_Lingkungan_C"].mean() - awal["Suhu_Lingkungan_C"].mean()
    delta_suhu = f"{selisih_suhu:+.1f} °C vs paruh pertama"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Produksi Pakan", f"{total_produksi:.1f} Ton", delta=delta_produksi)

with col2:
    st.metric(
        "Rata-Rata pH Air",
        f"{rata_ph:.2f}",
        delta=f"{hari_ph_buruk} hari di luar batas aman",
        delta_color="off",
    )

with col3:
    st.metric(
        "Rata-Rata Suhu",
        f"{rata_suhu:.1f} °C",
        delta=delta_suhu,
        delta_color="inverse",
    )

st.divider()

# ---------------------------------------------------------
# VISUALISASI DATA INTERAKTIF (HCI: hirarki visual)
# ---------------------------------------------------------
left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("📈 Tren Produksi Pakan Harian")
    fig_prod = px.line(
        data,
        x="Tanggal",
        y="Produksi_Pakan_Ton",
        markers=True,
        labels={"Produksi_Pakan_Ton": "Produksi (Ton)", "Tanggal": "Tanggal"},
        color_discrete_sequence=["#1f77b4"],
    )
    fig_prod.update_layout(hovermode="x unified")
    st.plotly_chart(fig_prod, use_container_width=True)

with right_chart:
    st.subheader(f"🧪 Pemantauan pH Air (Batas Aman {BATAS_BAWAH_PH} - {BATAS_ATAS_PH})")
    fig_ph = px.scatter(
        data,
        x="Tanggal",
        y="pH_Air",
        color="Status_pH",
        color_discrete_map={"Normal": "#2ca02c", "Di luar batas": "#ff7f0e"},
        labels={"pH_Air": "Tingkat pH", "Tanggal": "Tanggal", "Status_pH": "Status"},
    )
    fig_ph.add_hline(
        y=BATAS_BAWAH_PH, line_dash="dash", line_color="gray", annotation_text="Batas Bawah"
    )
    fig_ph.add_hline(
        y=BATAS_ATAS_PH, line_dash="dash", line_color="gray", annotation_text="Batas Atas"
    )
    st.plotly_chart(fig_ph, use_container_width=True)

# ---------------------------------------------------------
# DATA MENTAH (HCI: progressive disclosure)
# ---------------------------------------------------------
with st.expander("🔍 Lihat Detail Data Mentah"):
    st.dataframe(data, use_container_width=True)