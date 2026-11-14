import pandas as pd

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    df = df.dropna(subset=["Fecha", "Region", "Estacion", "Precipitacion_mm"])
    df["Precipitacion_mm"] = pd.to_numeric(df["Precipitacion_mm"], errors="coerce").fillna(0.0)
    return df[df["Precipitacion_mm"] >= 0].sort_values("Fecha").reset_index(drop=True)
