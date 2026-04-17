import streamlit as st
import pandas as pd
import datetime
import os
import plotly.express as px

st.set_page_config(page_title="Finanzas Pro", page_icon="📈", layout="wide")
st.title("🚀 Control de Capital - Franquicias")

archivo_datos = "mis_gastos.csv"
categorias = ["Comida", "Padel/Fútbol", "Cigarros", "Estudio/UBA", "Varios"]

# --- FORMULARIO ---
with st.expander("➕ Cargar Nuevo Gasto", expanded=True):
    with st.form("nuevo_gasto", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            concepto = st.text_input("¿Qué compraste?")
            monto = st.number_input("Monto ($)", min_value=0.0, step=100.0)
        with col2:
            categoria = st.selectbox("Categoría", categorias)
            fecha = st.date_input("Fecha", datetime.date.today())
        
        if st.form_submit_button("Registrar Gasto 🚀"):
            if concepto != "":
                nuevo_gasto = pd.DataFrame([[fecha, concepto, monto, categoria]], 
                                           columns=["Fecha", "Concepto", "Monto", "Categoría"])
                if not os.path.isfile(archivo_datos):
                    nuevo_gasto.to_csv(archivo_datos, index=False)
                else:
                    nuevo_gasto.to_csv(archivo_datos, mode='a', index=False, header=False)
                st.success("¡Gasto guardado!")
                st.rerun()

# --- LÓGICA DE FILTRADO ---
if os.path.isfile(archivo_datos):
    df = pd.read_csv(archivo_datos)
    df['Fecha'] = pd.to_datetime(df['Fecha']) # Convertimos a formato fecha real
    
    # Creamos una columna que diga "Mes Año" para filtrar
    df['Mes_Año'] = df['Fecha'].dt.strftime('%B %Y')
    
    # Selector de mes en la barra lateral
    meses_disponibles = df['Mes_Año'].unique()
    mes_seleccionado = st.sidebar.selectbox("📅 Seleccioná el Mes", meses_disponibles, index=len(meses_disponibles)-1)
    
    # Filtramos los datos
    df_filtrado = df[df['Mes_Año'] == mes_seleccionado]

    # --- VISUALIZACIÓN ---
    st.header(f"Análisis de {mes_seleccionado}")
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        total_mes = df_filtrado['Monto'].sum()
        st.metric("Total del Mes", f"${total_mes:,.2f}")
        st.write("---")
        st.write("**Desglose:**")
        st.dataframe(df_filtrado[["Fecha", "Concepto", "Monto", "Categoría"]], hide_index=True)

    with col_b:
        fig = px.pie(df_filtrado, values='Monto', names='Categoría', 
                     title=f"Gastos por Categoría - {mes_seleccionado}",
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Cargá tu primer gasto para empezar a trackear.")