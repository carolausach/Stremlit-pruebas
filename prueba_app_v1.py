import streamlit as st
import pandas as pd
import io

# Inicializa el DataFrame en session_state si no existe
if 'df_user' not in st.session_state:
    st.session_state.df_user = pd.DataFrame()

st.title("Subir datos y analizar")

# Widget para subir archivo
uploaded_file = st.file_uploader(
    "Elige un archivo CSV o Excel", 
    type=['csv', 'xlsx'], 
    accept_multiple_files=False
)

if uploaded_file is not None:
    # Lee el archivo automáticamente
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Guarda en session_state (automático al subir)
        st.session_state.df_user = df
        
        # Muestra el DataFrame
        st.success("¡Archivo cargado! Aquí está tu DataFrame:")
        st.dataframe(st.session_state.df_user)
        
        # Análisis básico automático (ejemplo: estadísticas)
        if not st.session_state.df_user.empty:
            st.subheader("Análisis automático")
            st.write(st.session_state.df_user.describe())
            
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

# Muestra el DataFrame guardado si existe
if not st.session_state.df_user.empty:
    st.subheader("DataFrame guardado para análisis")
    st.dataframe(st.session_state.df_user)
