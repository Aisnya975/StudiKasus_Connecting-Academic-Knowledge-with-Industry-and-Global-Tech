import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


def proses_data_aset_spasial(file_csv_path):
    """Baca CSV koordinat, ubah jadi GeoDataFrame, dan hitung ringkasan."""
    print("Membaca data tabular aset dari sumber...")
    df = pd.read_csv(file_csv_path)

    if "latitude" not in df.columns or "longitude" not in df.columns:
        raise ValueError("Data harus memiliki kolom 'latitude' dan 'longitude'.")

    print("Mengonversi data tabular menjadi objek geometri spasial (Point)...")
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]

    # Sistem koordinat WGS84 (EPSG:4326)
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    print("\n--- RINGKASAN ANALISIS SPASIAL ASET ---")
    print(f"Total Aset Terpetakan : {len(gdf)} titik")
    if "kategori" in gdf.columns:
        print(f"Daftar Kategori Aset  : {list(gdf['kategori'].unique())}")
        ringkasan = gdf.groupby("kategori").size().reset_index(name="jumlah")
        ringkasan.to_csv("data/ringkasan_kategori.csv", index=False)
        print("\nJumlah per kategori:")
        print(ringkasan.to_string(index=False))

    minx, miny, maxx, maxy = gdf.total_bounds
    print(f"\nBatas wilayah (bounding box):")
    print(f"  Longitude : {minx:.6f} s/d {maxx:.6f}")
    print(f"  Latitude  : {miny:.6f} s/d {maxy:.6f}")

    output_geojson = "data/output_aset_terpetakan.geojson"
    gdf.to_file(output_geojson, driver="GeoJSON")
    print(f"\nBerhasil mengekspor data spasial ke: {output_geojson}")

    return gdf


if __name__ == "__main__":
    input_file = "data/data_aset_sample.csv"
    try:
        proses_data_aset_spasial(input_file)
    except Exception as e:
        print(f"Terjadi kesalahan saat memproses data: {e}")