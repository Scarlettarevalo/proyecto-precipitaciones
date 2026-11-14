import numpy as np
import pandas as pd

def proyectar_precipitacion(df_anual: pd.DataFrame, anios_futuros: int = 5, metodo: str = "Regresión Lineal") -> pd.DataFrame:
    df_anual = df_anual.sort_values("Anio").reset_index(drop=True)
    ultimo_anio = int(df_anual["Anio"].max())
    anios_proj = np.arange(ultimo_anio + 1, ultimo_anio + anios_futuros + 1)
    if metodo == "Regresión Lineal":
        pendiente, intercepto = np.polyfit(df_anual["Anio"].values, df_anual["Precipitacion_mm"].values, 1)
        valores_proj = np.maximum(0, pendiente * anios_proj + intercepto)
    else:
        promedio_movil = df_anual["Precipitacion_mm"].rolling(window=min(3, len(df_anual))).mean().iloc[-1]
        valores_proj = np.repeat(promedio_movil, anios_futuros)
    return pd.DataFrame({"Anio": anios_proj, "Precipitacion_mm": np.round(valores_proj, 1)})
