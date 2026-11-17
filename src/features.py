import numpy as np
import pandas as pd

KOLOM_SENSOR = ['beban_pct', 'arus_A', 'tegangan_V',
                'suhu_belitan_C', 'getaran_rms_mm_s', 'kecepatan_rpm']

def rapikan_id(s):
    angka = ''.join(ch for ch in str(s) if ch.isdigit())
    return f'M-{int(angka):03d}'

def rapikan_tipe(s):
    s = str(s).upper().replace(' ', '').replace(',', '.')
    return s.replace('KW', 'kW')

def bersihkan_data(df):
    df = df.copy()
    df['motor_id'] = df['motor_id'].map(rapikan_id)
    df['tipe_motor'] = df['tipe_motor'].map(rapikan_tipe)
    df['tipe_motor'] = df.groupby('motor_id')['tipe_motor'].transform(lambda s: s.mode().iloc[0])
    df = df.drop_duplicates()
    df['suhu_belitan_C'] = np.where(df['suhu_belitan_C'] > 150,
                                    df['suhu_belitan_C'] - 273.15,
                                    df['suhu_belitan_C'])
    df.loc[df['getaran_rms_mm_s'] <= 0, 'getaran_rms_mm_s'] = np.nan
    df = df.sort_values(['motor_id', 'hari_operasi']).reset_index(drop=True)
    for c in ['arus_A', 'suhu_belitan_C', 'getaran_rms_mm_s']:
        df[c] = df.groupby('motor_id')[c].transform(lambda s: s.interpolate(limit_direction='both'))
    return df

def buat_fitur(df):
    df = df.copy()
    df['arus_per_beban'] = df['arus_A'] / df['beban_pct'].clip(lower=1)
    df['getaran_x_suhu'] = df['getaran_rms_mm_s'] * df['suhu_belitan_C']
    return df

def tentukan_status(rul_pred, segera=14, pesan=45):
    if rul_pred <= segera:
        return 'SEGERA GANTI'
    if rul_pred <= pesan:
        return 'PESAN PENGGANTI SEKARANG'
    return 'AMAN'
