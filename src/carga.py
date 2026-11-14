import pandas as pd

def cargar_datos(ruta: str) -> pd.DataFrame:
    return pd.read_csv(ruta)
