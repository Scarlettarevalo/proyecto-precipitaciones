import pandas as pd
import numpy as np

np.random.seed(42)
anios = range(2010, 2026)
meses = range(1, 13)
estaciones = [
    ("Valparaíso", "Quinta Normal Costa", 380),
    ("Metropolitana", "Quinta Normal Santiago", 310),
    ("Biobío", "Carriel Sur Concepción", 1050),
    ("La Araucanía", "Maquehue Temuco", 1150)
]

registros = []
for anio in anios:
    factor_sequia = 1 - (anio - 2010) * 0.018
    for mes in meses:
        peso_mes = 0.18 if mes in [5, 6, 7, 8] else (0.06 if mes in [4, 9, 10] else 0.025)
        for region, estacion, base_anual in estaciones:
            lluvia = base_anual * peso_mes * factor_sequia * np.random.uniform(0.75, 1.25)
            registros.append({
                "Fecha": f"{anio}-{mes:02d}-01",
                "Anio": anio,
                "Mes": mes,
                "Region": region,
                "Estacion": estacion,
                "Precipitacion_mm": round(lluvia, 1)
            })

df = pd.DataFrame(registros)
df.to_csv("data/precipitaciones_limpias.csv", index=False)
print("Listo! Datos creados.")
