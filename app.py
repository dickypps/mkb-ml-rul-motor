import json
import joblib
import pandas as pd
import streamlit as st
from src.features import buat_fitur, tentukan_status

st.set_page_config(page_title='Sisa Umur Motor Induksi')

@st.cache_resource
def muat():
    model = joblib.load('models/model.joblib')
    meta = json.load(open('models/metadata.json'))
    return model, meta

model, meta = muat()
batas_latih = meta['batas_data_latih']
amb = meta['ambang_status']

BATAS_MUSTAHIL = {
    'beban_pct': (0, 150), 'arus_A': (0, 100), 'tegangan_V': (300, 450),
    'suhu_belitan_C': (0, 200), 'getaran_rms_mm_s': (0.01, 30),
    'kecepatan_rpm': (500, 1800), 'hari_operasi': (0, 2000),
}

st.title('Prediksi Sisa Umur Pakai Motor Induksi')
st.write('Untuk perencana pemeliharaan: masukkan tipe motor dan pembacaan sensor hari ini.')

tipe = st.selectbox('Tipe motor', ['5.5kW', '11kW', '22kW'])
c1, c2 = st.columns(2)
nilai = {
    'hari_operasi': c1.number_input('Hari operasi (sejak dipasang)', value=150, step=1),
    'beban_pct': c1.number_input('Beban (%)', value=75.0),
    'arus_A': c1.number_input('Arus (A)', value=15.0),
    'tegangan_V': c1.number_input('Tegangan (V)', value=380.0),
    'suhu_belitan_C': c2.number_input('Suhu belitan (°C)', value=65.0),
    'getaran_rms_mm_s': c2.number_input('Getaran RMS (mm/s)', value=2.3),
    'kecepatan_rpm': c2.number_input('Kecepatan (rpm)', value=1472.0),
}

if st.button('Prediksi'):
    # 1) tolak masukan yang mustahil
    salah = [f'{k} = {v} di luar rentang wajar {BATAS_MUSTAHIL[k]}'
             for k, v in nilai.items()
             if not (BATAS_MUSTAHIL[k][0] <= v <= BATAS_MUSTAHIL[k][1])]
    if salah:
        st.error('Masukan tidak valid:\n\n- ' + '\n- '.join(salah))
        st.stop()

    # 2) peringatan kalau di luar rentang data latih
    luar = [k for k, v in nilai.items()
            if not (batas_latih[k][0] <= v <= batas_latih[k][1])]
    if luar:
        st.warning('Nilai di luar rentang data latih, prediksi kurang dapat diandalkan: '
                   + ', '.join(luar))

    # 3) prediksi
    baris = pd.DataFrame([{'tipe_motor': tipe, **nilai}])
    pred = max(float(model.predict(buat_fitur(baris)[meta['fitur']])[0]), 0.0)
    status = tentukan_status(pred, amb['segera_ganti_hari'], amb['pesan_sekarang_hari'])

    st.metric('Perkiraan sisa umur', f'{pred:.0f} hari')
    if status == 'SEGERA GANTI':
        st.error(status)
    elif status == 'AMAN':
        st.success(status)
    else:
        st.warning(status)
    mae = meta['metrik_test']['mae_rul_le_60']
    st.caption(f'Pada motor yang hampir rusak, tebakan model rata-rata meleset sekitar {mae:.1f} hari.')
