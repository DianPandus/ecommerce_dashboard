import pandas as pd
import streamlit as st
import requests
import plotly.express as px
from io import BytesIO
from babel.numbers import format_currency

# --- Konfigurasi Halaman & Judul Utama ---
# st.set_page_config untuk menggunakan layout 'wide' agar lebih lega.
st.set_page_config(layout="wide")
st.title('E-Commerce Dashboard: Analisis Kinerja Penjualan')

# --- Fungsi untuk Memuat Data ---
# @st.cache_data digunakan agar Streamlit tidak perlu mengunduh dan memproses ulang data setiap kali pengguna berinteraksi
# dengan filter. Ini secara drastis meningkatkan kecepatan aplikasi.
@st.cache_data
def load_data(url):
    """Mengunduh, membaca, dan memproses data dari Google Drive."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Akan error jika status code bukan 2xx
        data = pd.read_csv(BytesIO(response.content))
        # Konversi kolom tanggal ke tipe data datetime
        data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal mengunduh dataset: {e}")
        return None
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {e}")
        return None

# --- Memuat Data ---
# ID file dari Google Drive
file_id = "1gFSBGm9U_w6rrHvP3qnTnvnGT2Mwc1LP"
url = f"https://drive.google.com/uc?id={file_id}"
all_df = load_data(url)

# Jika data gagal dimuat, hentikan eksekusi aplikasi
if all_df is None:
    st.stop()

# --- Sidebar untuk Filter ---
with st.sidebar:
    st.header('Filter Data')
    # Filter tanggal
    start_date = st.date_input('Start Date', all_df['order_purchase_timestamp'].min().date())
    end_date = st.date_input('End Date', all_df['order_purchase_timestamp'].max().date())

    # Filter Kategori Produk
    # Menambahkan opsi 'Semua Kategori' untuk kemudahan
    all_categories = ['Semua Kategori'] + sorted(all_df['product_category_name'].unique().tolist())
    selected_category = st.selectbox('Pilih Kategori Produk', all_categories)

# --- Proses Filtering Data ---
# Konversi start_date dan end_date ke datetime untuk perbandingan
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date)

# Terapkan filter ke dataframe
filtered_df = all_df[
    (all_df['order_purchase_timestamp'] >= start_datetime) &
    (all_df['order_purchase_timestamp'] <= end_datetime + pd.Timedelta(days=1))
]

# Terapkan filter kategori jika bukan 'Semua Kategori'
if selected_category != 'Semua Kategori':
    filtered_df = filtered_df[filtered_df['product_category_name'] == selected_category]


# --- Menampilkan Metrik Utama ---
st.header('Ringkasan Kinerja')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = filtered_df['order_id'].nunique()
    st.metric("Total Pesanan", value=f"{total_orders:,}")

with col2:
    total_revenue = filtered_df['payment_value'].sum()
    st.metric("Total Pendapatan", value=format_currency(total_revenue, "BRL", locale='pt_BR'))

with col3:
    # Hindari division by zero jika tidak ada order
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    st.metric("Pendapatan Rata-Rata/Pesanan", value=format_currency(avg_order_value, "BRL", locale='pt_BR'))

st.markdown("---") # Garis pemisah

# --- Penggunaan Tabs untuk Organisasi Konten ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tren Penjualan",
    "📦 Analisis Produk",
    "👥 Analisis Pelanggan",
    "🚚 Analisis Pesanan & Pengiriman"
])

# --- Konten TAB 1: Tren Penjualan ---
with tab1:
    st.subheader("Tren Pendapatan Bulanan")
    filtered_df['order_purchase_month'] = filtered_df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    revenue_by_month = filtered_df.groupby('order_purchase_month')['payment_value'].sum().reset_index()

    fig = px.line(
        revenue_by_month,
        x='order_purchase_month',
        y='payment_value',
        title="Total Pendapatan per Bulan",
        labels={'order_purchase_month': 'Bulan', 'payment_value': 'Total Pendapatan'},
        markers=True
    )
    fig.update_layout(yaxis_tickprefix='R$ ')
    st.plotly_chart(fig, use_container_width=True)

# --- Konten TAB 2: Analisis Produk ---
with tab2:
    col_prod1, col_prod2 = st.columns(2)
    with col_prod1:
        st.subheader("Top 10 Kategori (Pendapatan)")
        category_revenue = filtered_df.groupby('product_category_name')['payment_value'].sum().nlargest(10).reset_index()
        fig = px.bar(
            category_revenue,
            x='payment_value',
            y='product_category_name',
            orientation='h',
            title="Top 10 Kategori Produk berdasarkan Pendapatan",
            labels={'product_category_name': 'Kategori Produk', 'payment_value': 'Total Pendapatan'}
        )
        fig.update_layout(xaxis_tickprefix='R$ ', yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col_prod2:
        st.subheader("Top 10 Kategori (Terlaris)")
        # Menggunakan .size() atau .count() lebih akurat untuk jumlah item terjual daripada .sum('order_item_id')
        sales_by_category = filtered_df.groupby('product_category_name').size().nlargest(10).reset_index(name='items_sold')
        fig = px.bar(
            sales_by_category,
            x='items_sold',
            y='product_category_name',
            orientation='h',
            title="Top 10 Kategori Produk berdasarkan Jumlah Terjual",
            labels={'product_category_name': 'Kategori Produk', 'items_sold': 'Jumlah Item Terjual'}
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

# --- Konten TAB 3: Analisis Pelanggan ---
with tab3:
    col_cust1, col_cust2 = st.columns(2)
    with col_cust1:
        st.subheader("Pelanggan per Negara Bagian")
        customer_by_state = filtered_df.groupby('customer_state')['customer_unique_id'].nunique().nlargest(10).reset_index()
        fig = px.bar(
            customer_by_state,
            x='customer_state',
            y='customer_unique_id',
            title="Top 10 Negara Bagian dengan Pelanggan Terbanyak",
            labels={'customer_state': 'Negara Bagian', 'customer_unique_id': 'Jumlah Pelanggan Unik'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_cust2:
        st.subheader("Pelanggan per Kota")
        customer_by_city = filtered_df.groupby('customer_city')['customer_unique_id'].nunique().nlargest(10).reset_index()
        fig = px.bar(
            customer_by_city,
            x='customer_city',
            y='customer_unique_id',
            title="Top 10 Kota dengan Pelanggan Terbanyak",
            labels={'customer_city': 'Kota', 'customer_unique_id': 'Jumlah Pelanggan Unik'}
        )
        st.plotly_chart(fig, use_container_width=True)

# --- Konten TAB 4: Analisis Pesanan & Pengiriman ---
with tab4:
    col_order1, col_order2 = st.columns(2)
    with col_order1:
        st.subheader("Distribusi Status Pesanan")
        order_status = filtered_df['order_status'].value_counts().reset_index()
        fig = px.pie(
            order_status,
            names='order_status',
            values='count',
            title="Proporsi Status Pesanan",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_order2:
        st.subheader("Distribusi Metode Pembayaran")
        payment_type = filtered_df['payment_type'].value_counts().reset_index()
        fig = px.pie(
            payment_type,
            names='payment_type',
            values='count',
            title="Proporsi Metode Pembayaran",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)


# --- Footer ---
st.markdown("---")
st.caption('Copyright © 2025 (Versi Disederhanakan)')