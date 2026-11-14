import pandas as pd

def transformar_datos(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.copy()
    df["Anio"] = df["Fecha"].dt.year
    df["Mes"] = df["Fecha"].dt.month
    mensual = df.groupby(["Region", "Estacion", "Anio", "Mes"], as_index=False)["Precipitacion_mm"].sum()
    anual = df.groupby(["Region", "Estacion", "Anio"], as_index=False)["Precipitacion_mm"].sum()
    return mensual, anual
