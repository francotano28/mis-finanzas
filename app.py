import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Finanzas Pro", page_icon="📈", layout="wide")

st.title("🚀 Control de Capital")

# Función para cargar datos (si no existe, crea uno nuevo con columnas limpias)
def cargar_datos():
    columnas = ['Producto', 'Categoria', 'Monto', 'Fecha']
    if os.path.exists('mis_gastos.csv'):
        df_cargado = pd.read_csv('mis_gastos.csv')
        # Si al archivo le faltan columnas por ser viejo, lo reseteamos
        if list(df_cargado.columns) != columnas:
            return pd.DataFrame(columns=columnas)
        return df_cargado
    else:
        return pd.DataFrame(columns=columnas)

df = cargar_datos()

# --- SECCIÓN: CARGAR GASTO ---
with st.expander("➕ Cargar Nuevo Gasto"):
    with st.form("formulario_gasto"):
        col1, col2 = st.columns(2)
        with col1:
            item = st.text_input("¿Qué compraste?")
            monto = st.number_input("Monto ($)", min_value=0.0, step=0.1)
        with col2:
            categoria = st.selectbox("Categoría", ["Comida", "Transporte", "Servicios", "Salidas", "Otros"])
            fecha = st.date_input("Fecha")
        
        enviar = st.form_submit_button("Registrar Gasto 🚀")
        
        if enviar:
            nuevo_gasto = pd.DataFrame([[item, categoria, monto, str(fecha)]], 
                                     columns=['Producto', 'Categoria', 'Monto', 'Fecha'])
            df = pd.concat([df, nuevo_gasto], ignore_index=True)
            df.to_csv('mis_gastos.csv', index=False)
            st.success("¡Gasto registrado!")
            st.rerun()

# --- SECCIÓN: BORRAR GASTO ---
with st.expander("🗑️ Borrar Gasto"):
    if not df.empty:
        opciones = df.index.tolist()
        seleccion = st.selectbox(
            "Seleccioná el gasto que querés eliminar:",
            opciones,
            format_func=lambda x: f"{df.iloc[x]['Fecha']} | {df.iloc[x]['Producto']} | ${df.iloc[x]['Monto']}"
        )
        
        if st.button("Eliminar Gasto Seleccionado ❌"):
            df = df.drop(seleccion).reset_index(drop=True)
            df.to_csv('mis_gastos.csv', index=False)
            st.warning("Gasto eliminado.")
            st.rerun()
    else:
        st.info("No hay gastos registrados para borrar.")

# --- ANÁLISIS ---
if not df.empty:
    st.divider()
    st.subheader("Análisis de Gastos")
    st.write(f"**Total acumulado:** ${df['Monto'].sum():,.2f}")
    
    fig = px.pie(df, values='Monto', names='Categoria', title="Gastos por Categoría")
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df, use_container_width=True)