import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.forecasting import proyeccion_lineal, proyeccion_promedio_movil

st.set_page_config(page_title="Análisis de Precipitaciones", layout="wide")
st.title("🌧️ Monitoreo Hídrico y Proyección de Precipitaciones")
st.markdown("**Pregunta orientadora:** *¿Las precipitaciones muestran una disminución sostenida?*")

@st.cache_data
def cargar_datos():
    return pd.read_csv("data/precipitaciones_limpias.csv")

df = cargar_datos()

st.sidebar.header("🔍 Filtros de Exploración")
regiones = st.sidebar.multiselect("1. Región:", df["Region"].unique(), default=df["Region"].unique())
estaciones_disp = df[df["Region"].isin(regiones)]["Estacion"].unique()
estaciones = st.sidebar.multiselect("2. Estación Meteorológica:", estaciones_disp, default=estaciones_disp)
rango_anios = st.sidebar.slider("3. Rango de Años:", int(df["Anio"].min()), int(df["Anio"].max()), (2010, 2025))

st.sidebar.header("⚙️ Parámetros de Proyección")
horizonte = st.sidebar.slider("Años a proyectar:", 1, 15, 5)
ventana_pm = st.sidebar.number_input("Ventana Promedio Móvil (años):", 2, 6, 3)
modelo_sel = st.sidebar.selectbox("Método de proyección:", ["Comparar Ambos (Desafío Extra)", "Regresión Lineal", "Promedio Móvil"])

df_filt = df[(df["Region"].isin(regiones)) & (df["Estacion"].isin(estaciones)) & (df["Anio"].between(rango_anios[0], rango_anios[1]))]

if df_filt.empty:
    st.warning("⚠️ Selecciona al menos una región y estación.")
    st.stop()

df_anual = df_filt.groupby(["Anio", "Estacion"], as_index=False)["Precipitacion_mm"].sum()
df_anual_prom = df_anual.groupby("Anio", as_index=False)["Precipitacion_mm"].mean()

st.subheader("📊 Indicadores Hídricos Clave")
c1, c2, c3, c4 = st.columns(4)
prom_anual = df_anual_prom["Precipitacion_mm"].mean()
max_anual = df_anual_prom["Precipitacion_mm"].max()
min_anual = df_anual_prom["Precipitacion_mm"].min()
var_pct = ((df_anual_prom["Precipitacion_mm"].iloc[-1] - df_anual_prom["Precipitacion_mm"].iloc[0]) / df_anual_prom["Precipitacion_mm"].iloc[0]) * 100 if len(df_anual_prom) > 1 else 0

c1.metric("Promedio Anual", f"{prom_anual:,.1f} mm")
c2.metric("Año Más Lluvioso (Máx)", f"{max_anual:,.1f} mm")
c3.metric("Año Más Seco (Mín)", f"{min_anual:,.1f} mm")
c4.metric("Variación Punta a Punta", f"{var_pct:.1f}%")

tab1, tab2 = st.tabs(["📅 Evolución Histórica (Anual y Mensual)", "🔮 Proyección Futura"])

with tab1:
    col_izq, col_der = st.columns(2)
    with col_izq:
        fig_anual = px.bar(df_anual, x="Anio", y="Precipitacion_mm", color="Estacion", barmode="group", title="Totales Anuales por Estación (mm)")
        st.plotly_chart(fig_anual, use_container_width=True)
    with col_der:
        df_mensual = df_filt.groupby("Mes", as_index=False)["Precipitacion_mm"].mean()
        fig_mes = px.area(df_mensual, x="Mes", y="Precipitacion_mm", title="Distribución Mensual Promedio (Estacionalidad)", markers=True)
        st.plotly_chart(fig_mes, use_container_width=True)

with tab2:
    df_lin, pendiente, intercepto = proyeccion_lineal(df_anual_prom, horizonte)
    df_pm = proyeccion_promedio_movil(df_anual_prom, horizonte, ventana=ventana_pm)
    
    fig_proj = go.Figure()
    fig_proj.add_trace(go.Scatter(x=df_anual_prom["Anio"], y=df_anual_prom["Precipitacion_mm"], mode="lines+markers", name="Histórico Real (mm)", line=dict(color="#1f77b4", width=3)))
    
    if modelo_sel in ["Regresión Lineal", "Comparar Ambos (Desafío Extra)"]:
        fig_proj.add_trace(go.Scatter(x=df_lin["Anio"], y=df_lin["Proyeccion_mm"], mode="lines+markers", name="Regresión Lineal", line=dict(dash="dash", color="#d62728")))
        
    if modelo_sel in ["Promedio Móvil", "Comparar Ambos (Desafío Extra)"]:
        fig_proj.add_trace(go.Scatter(x=df_pm["Anio"], y=df_pm["Proyeccion_mm"], mode="lines+markers", name=f"Promedio Móvil (v={ventana_pm})", line=dict(dash="dot", color="#2ca02c")))
        
    fig_proj.update_layout(title="Comparación: Precipitación Histórica vs. Escenarios Proyectados", xaxis_title="Año", yaxis_title="Precipitación Acumulada (mm)")
    st.plotly_chart(fig_proj, use_container_width=True)
    
    tendencia_texto = "disminución sostenida" if pendiente < 0 else "aumento sostenido"
    st.info(f"📌 **Evidencia para la Pregunta Orientadora:** La pendiente lineal es de **{pendiente:.2f} mm/año**, lo que confirma una **{tendencia_texto}** en el período analizado.")
