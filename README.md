# Prediksi Sisa Umur Pakai Motor (RUL) · Tim [nama tim]

**Kasus:** [nomor dan nama kasus] · **Aplikasi:** [tautan aplikasi] · **Video:** [tautan video]

| Anggota | NIM | Bagian yang dikerjakan |
|---|---|---|
| [nama] | [NIM] | EDA dan pembersihan data |
| [nama] | [NIM] | Model dan evaluasi |
| [nama] | [NIM] | API dan aplikasi |

## Masalah dan pengguna

Pengguna proyek ini adalah teknisi perawatan (*maintenance*) dan manajer pabrik yang mengoperasikan motor listrik. Model memperkirakan sisa umur pakai (RUL) motor dari data sensor, sehingga tim dapat menjadwalkan perawatan sebelum motor rusak dan menghindari henti produksi mendadak.

## Data dan pembersihan

| Masalah yang ditemukan | Jumlah baris | Cara menangani |
|---|---|---|
| Baris duplikat | [angka] | Dihapus dengan `drop_duplicates` |
| Nilai sensor kosong | [angka] | [diisi median / interpolasi / dihapus] |
| Nilai sensor tidak wajar (*outlier*) | [angka] | [dipotong dengan batas IQR / dibiarkan, alasannya] |

## Hasil

| Model | RMSE *validation* | RMSE *test* |
|---|---|---|
| *Baseline*: [rata-rata RUL / regresi linear] | [angka] | [angka] |
| [model final, misalnya Random Forest] | [angka] | [angka] |

*Threshold* yang dipakai: [angka] siklus, karena [alasan bisnis, misalnya motor dengan prediksi RUL di bawah angka ini harus segera dijadwalkan perawatan].

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
