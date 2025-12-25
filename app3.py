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

# Custom CSS untuk UI Premium dan teks hasil yang dipertegas
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
    .card-label { font-size: 0.9rem; font-weight: 700; text-transform: uppercase; }
    .card-value { font-size: 1.6rem; font-weight: 800; }
    
    /* Perbaikan Kotak Hasil agar lebih jelas dan teks tebal */
    .sum-result-box {
        background-color: rgba(151, 166, 195, 0.1);
        border: 2px solid #FF4B4B;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
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

    # 2. Kotak Hasil Penjumlahan (Teks Sebesar 'Perbandingan Kecepatan' & Bold)
    st.markdown(f"""
        <div class="sum-result-box">
            <h3 style="margin:0; font-weight: 900; color: var(--text-color); text-transform: uppercase; letter-spacing: 1px;">
                TOTAL PENJUMLAHAN FAKTOR GENAP (N={n_val}): 
                <span style="color: #FF4B4B;">{res_i}</span>
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # 3. Perbandingan Kecepatan (Highlight Utama)
    st.write("### ⏱️ Perbandingan Kecepatan")
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        st.markdown(f"""<div class="speed-card rekursif-bg">
            <div class="card-label">WAKTU REKURSIF</div>
            <div class="card-value">{time_r:.6f} s</div>
        </div>""", unsafe_allow_html=True)
    with col_v2:
