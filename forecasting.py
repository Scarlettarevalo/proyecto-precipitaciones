import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def proyeccion_lineal(df_anual, periodos_futuros):
    X = df_anual[["Anio"]].values
    y = df_anual["Precipitacion_mm"].values
    modelo = LinearRegression()
    modelo.fit(X, y)
    ultimo_anio = int(df_anual["Anio"].max())
    anios_futuros = np.arange(ultimo_anio + 1, ultimo_anio + periodos_futuros + 1).reshape(-1, 1)
    predicciones = np.maximum(0, modelo.predict(anios_futuros))
    return pd.DataFrame({
        "Anio": anios_futuros.flatten(),
        "Proyeccion_mm": np.round(predicciones, 1)
    }), modelo.coef_[0], modelo.intercept_

def proyeccion_promedio_movil(df_anual, periodos_futuros, ventana=3):
    serie = df_anual["Precipitacion_mm"].tolist()
    ultimo_anio = int(df_anual["Anio"].max())
    predicciones = []
    anios_futuros = []
    for i in range(1, periodos_futuros + 1):
        val_pred = np.mean(serie[-ventana:])
        predicciones.append(round(val_pred, 1))
        serie.append(val_pred)
        anios_futuros.append(ultimo_anio + i)
    return pd.DataFrame({
        "Anio": anios_futuros,
        "Proyeccion_mm": predicciones
    })
