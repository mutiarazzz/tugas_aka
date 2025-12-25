import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import sys
import matplotlib.pyplot as plt

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
    def _logic(n, curr):
        if curr > n:
            return 0, []
        total_next, factors_next = _logic(n, curr + 1)
        if n % curr == 0 and curr % 2 == 0:
            return curr + total_next, [curr] + factors_next
        else:
            return total_next, factors_next
    
    start_time = time.perf_counter()
    try:
        res, facts = _logic(n, current)
        success = True
    except RecursionError:
        res, facts = 0, []
        success = False
    end_time = time.perf_counter()
    return res, end_time - start_time, facts, success

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Analisis Kompleksitas Algoritma", layout="wide")

# Custom CSS untuk Box Hasil Berwarna
st.markdown("""
    <style>
    .result-card {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 10px;
    }
    .iteratif-card { background: linear-gradient(135deg, #EC4899 0%, #F472B6 100%); border: 2px solid #F472B6; }
    .rekursif-card { background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%); border: 2px solid #60A5FA; }
    .card-label { font-size: 1.1rem; font-weight: 700; margin-bottom: 5px; opacity: 0.9; }
    .card-value { font-size: 2.2rem; font-weight: 800; }
    
    [data-testid="stMetric"] {
        background-color: var(--background-secondary-color);
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Panel Kontrol")
    n_val = st.slider("Nilai N:", min_value=1, max_value=2000, value=500)
    st.divider()
    run_btn = st.button("🚀 MULAI ANALISIS", use_container_width=True)
    st.caption("Tugas Mata Kuliah: Analisis Kompleksitas Algoritma")

# --- KONTEN UTAMA ---
st.title("⚖️ Analisis Faktor Genap")

if run_btn:
    # 1. Eksekusi Perhitungan Utama
    res_i, time_i, fact_i = sum_even_factors_iterative(n_val)
    res_r, time_r, fact_r, success_r = sum_even_factors_recursive(n_val)

    # 2. Tampilan Hasil Penjumlahan (Berwarna)
    st.write("### 🏁 Hasil Penjumlahan")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""<div class="result-card rekursif-card">
            <div class="card-label">HASIL REKURSIF</div>
            <div class="card-value">{res_r if success_r else 'Error'}</div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""<div class="result-card iteratif-card">
            <div class="card-label">HASIL ITERATIF</div>
            <div class="card-value">{res_i}</div>
        </div>""", unsafe_allow_html=True)

    # 3. Metrik Waktu Eksekusi
    st.write("### ⏱️ Waktu Eksekusi")
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Waktu Iteratif", f"{time_i:.6f} s")
    with m2: st.metric("Waktu Rekursif", f"{time_r:.6f} s" if success_r else "Limit Tercapai")
    with m3: st.metric("Selisih Waktu", f"{abs(time_i - time_r):.8f} s")

    # 4. Grafik Garis Kenaikan (Analisis N)
    st.divider()
    st.subheader("📈 Grafik Kenaikan Waktu (N)")
    
    input_sizes = [10, 50, 100, 250, 500, 750, 1000, 1500]
    data_points = []
    for size in input_sizes:
        _, t_i, _ = sum_even_factors_iterative(size)
        _, t_r, _, ok = sum_even_factors_recursive(size)
        data_points.append({
            "N": size, 
            "Iteratif (s)": t_i, 
            "Rekursif (s)": t_r if ok else None
        })
    
    df_perf = pd.DataFrame(data_points)
    
    col_g1, col_g2 = st.columns([3, 2])
    with col_g1:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df_perf["N"], df_perf["Rekursif (s)"], marker='o', label='Rekursif', color='#3B82F6')
        ax.plot(df_perf["N"], df_perf["Iteratif (s)"], marker='o', label='Iteratif', color='#EC4899')
        ax.set_xlabel("Nilai N")
        ax.set_ylabel("Waktu (detik)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col_g2:
        st.write("#### 📋 Tabel Kenaikan N")
        st.dataframe(df_perf.style.format({
            "Iteratif (s)": "{:.8f}",
            "Rekursif (s)": "{:.8f}"
        }), use_container_width=True)

    # 5. Detail Data
    st.divider()
    st.subheader("📋 Detail Faktor Genap")
    st.write(f"Ditemukan **{len(fact_i)}** faktor genap dari angka **{n_val}**.")
    st.info(", ".join(map(str, sorted(fact_i))) if fact_i else "Tidak ada faktor genap")

    # 6. Tab Analisis & Kode
    st.divider()
    t1, t2 = st.tabs(["📝 Kesimpulan Analisis", "💻 Kode Algoritma"])
    
    with t1:
        pemenang = "Iteratif" if time_i < time_r else "Rekursif"
        st.markdown(f"""
        <div style="background-color: rgba(151,166,195,0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B;">
            <h4 style="margin-top:0;">1. Mana yang Lebih Cepat?</h4>
            <p>Pada nilai N = <b>{n_val}</b>, metode <b>{pemenang}</b> lebih unggul.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("#### 📊 Kelas Kompleksitas")
        df_comp = pd.DataFrame({
            "Aspek": ["Time Complexity", "Space Complexity", "Efisiensi"],
            "Iteratif": ["O(n)", "O(1)", "Sangat Tinggi"],
            "Rekursif": ["O(n)", "O(n)", "Rendah (Stack Overhead)"]
        })
        st.table(df_comp)
    
    with t2:
        st.code("""
# Algoritma Iteratif
total = 0
for i in range(1, n + 1):
    if n % i == 0 and i % 2 == 0:
        total += i

# Algoritma Rekursif
def logic(n, curr):
    if curr > n: return 0
    # pemanggilan rekursif memakan stack memori
    return current + logic(n, curr + 1)
        """, language="python")

else:
    st.info("Pilih angka di sidebar dan klik **MULAI ANALISIS** untuk melihat performa.")

st.markdown("<div style='text-align: center; color: gray; padding: 20px;'>Tugas Besar Analisis Kompleksitas Algoritma © 2024</div>", unsafe_allow_html=True)
