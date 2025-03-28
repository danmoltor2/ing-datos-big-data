import pandas as pd
import os

#print(os.getcwd())

def convert_csv_to_parquet(csv_path, parquet_path):
    try:
        df = pd.read_csv(csv_path, low_memory=False)

        # Normalizamos los nombres de las columnas
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # Realizamos conversiones de tipos de datos para timestamp y energy(kwh/hh), y renombramos para este segundo caso
        if 'tstp' in df.columns:
            df['tstp'] = pd.to_datetime(df['tstp'], errors='coerce')

        if 'energy(kwh/hh)' in df.columns:
            df = df.rename(columns={'energy(kwh/hh)': 'energy'})
            df['energy'] = pd.to_numeric(df['energy'], errors='coerce')

        # Guardamos en Parquet con compresión Snappy
        df.to_parquet(parquet_path, engine='pyarrow', compression='snappy')
        print(f"Conversión completa: {csv_path} → {parquet_path}")

    except Exception as e:
        print(f"Error al convertir {csv_path}: {e}")

# Convertimos informations_households.csv a Parquet
base_path = '../datasets/E1/'
household_path = os.path.join(base_path, 'informations_households.csv')
household_parquet = os.path.join(base_path, 'informations_households.parquet')
convert_csv_to_parquet(household_path, household_parquet)

# Repetimos con halfhourly_dataset
halfhourly_path = os.path.join(base_path, 'halfhourly_dataset')
parquet_folder = os.path.join(base_path, 'halfhourly_parquet')
os.makedirs(parquet_folder, exist_ok=True)

for i in range(112):
    csv_file = os.path.join(halfhourly_path, f'block_{i}.csv')
    parquet_file = os.path.join(parquet_folder, f'block_{i}.parquet')
    if os.path.exists(csv_file):
        convert_csv_to_parquet(csv_file, parquet_file)
    else:
        print(f"Archivo no encontrado: {csv_file}")