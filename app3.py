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

# Custom CSS untuk UI yang lebih ramping dan fokus pada kecepatan
st.markdown("""
    <style>
    .speed-card {
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 5px;
    }
    .iteratif-bg { background: linear-gradient(135deg, #EC4899 0%, #F472B6 100%); }
    .rekursif-bg { background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%); }
    .card-label { font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .card-value { font-size: 1.6rem; font-weight: 800; }
    
    .sum-result-box {
        background-color: var(--background-secondary-color);
        border: 1px solid #444;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
    }
    .footer { text-align: center; color: gray; padding: 20px; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=60)
    st.title("Panel Kontrol")
    n_val = st.slider("Nilai N:", min_value=1, max_value=2000, value=500)
    st.divider()
    run_btn = st.button("🚀 MULAI ANALISIS", use_container_width=True)
    st.caption("Tugas Besar Analisis Kompleksitas Algoritma")

# --- KONTEN UTAMA ---
st.title("⚖️ Analisis Faktor Genap")

if run_btn:
    # 1. Eksekusi
    res_i, time_i, fact_i = sum_even_factors_iterative(n_val)
    res_r, time_r, fact_r, success_r = sum_even_factors_recursive(n_val)

    # 2. Highlight Hasil Penjumlahan (Dikecilkan & Digabung)
    st.markdown(f"""
        <div class="sum-result-box">
            <span style="color: gray;">Total Penjumlahan Faktor Genap (N={n_val}):</span><br>
            <b style="font-size: 1.5rem; color: #FF4B4B;">{res_i}</b>
        </div>
    """, unsafe_allow_html=True)

    # 3. Highlight Kecepatan (Fokus Utama Sekarang)
    st.write("### ⏱️ Perbandingan Kecepatan")
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        st.markdown(f"""<div class="speed-card rekursif-bg">
            <div class="card-label">WAKTU REKURSIF</div>
            <div class="card-value">{time_r:.6f} s</div>
        </div>""", unsafe_allow_html=True)
    with col_v2:
        st.markdown(f"""<div class="speed-card iteratif-bg">
            <div class="card-label">WAKTU ITERATIF</div>
            <div class="card-value">{time_i:.6f} s</div>
        </div>""", unsafe_allow_html=True)
    with col_v3:
        selisih = abs(time_i - time_r)
        st.metric("Selisih Efisiensi", f"{selisih:.8f} s")

    # 4. Grafik Bar (Original)
    st.divider()
    col_chart, col_detail = st.columns([3, 2])
    with col_chart:
        st.subheader("📊 Visualisasi Bar Kecepatan")
        if success_r:
            fig = go.Figure(data=[
                go.Bar(name='Iteratif', x=['Iteratif'], y=[time_i], marker_color='#EC4899', text=[f"{time_i:.5f}"], textposition='auto'),
                go.Bar(name='Rekursif', x=['Rekursif'], y=[time_r], marker_color='#3B82F6', text=[f"{time_r:.5f}"], textposition='auto')
            ])
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Rekursif mencapai batasan stack memori.")

    with col_detail:
        st.subheader("📋 Detail Data Faktor")
        st.write(f"Ditemukan **{len(fact_i)}** faktor genap.")
        with st.container(border=True):
            st.write(", ".join(map(str, sorted(fact_i))) if fact_i else "Tidak ada faktor genap")

    # 5. Grafik Garis & Tabel Kenaikan N (Analisis Tambahan)
    st.divider()
    st.subheader("📈 Trend Kenaikan Waktu Berdasarkan N")
    input_sizes = [10, 100, 250, 500, 750, 1000, 1500, 2000]
    history = []
    for size in input_sizes:
        _, t_i, _ = sum_even_factors_iterative(size)
        _, t_r, _, ok = sum_even_factors_recursive(size)
        history.append({"N": size, "Iteratif (s)": t_i, "Rekursif (s)": t_r if ok else None})
    
    df_perf = pd.DataFrame(history)
    c_line, c_table = st.columns([3, 2])
    with c_line:
        fig2, ax = plt.subplots(figsize=(10, 4.5))
        ax.plot(df_perf["N"], df_perf["Rekursif (s)"], marker='o', label='Rekursif', color='#3B82F6')
        ax.plot(df_perf["N"], df_perf["Iteratif (s)"], marker='o', label='Iteratif', color='#EC4899')
        ax.set_ylabel("Waktu (detik)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig2)
    with c_table:
        st.dataframe(df_perf.style.format({"Iteratif (s)": "{:.8f}", "Rekursif (s)": "{:.8f}"}), use_container_width=True)

    # 6. Tab Analisis
    st.divider()
    t1, t2 = st.tabs(["📝 Kesimpulan Analisis", "💻 Kode Algoritma"])
    with t1:
        pemenang = "Iteratif" if time_i < time_r else "Rekursif"
        st.success(f"Analisis Selesai: Metode **{pemenang}** lebih efisien untuk N = {n_val}.")
        
        st.write("#### 📊 Kelas Kompleksitas")
        st.table(pd.DataFrame({
            "Metode": ["Iteratif", "Rekursif"],
            "Time Complexity": ["O(n)", "O(n)"],
            "Space Complexity": ["O(1)", "O(n)"],
            "Stabilitas": ["Tinggi", "Terbatas (Stack Memory)"]
        }))
        st.info("Catatan: Secara teori Big O, keduanya adalah linear. Namun secara praktis, rekursif lebih lambat karena overhead pemanggilan fungsi.")

    with t2:
        st.code("""
# Iteratif (Looping)
for i in range(1, n + 1):
    if n % i == 0 and i % 2 == 0: total += i

# Rekursif (Self-Calling)
def logic(n, curr):
    if curr > n: return 0
    return logic + recursive(n, curr + 1)
        """, language="python")

else:
    col_a, col_b = st.columns(2)
    with col_a:
        st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-804.jpg")
    with col_b:
        st.write("### Selamat Datang!")
        st.write("Gunakan slider di samping untuk mengatur angka, lalu klik **Mulai Analisis**.")

st.markdown("<div class='footer'>Tugas Besar Analisis Kompleksitas Algoritma - 2024</div>", unsafe_allow_html=True)

