# Prediksi Sisa Umur Pakai Motor Induksi · Tim 18

**Kasus:** 03 · Sisa Umur Pakai Motor Induksi (*remaining useful life*) · **Aplikasi:** https://mkb-ml-rul-motor-kvcysaqh7qyl6dki4yev6r.streamlit.app · **Video:** https://drive.google.com/drive/folders/1IgYoyeTorniR6fCVPjuGvqUHXS7AJ5J7?usp=sharing

| Anggota | NIM | Bagian yang dikerjakan |
|---|---|---|
| Dicky Pinusa Prima S | 2410015 | EDA, pembersihan data, API, dokumentasi dan laporan|
| Daffa Jiyadi Santoso | 2405250 | Model, evaluasi, dokumentasi dan laporan|

## Masalah dan pengguna

Klien adalah manajer pemeliharaan grup pabrik di tiga lokasi (Cikarang, Karawang, Purwakarta) dengan ratusan motor pompa dan konveyor. Pengiriman motor pengganti memakan waktu 2–4 minggu, sehingga perencana pemeliharaan perlu tahu berapa hari lagi sebuah motor masih bekerja agar pesanan dapat dibuat sebelum motor rusak. Model memprediksi sisa umur (dalam hari) dari tipe motor dan pembacaan sensor, lalu aplikasi menampilkan status **AMAN**, **PESAN PENGGANTI SEKARANG**, atau **SEGERA GANTI**.

## Data dan pembersihan

Data mentah `raw.csv` berisi 79.652 baris dari 300 motor yang dipantau harian sampai rusak (*run-to-failure*). Setelah dibersihkan tersisa 79.159 baris dengan tepat 300 motor.

| Masalah yang ditemukan | Jumlah baris | Cara menangani |
|---|---|---|
| `motor_id` tidak seragam (spasi, huruf kecil, tanpa tanda hubung) sehingga tampak 1.147 motor | 3.185 | dirapikan menjadi format `M-###`, hasilnya 300 motor |
| Ejaan `tipe_motor` beragam (`22KW`, `11 kW`, `5,5 kW`) | 1.588 | disamakan menjadi `5.5kW`, `11kW`, `22kW` |
| `tipe_motor` tertukar pada sebagian baris (satu motor tidak mungkin berganti tipe) | 1.045 | dipakai tipe yang paling sering muncul pada motor itu |
| Baris duplikat | 493 | dihapus dengan `drop_duplicates()` |
| Satuan suhu campur: nilai 316–372 adalah Kelvin | 25.355 | nilai > 150 dikurangi 273,15 menjadi °C |
| `arus_A` kosong | 1.602 | diinterpolasi dari data motor yang sama |
| `suhu_belitan_C` kosong | 794 | diinterpolasi dari data motor yang sama |
| `getaran_rms_mm_s` bernilai -1 (kode galat sensor) | 241 | dijadikan kosong, lalu diinterpolasi dari motor yang sama |
| `beban_pct` di atas 100% (maksimum 110%) | 797 | dipertahankan, masih mungkin terjadi (beban lebih) |

Pembagian data dilakukan **per `motor_id`** (180 motor *train*, 60 *validation*, 60 *test*) sehingga tidak ada motor yang muncul di dua bagian.

## Hasil

Metrik utama: MAE (hari) pada baris dengan `rul_hari` ≤ 60, karena motor yang hampir rusak menentukan kapan motor baru harus dipesan.

| Model | MAE ≤ 60 *validation* | MAE ≤ 60 *test* |
|---|---|---|
| *Baseline*: regresi linear (fitur sensor asli) | 29,88 | 30,46 |
| Gradient boosting (`loss='absolute_error'`, + `hari_operasi`) | 9,22 | **8,77** |

| Model | MAE semua baris *validation* | MAE semua baris *test* |
|---|---|---|
| *Baseline*: regresi linear | 47,36 | 54,90 |
| Gradient boosting | 40,13 | 48,66 |

Ambang status yang dipakai: **≤ 14 hari = SEGERA GANTI**, **≤ 45 hari = PESAN PENGGANTI SEKARANG**, selebihnya **AMAN**. Alasannya: pengiriman motor memakan 14–28 hari, jadi motor dengan sisa umur ≤ 14 hari sudah tidak sempat dipesan, sedangkan 45 hari adalah pengiriman terlama (28 hari) ditambah cadangan sekitar dua kali MAE model.

## Cara menjalankan

```bash
pip install -r requirements.txt
streamlit run app.py
```

Aplikasi Streamlit memuat `models/model.joblib` secara langsung (tanpa API terpisah). Untuk mengulang pelatihan, jalankan *notebook* dari atas sampai bawah. Model dilatih dengan scikit-learn 1.6.1.

## Struktur repositori

```
*.ipynb              notebook dari EDA sampai penyimpanan model
data/                raw.csv (data mentah) dan clean.csv (data bersih)
src/features.py      fungsi pembersihan, pembuat fitur, dan aturan status,
                     dipakai saat pelatihan dan saat prediksi
models/              model.joblib + metadata.json
app.py               aplikasi Streamlit
requirements.txt     daftar library
```

## Keterbatasan

- Data bersifat sintetis dan hanya mencakup tiga tipe motor (5.5 kW, 11 kW, 22 kW) di tiga lokasi pabrik.
- Motor yang masih sehat sulit diprediksi: getaran dan suhu baru berubah jelas pada sekitar 100 hari terakhir, sehingga MAE untuk sisa umur panjang tetap besar (MAE semua baris 48,66 hari pada *test*).
- Model memakai pembacaan satu hari dan `hari_operasi`; tidak memakai riwayat beberapa hari terakhir.
- Pengguna harus mengetahui `hari_operasi` (lama motor sudah beroperasi sejak dipasang).
- Nilai di luar rentang data latih membuat prediksi kurang dapat diandalkan; aplikasi menampilkan peringatan untuk kasus ini dan menolak masukan yang mustahil.
- Ambang 14 dan 45 hari adalah asumsi berdasarkan waktu pengiriman pada *brief* dan perlu disesuaikan dengan kondisi pabrik.

## Daftar periksa sebelum dikumpulkan

- [ ] Repositori bersifat publik dan setiap anggota memiliki *commit*
- [ ] *Notebook* dapat dijalankan ulang dari awal sampai akhir tanpa galat
- [ ] *Baseline* wajib dilaporkan dan dibandingkan
- [ ] Data *test* hanya dibuka satu kali, di akhir
- [ ] `models/metadata.json` berisi versi model, fitur masukan, ambang status, dan metrik
- [ ] Aplikasi dapat dibuka orang lain melalui tautan, termasuk dari ponsel
- [ ] Aplikasi tidak berhenti mendadak ketika menerima masukan yang tidak wajar
- [ ] Laporan paling banyak 6 halaman dan video paling lama 5 menit
