# Prediksi Sisa Umur Pakai Motor (RUL) · Tim 18

**Kasus:** [3-Remaining usefull life, induction motor] · **Aplikasi:** [[tautan aplikasi](https://mkb-ml-rul-motor-kvcysaqh7qyl6dki4yev6r.streamlit.app/)] · **Video:** [tautan video]

| Anggota | NIM | Bagian yang dikerjakan |
|---|---|---|
| Dicky Pinusa Prima Sugondo | 2410015 | EDA dan pembersihan data |
| Daffa Jiyadi Santoso | 2405250 | Model dan evaluasi |
| API dan aplikasi |

## Masalah dan pengguna

Pengguna proyek ini adalah teknisi perawatan (*maintenance*) dan manajer pabrik yang mengoperasikan motor listrik. Model memperkirakan sisa umur pakai (RUL) motor dari data sensor, sehingga tim dapat menjadwalkan perawatan sebelum motor rusak dan menghindari henti produksi mendadak.

## Data dan pembersihan

Data mentah berisi 79.652 baris dan 11 kolom. Setelah dibersihkan menjadi 79.159 baris dari 300 motor.

| Masalah yang ditemukan | Jumlah baris | Cara menangani |
|---|---|---|
| Baris duplikat | 493 | Dihapus dengan `drop_duplicates` setelah ID dan tipe dirapikan |
| Format `motor_id` tidak konsisten | 1.147 ID mentah menjadi 300 motor | Diseragamkan ke format `M-001` |
| Penulisan `tipe_motor` tidak konsisten (`22KW`, `11 kW`, `5,5 kW`) | 1.588 | Dirapikan menjadi 3 tipe (`5.5kW`, `11kW`, `22kW`), lalu diambil nilai yang paling sering per motor |
| `arus_A` kosong | 1.602 | Interpolasi dari data motor yang sama |
| `suhu_belitan_C` kosong | 794 | Interpolasi dari data motor yang sama |
| Suhu dalam Kelvin (nilai > 150) | 25.355 | Dikurangi 273,15 menjadi Celsius |
| `getaran_rms_mm_s` ≤ 0 (kode error sensor) | 241 | Dijadikan kosong, lalu diinterpolasi per motor |


## Hasil

Metrik utama adalah MAE (hari) pada motor yang hampir rusak (`rul_hari` ≤ 60), karena itu yang paling penting bagi pengguna.

| Model | MAE RUL ≤ 60 *validation* | MAE RUL ≤ 60 *test* | MAE semua baris *test* |
|---|---|---|---|
| *Baseline*: regresi linear | 29,88 | 30,46 | 54,90 |
| Gradient boosting (`HistGradientBoostingRegressor`, loss `absolute_error`, + `hari_operasi`) | 9,22 | 8,77 | 48,66 |

Pada motor yang hampir rusak, kesalahan rata-rata turun dari sekitar 30 hari menjadi sekitar 9 hari (kira-kira 71% lebih akurat), dan angka *test* dekat dengan *validation* sehingga model stabil.

*Threshold* yang dipakai: 14 hari untuk status "segera ganti" dan 45 hari untuk status "pesan sekarang", karena pengiriman motor pengganti memakan 14-28 hari, sehingga motor yang diprediksi sisa umurnya di bawah angka itu harus segera ditangani.

## Cara menjalankan

```bash
pip install -r requirements.txt
uvicorn app.api.main:app --reload       # API
streamlit run app/ui/streamlit_app.py   # aplikasi
```

## Struktur repositori

```
notebooks/      notebook dari EDA sampai penyimpanan model
data/           data mentah (dan data bersih jika perlu)
src/features.py fungsi pembuat fitur, dipakai saat pelatihan dan saat prediksi
artifacts/      model.joblib + metadata.json
app/            API (FastAPI) dan antarmuka (Streamlit)
```

## Keterbatasan

Model hanya dilatih pada data [jenis motor / kondisi operasi] sehingga kurang dapat dipercaya untuk motor dengan spesifikasi atau beban kerja yang jauh berbeda. Data kegagalan nyata masih terbatas, dan [data yang belum tersedia, misalnya riwayat perawatan atau kondisi lingkungan] belum dipakai.

## Daftar periksa sebelum dikumpulkan

- [ ] Repositori bersifat publik dan setiap anggota memiliki *commit*
- [ ] *Notebook* dapat dijalankan ulang dari awal sampai akhir tanpa galat
- [ ] *Baseline* wajib dilaporkan dan dibandingkan
- [ ] Data *test* hanya dibuka satu kali, di akhir
- [ ] `artifacts/metadata.json` berisi versi model, fitur masukan, *threshold*, dan metrik
- [ ] Aplikasi dapat dibuka orang lain melalui tautan, termasuk dari ponsel
- [ ] Aplikasi tidak berhenti mendadak ketika menerima masukan yang tidak wajar
- [ ] Laporan paling banyak 6 halaman dan video paling lama 5 menit
