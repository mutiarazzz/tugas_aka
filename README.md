
# Analisis Kompleksitas Algoritma
## Penjumlahan Faktor Genap Menggunakan Metode Iteratif dan Rekursif

## 📝 Deskripsi
Program ini dibuat untuk menghitung jumlah faktor genap dari suatu bilangan
menggunakan dua pendekatan algoritma, yaitu:
1. Algoritma Iteratif
2. Algoritma Rekursif

Kedua algoritma dibandingkan dari sisi cara kerja dan waktu eksekusi
untuk melihat perbedaan efisiensi. 

Aplikasi ini dikembangkan menggunakan Python dan Streamlit. Hasil pengolahan ditampilkan secara visual dalam bentuk grafik sehingga perbedaan kinerja antara kedua pendekatan dapat diamati secara langsung.

## Definisi Faktor Genap
Faktor genap adalah bilangan genap yang dapat membagi habis suatu bilangan.

Contoh:
Jika n = 12  
Faktor genap = 2, 4, 6, 12  
Jumlah faktor genap = 24

## Fitur Utama
1. Perhitungan jumlah faktor genap menggunakan:
   - Algoritma Iteratif
   - Algoritma Rekursif
2. Pengukuran waktu eksekusi masing-masing algoritma
3. Perbandingan performa secara langsung
4. Visualisasi:
   - Grafik batang waktu eksekusi
   - Grafik garis tren kenaikan waktu terhadap nilai input
5. Tampilan daftar faktor genap yang ditemukan
6. Analisis kompleksitas waktu dan ruang

## ▶️ Cara Menjalankan Program
1. Pastikan Python sudah terpasang di komputer
2. Pasang library yang dibutuhkan: streamlit, pandas, matplotlib, dan plotly
3. Simpan file program dalam satu folder
4. Jalankan aplikasi menggunakan perintah Streamlit melalui terminal atau command prompt
5. Atur nilai input menggunakan slider yang tersedia pada tampilan aplikasi
6. Klik tombol Mulai Analisis untuk melihat hasil perhitungan dan grafik

## Algoritma yang Digunakan

### 1. Algoritma Iteratif
- Menggunakan perulangan dari 1 sampai n
- Kompleksitas waktu: O(n)
- Mengecek apakah bilangan merupakan faktor genap dan menjumlahkan faktor genap yang ditemukan
- Lebih efisien secara praktik

### 2. Algoritma Rekursif
- Menggunakan pemanggilan fungsi berulang
- Kompleksitas waktu: O(n)
- Melakukan pengecekan faktor genap hingga seluruh bilangan diperiksa
- Memiliki overhead pemanggilan fungsi dan keterbatasan stack memori

### Anggota
1. **Mutiara Zahra** (103052400010)
2. **Salwa Nabilah Nur Bahri** (103052400013)
3. **Nada Thahira Sosa** (103052400049)
