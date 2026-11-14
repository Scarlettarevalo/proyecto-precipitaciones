import os
import pandas as pd

def generar_resumen_texto(df_anual: pd.DataFrame, proj: pd.DataFrame) -> str:
    os.makedirs("reportes", exist_ok=True)
    texto = f"Promedio anual: {df_anual['Precipitacion_mm'].mean():.1f} mm\n"
    with open("reportes/resumen_pipeline.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    return texto
