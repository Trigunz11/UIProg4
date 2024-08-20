import pandas as pd

# Función para cargar y procesar un archivo CSV
def load_and_process_csv(file_path, sep=',', skiprows=0):
    try:
        df = pd.read_csv(file_path, sep=sep, skiprows=skiprows, engine='python', quotechar='"', on_bad_lines='skip')
        print(f"Archivo {file_path} cargado correctamente.")
        print(df.head())
        return df
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo {file_path}: {e}")
        return None

# Cargar los tres archivos
df1 = load_and_process_csv('API_SH.IMM.MEAS_DS2_en_csv_v2_3437337.csv', skiprows=4)
df2 = load_and_process_csv('Metadata_Country_API_SH.IMM.MEAS_DS2_en_csv_v2_3437337.csv', skiprows=2)
df3 = load_and_process_csv('Metadata_Indicator_API_SH.IMM.MEAS_DS2_en_csv_v2_3437337.csv', skiprows=0)  # Ajusta 'otro_archivo.csv' con el nombre real

# Si necesitas concatenar los DataFrames, asegúrate de que tengan la misma estructura
# df_combined = pd.concat([df1, df2, df3], ignore_index=True)

# Si necesitas guardar los resultados procesados
if df1 is not None:
    df1.to_csv('processed_API_SH.IMM.MEAS_DS2_en_csv_v2_3437337.csv', index=False)

if df2 is not None:
    df2.to_csv('processed_Metadata_Country_API_SH.IMM.MEAS_DS2_en_csv_v2_3437337.csv', index=False)

if df3 is not None:
    df3.to_csv('processed_Metadata_Indicator_API_SH.IMM.MEAS_DS2_en_csv_v2_3437337.csv', index=False)
