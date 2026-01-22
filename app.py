import streamlit as st
import pandas as pd
import numpy as np

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="InviertePro - Stock Consolidado", layout="wide")

# TÍTULO
st.title("🏢 Buscador de Stock - InviertePro")

# 1. CARGAR DATOS
@st.cache_data
def cargar_datos():
    # Leemos el archivo que subiste
    df = pd.read_csv("Stock_Consolidado_Completo.csv")
    return df

try:
    df = cargar_datos()
except:
    st.error("⚠️ No se encuentra el archivo 'Stock_Consolidado_Completo.csv'. Súbelo a GitHub.")
    st.stop()

# 2. BARRA LATERAL (FILTROS INTELIGENTES)
st.sidebar.header("🔍 Filtros de Búsqueda")

# Filtro 1: Proyecto
proyectos_disponibles = ["Todos"] + list(df['Proyecto_Unificado'].unique())
proyecto_selec = st.sidebar.selectbox("Proyecto", proyectos_disponibles)

# Filtro 2: Tipología
tipologias_disponibles = ["Todas"] + list(df['Tipologia_Unificada'].astype(str).unique())
tipo_selec = st.sidebar.selectbox("Tipología", tipologias_disponibles)

# Filtro 3: Precio Máximo
precio_max = st.sidebar.slider("Precio Máximo (UF)", 
                               min_value=int(df['Precio_UF_Unificado'].min()), 
                               max_value=int(df['Precio_UF_Unificado'].max()), 
                               value=5000)

# APLICAR FILTROS
df_filtrado = df.copy()

if proyecto_selec != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Proyecto_Unificado'] == proyecto_selec]

if tipo_selec != "Todas":
    df_filtrado = df_filtrado[df_filtrado['Tipologia_Unificada'].astype(str) == tipo_selec]

df_filtrado = df_filtrado[df_filtrado['Precio_UF_Unificado'] <= precio_max]

# 3. RESULTADOS
col1, col2, col3 = st.columns(3)
col1.metric("Unidades Encontradas", len(df_filtrado))
col2.metric("Precio Promedio", f"{df_filtrado['Precio_UF_Unificado'].mean():,.0f} UF")

st.divider()

# MOSTRAR TABLA (Solo columnas clave para que se vea ordenado)
cols_visualizar = ['Proyecto_Unificado', 'Unidad_Unificada', 'Tipologia_Unificada', 
                   'Precio_UF_Unificado', 'M2_Total_Unificado', 'Estado_Unificado']

st.dataframe(
    df_filtrado[cols_visualizar].style.format({"Precio_UF_Unificado": "{:,.0f} UF"}),
    use_container_width=True
)

# 4. BOTÓN DESCARGAR (Para que tus asesores bajen lo filtrado)
st.download_button(
    label="⬇️ Descargar Resultados Filtrados",
    data=df_filtrado.to_csv(index=False).encode('utf-8'),
    file_name='seleccion_inviertepro.csv',
    mime='text/csv',
)
