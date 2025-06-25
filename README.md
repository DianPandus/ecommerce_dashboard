# Analisis Data E-Commerce Brasil: Interactive Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.43-ff4b4b.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2-blueviolet.svg)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Proyek ini menyajikan analisis mendalam terhadap **Olist E-Commerce Dataset**, sebuah dataset publik berisi data transaksi dari sebuah marketplace di Brasil. Seluruh proses, mulai dari pembersihan data, analisis eksplorasi, hingga visualisasi, dirangkum dalam sebuah dashboard interaktif yang dibangun menggunakan Streamlit.

## 🚀 Live Dashboard

Anda dapat mengakses dan berinteraksi langsung dengan dashboard melalui link berikut:

**[[https://dashboard-ecommerce-dianps.streamlit.app/](https://ecommerce-dashboards.streamlit.app/)**

## 🎯 Latar Belakang & Tujuan

Tujuan utama dari proyek ini adalah untuk menjawab pertanyaan-pertanyaan bisnis kunci yang dapat membantu pengambilan keputusan strategis bagi platform e-commerce. Analisis ini berfokus pada pemahaman perilaku pelanggan, performa produk, dan tren penjualan.

### Pertanyaan Bisnis yang Dijawab:

1.  Kategori produk apa yang paling laris dan yang menghasilkan pendapatan tertinggi?
2.  Bagaimana tren penjualan dari waktu ke waktu? Apakah ada pola musiman?
3.  Wilayah (kota/negara bagian) mana yang memiliki jumlah pelanggan terbanyak?
4.  Metode pembayaran apa yang paling sering digunakan oleh pelanggan?
5.  Bagaimana demografi pelanggan berdasarkan lokasi geografis?

## ✨ Fitur Dashboard

- **Visualisasi Interaktif**: Grafik dan plot yang dapat difilter sesuai kebutuhan.
- **Analisis Tren Penjualan**: Melihat performa penjualan harian, mingguan, dan bulanan.
- **Analisis Kategori Produk**: Menampilkan kategori produk terlaris dan paling menguntungkan.
- **Analisis Geospasial**: Peta interaktif yang menunjukkan persebaran pelanggan di seluruh Brasil.
- **Ringkasan Metrik Utama**: Tampilan metrik-metrik penting secara ringkas dan jelas.

## 🛠️ Teknologi yang Digunakan

- **Analisis & Manipulasi Data**: `pandas`, `numpy`
- **Visualisasi Data**: `matplotlib`, `seaborn`
- **Dashboard Interaktif**: `streamlit`
- **Analisis Geospasial**: `geopandas`, `folium`

## ⚙️ Cara Menjalankan Proyek Secara Lokal

### 1. Prasyarat

- Python 3.10 atau lebih baru
- Git

### 2. Instalasi

1.  Clone repositori ini ke mesin lokal Anda:

    ```bash
    git clone [https://github.com/DianPandus/ecommerce_dashboard.git](https://github.com/DianPandus/ecommerce_dashboard.git)
    cd nama-repo-anda
    ```

2.  Buat dan aktifkan _virtual environment_ (sangat disarankan):

    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Instal semua pustaka yang diperlukan dari file `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    _Catatan: File `requirements.txt` Anda sudah mencakup semua pustaka utama._

### 3. Menjalankan Dashboard

Setelah instalasi selesai, jalankan aplikasi Streamlit dengan perintah berikut di terminal:

```bash
streamlit run dashboard.py
```

## 📁 Struktur Repositori

```
data/
.
├── 📊 data/
│   └── olist_customers_dataset.csv
├── 📊 dashboard/
│   └── dashboard.py      # Script utama untuk aplikasi Streamlit
├── 📓 Proyek_Analisis_Data.ipynb # Notebook untuk analisis data eksplorasi
├── 📄 requirements.txt          # Daftar pustaka yang dibutuhkan
└── 📜 README.md                 # File yang sedang Anda baca
```
