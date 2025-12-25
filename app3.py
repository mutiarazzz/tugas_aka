import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import sys

# Menaikkan limit rekursi agar aman untuk angka besar
sys.setrecursionlimit(5000)

# --- FUNGSI ALGORITMA ---

def sum_even_factors_iterative(n):
    start_time = time.perf_counter()
    total = 0
    factors = []
    for i in range(1, n + 1):
        if n % i == 0 and i % 2 == 0:
            total += i
            factors.append(i)
    end_time = time.perf_counter()
    return total, end_time - start_time, factors

def sum_even_factors_recursive(n, current=1):
    # Fungsi pembungkus untuk menghitung waktu total
    start_time = time.perf_counter()
    
    def _logic(n, curr):
        if curr > n:
            return 0, []
        
        total_next, factors_next = _logic(n, curr + 1)
        
        if n % curr == 0 and curr % 2 == 0:
            return curr + total_next, [curr] + factors_next
        else:
            return total_next, factors_next
    
    res, facts = _logic(n, current)
    end_time = time.perf_counter()
    return res, end_time - start_time, facts

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Analisis Kompleksitas Algoritma", layout="wide")

# Custom CSS untuk tampilan premium (Perbaikan pada bagian ini)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #1f77b4; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 12px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Panel Kontrol")
    st.write("Gunakan slider untuk memilih angka.")
    n_val = st.slider("Nilai N:", min_value=1, max_value=2500, value=500)
    st.divider()
    run_btn = st.button("🚀 MULAI ANALISIS", use_container_width=True)
    st.write("---")
    st.caption("Tugas Mata Kuliah: Analisis Kompleksitas Algoritma")

# --- KONTEN UTAMA ---
st.title("⚖️ Analisis Faktor Genap")
st.markdown("Membandingkan efisiensi waktu antara metode **Iteratif** dan **Rekursif**.")

if run_btn:
    # 1. Eksekusi
    res_i, time_i, fact_i = sum_even_factors_iterative(n_val)
    
    try:
        res_r, time_r, fact_r = sum_even_factors_recursive(n_val)
        error_r = False
    except RecursionError:
        error_r = True

    # 2. Barisan Metrik (Kartu Hasil)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Penjumlahan", res_i)
    with m2:
        st.metric("Waktu Iteratif", f"{time_i:.6f} s")
    with m3:
        if not error_r:
            st.metric("Waktu Rekursif", f"{time_r:.6f} s")
        else:
            st.metric("Waktu Rekursif", "Limit Tercapai")

    st.write("###") # Spacer

    # 3. Grafik dan Detail
    col_chart, col_detail = st.columns([3, 2])

    with col_chart:
        st.subheader("📊 Grafik Kecepatan")
        if not error_r:
            fig = go.Figure(data=[
                go.Bar(name='Iteratif', x=['Iteratif'], y=[time_i], marker_color='#3498db', text=[f"{time_i:.5f}"], textposition='auto'),
                go.Bar(name='Rekursif', x=['Rekursif'], y=[time_r], marker_color='#e67e22', text=[f"{time_r:.5f}"], textposition='auto')
            ])
            fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Metode Rekursif mencapai batasan stack memori (Recursion Limit). Gunakan angka di bawah 2000.")

    with col_detail:
        st.subheader("📋 Detail Data")
        st.write(f"Ditemukan **{len(fact_i)}** faktor genap dari angka **{n_val}**.")
        with st.container(border=True):
            st.write(", ".join(map(str, sorted(fact_i))) if fact_i else "Tidak ada faktor genap")

    # 4. Tab Analisis
    st.divider()
    t1, t2 = st.tabs(["📝 Kesimpulan Analisis", "💻 Kode Algoritma"])
    
    with t1:
        st.markdown(f"""
        ### Kenapa ada perbedaan waktu?
        1. **Iteratif ($O(n)$)**: Hanya menggunakan satu jalur proses (*looping*). Sangat stabil untuk angka besar.
        2. **Rekursif ($O(n)$)**: Memanggil dirinya sendiri berulang kali. Setiap panggilan disimpan dalam **Stack Memori**. 
        
        **Hasil Percobaan:**
        Pada $n = {n_val}$, metode **{'Iteratif' if time_i < (time_r if not error_r else 999) else 'Rekursif'}** tercatat lebih cepat sebanyak **{abs(time_i - (time_r if not error_r else 0)):.6f} detik**.
        """)
    
    with t2:
        st.code("""
# Versi Iteratif
for i in range(1, n + 1):
    if n % i == 0 and i % 2 == 0:
        total += i
        
# Versi Rekursif
def logic(n, curr):
    if curr > n: return 0
    # ... call logic(n, curr + 1)
        """, language="python")

else:
    # Tampilan awal saat belum klik tombol
    st.empty()
    col_a, col_b = st.columns(2)
    with col_a:
        st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-804.jpg")
    with col_b:
        st.write("### Selamat Datang!")
        st.write("Pilih angka pada slider di samping dan klik tombol **Mulai Analisis** untuk melihat bagaimana algoritma bekerja di balik layar.")

st.markdown("<div class='footer'>Tugas Besar Analisis Kompleksitas Algoritma - 2024</div>", unsafe_allow_html=True)