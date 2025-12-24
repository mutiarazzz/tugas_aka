import streamlit as st
import time
import matplotlib.pyplot as plt
import pandas as pd
import sys

# Menaikkan limit rekursi agar tidak cepat error pada angka besar
sys.setrecursionlimit(5000)

# --- FUNGSI ALGORITMA ---

def sum_even_iterative(n):
    start_time = time.perf_counter()
    total = 0
    for i in range(1, n + 1):
        if n % i == 0 and i % 2 == 0:
            total += i
    end_time = time.perf_counter()
    return total, end_time - start_time

def sum_even_recursive(n, current=1):
    # Fungsi pembungkus untuk menghitung waktu
    start_time = time.perf_counter()
    
    def logic(n, curr):
        if curr > n:
            return 0
        val = curr if (n % curr == 0 and curr % 2 == 0) else 0
        return val + logic(n, curr + 1)
    
    result = logic(n, current)
    end_time = time.perf_counter()
    return result, end_time - start_time

# --- TAMPILAN STREAMLIT ---

st.set_page_config(page_title="Analisis Algoritma", layout="wide")

st.title("⚖️ Perbandingan Algoritma: Faktor Genap")
st.write("Aplikasi ini membandingkan efisiensi antara metode **Iteratif** dan **Rekursif**.")

# Input User
n_input = st.number_input("Masukkan bilangan (n):", min_value=1, max_value=2500, value=500)

if st.button("Mulai Hitung"):
    # Jalankan kedua algoritma
    res_iter, time_iter = sum_even_iterative(n_input)
    
    # Rekursi bisa menyebabkan error jika n terlalu besar (Stack Overflow)
    try:
        res_rec, time_rec = sum_even_recursive(n_input)
        error_rec = False
    except RecursionError:
        error_rec = True

    # 1. Menampilkan Hasil Angka
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Metode Iteratif")
        st.success(f"Hasil: {res_iter}")
        st.info(f"Waktu: {time_iter:.8f} detik")

    with col2:
        st.subheader("Metode Rekursif")
        if error_rec:
            st.error("Rekursi Gagal! (Stack Overflow)")
        else:
            st.success(f"Hasil: {res_rec}")
            st.info(f"Waktu: {time_rec:.8f} detik")

    st.divider()

    # 2. Visualisasi Grafik Perbandingan
    if not error_rec:
        st.subheader("Grafik Kecepatan Eksekusi")
        
        data = pd.DataFrame({
            'Metode': ['Iteratif', 'Rekursif'],
            'Waktu (Detik)': [time_iter, time_rec]
        })
        
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#3498db', '#e67e22']
        ax.bar(data['Metode'], data['Waktu (Detik)'], color=colors)
        ax.set_ylabel('Waktu (detik)')
        st.pyplot(fig)

        # Penjelasan Teknis
        st.write("### Analisis Singkat:")
        st.write(f"""
        - Kedua algoritma memiliki kompleksitas waktu yang sama, yaitu $O(n)$.
        - Namun, secara praktis, **Iteratif** biasanya lebih cepat dan aman.
        - **Rekursif** menggunakan memori tambahan berupa *Call Stack*. Terbukti saat $n$ sangat besar, 
          rekursif akan mengalami *Stack Overflow* sedangkan iteratif tetap berjalan lancar.
        """)