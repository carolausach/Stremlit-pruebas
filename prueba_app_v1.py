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




st.title("Ingreso manual de datos")

# Crea un DataFrame base (vacío o con columnas definidas)
if 'df_manual' not in st.session_state:
    # Ejemplo: columnas para datos de ejemplo (adáptalo a tu caso)
    st.session_state.df_manual = pd.DataFrame({
        'Nombre': [''],
        'Edad': [0],
        'Ciudad': ['']
    })

# Widget editable: el usuario puede agregar/filas, editar celdas
edited_df = st.data_editor(
    st.session_state.df_manual,
    num_rows="dynamic",  # Permite agregar/eliminar filas automáticamente
    use_container_width=True,
    hide_index=False
)

# Guarda cambios automáticamente al editar
st.session_state.df_manual = edited_df

# Muestra el DataFrame actualizado
st.subheader("Tus datos ingresados:")
st.dataframe(st.session_state.df_manual)

# Análisis automático (ejemplo)
if not st.session_state.df_manual.empty:
    st.subheader("Análisis rápido")
    # Limpia filas vacías si hay
    df_clean = st.session_state.df_manual.dropna()
    if not df_clean.empty:
        st.write(df_clean.describe(include='all'))
