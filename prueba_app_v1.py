import streamlit as st
import pandas as pd
import io
from io import BytesIO

st.set_page_config(
    page_title='Análisis',
    page_icon=':clipboard2-data:', # This is an emoji shortcode. Could be a URL too.
)

st.info(
        "Selecciona si vas a **subir un archivo** o vas a subir de **ingresar de manera manual**",
    )


tab1, tab2, tab3 = st.tabs([f"Subir archivo",
                        f"Ingreso Manual",
                        f"Cotizaciones"])


with tab1:
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

            st.write("Nombres de columnas detectadas:", list(df.columns))
            #st.dataframe(df)
            
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

        st.header(":bar_chart: Estadísticas :bar_chart:")

        st.subheader("Análisis rápido con métricas")

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if not numeric_cols:
            st.warning("No hay columnas numéricas.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                col_selected = st.selectbox("Columna numérica", numeric_cols)

            with col2:
                operation = st.radio("Operación", ["Suma", "Promedio"], horizontal=True)

            if col_selected:
                if operation == "Suma":
                    result = df[col_selected].sum()
                    label = f"Suma de {col_selected}"
                else:
                    result = df[col_selected].mean()
                    label = f"Promedio de {col_selected}"

                # Mostrar el resultado en una columna con metric
                c1, c2, c3 = st.columns(3)
                with c2:
                    st.metric(label=label, value=f"{result:,.2f}")

with tab2:
# Muestra el DataFrame guardado si existe
    if not st.session_state.df_user.empty:
        st.subheader("DataFrame guardado para análisis")
        st.dataframe(st.session_state.df_user)


    st.title("Ingreso manual de datos")

    st.info(
        "Ingresa tus datos manualmente.",
        icon="✍️",
    )
    cols_input = st.text_input("Escribe los nombres de las columnas, separados por coma:", value="Nombre,Edad,Ciudad")
    if cols_input:
        col_names = [c.strip() for c in cols_input.split(",")]
        # Crea DataFrame vacío con esas columnas
        df_manual = pd.DataFrame(columns=col_names)
        st.write("Tus columnas serán:", col_names)
        # Permite luego agregar filas/editarlos, por ejemplo con st.data_editor
        edited_df = st.data_editor(df_manual, num_rows="dynamic")
        st.write("Data ingresada:", edited_df)

    # Crea un DataFrame base (vacío o con columnas definidas)
    #if 'df_manual' not in st.session_state:
    #    # Ejemplo: columnas para datos de ejemplo (adáptalo a tu caso)
    #    st.session_state.df_manual = pd.DataFrame({
    #    "producto": [""],
    #    "cantidad": [0],
    #    "precio": [0.0],
    #    })

    # Widget editable: el usuario puede agregar/filas, editar celdas
    #edited_df = st.data_editor(
    #    st.session_state.df_manual,
    #    num_rows="dynamic",  # Permite agregar/eliminar filas automáticamente
    #    use_container_width=True,
    #    hide_index=False
    #)

    # Guarda cambios automáticamente al editar
    st.session_state.df_manual = edited_df
    df = st.session_state.df_manual

    # Solo columnas numéricas
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

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

        ## agrego estadísticas y gráficos de barras

    ## agrego estadísticas y gráficos de barras
        st.header(":bar_chart: Estadísticas :bar_chart:")

        st.subheader("Análisis rápido con métricas")

        numeric_cols = edited_df.select_dtypes(include="number").columns.tolist()

        if not numeric_cols:
            st.warning("No hay columnas numéricas.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                col_selected = st.selectbox("Columna numérica", numeric_cols)

            with col2:
                operation = st.radio("Operación", ["Suma", "Promedio"], horizontal=True)

            if col_selected:
                if operation == "Suma":
                    result = edited_df[col_selected].sum()
                    label = f"Suma de {col_selected}"
                else:
                    result = edited_df[col_selected].mean()
                    label = f"Promedio de {col_selected}"

                # Mostrar el resultado en una columna con metric
                c1, c2, c3 = st.columns(3)
                with c2:
                    st.metric(label=label, value=f"{result:,.2f}")

with tab3:
    st.title("Generador de Cotizaciones")

    # --- Datos generales de la cotización ---
    st.header("Datos del cliente y empresa")

    col1, col2 = st.columns(2)
    with col1:
        nombre_cotizante = st.text_input("Nombre de la persona que cotiza")
        empresa_cliente = st.text_input("Nombre de la empresa cliente")
    with col2:
        empresa_proveedora = st.text_input("Nombre de la empresa que cotiza")
        numero_cotizacion = st.text_input("N° de cotización (opcional)")

    # --- Ingreso de productos ---
    st.header("Productos a cotizar")

    # Número de filas (items)
    n_items = st.number_input("¿Cuántos productos quieres ingresar?", min_value=1, max_value=50, value=3, step=1)

    items = []
    for i in range(n_items):
        st.subheader(f"Producto {i+1}")
        c1, c2, c3 = st.columns([2,1,1])
        with c1:
            codigo = st.text_input(f"Código producto {i+1}", key=f"cod_{i}")
            descripcion = st.text_input(f"Descripción producto {i+1}", key=f"desc_{i}")
        with c2:
            cantidad = st.number_input(f"Cantidad {i+1}", min_value=0.0, value=0.0, step=1.0, key=f"cant_{i}")
        with c3:
            precio_unitario = st.number_input(f"Precio unitario {i+1}", min_value=0.0, value=0.0, step=100.0, key=f"precio_{i}")
        
        if codigo or descripcion:
            subtotal = cantidad * precio_unitario
            items.append({
                "Código": codigo,
                "Descripción": descripcion,
                "Cantidad": cantidad,
                "Precio unitario": precio_unitario,
                "Subtotal": subtotal,
            })

    # --- Construir tabla de cotización ---
    if items:
        df_cotizacion = pd.DataFrame(items)
        total = df_cotizacion["Subtotal"].sum()

        st.header("Resumen de la cotización")

        st.markdown(f"**Cotizante:** {nombre_cotizante}")
        st.markdown(f"**Empresa cliente:** {empresa_cliente}")
        st.markdown(f"**Empresa que cotiza:** {empresa_proveedora}")
        if numero_cotizacion:
            st.markdown(f"**N° Cotización:** {numero_cotizacion}")

        st.dataframe(df_cotizacion, use_container_width=True)

        st.subheader("Total")
        st.metric("Total cotización", f"${total:,.0f}")

        # --- Descargar planilla personalizada (Excel) ---
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            # Hoja con detalle
            df_cotizacion.to_excel(writer, sheet_name="Cotización", index=False)

            # Hoja con meta-datos (opcional)
            meta = pd.DataFrame({
                "Campo": ["Cotizante", "Empresa cliente", "Empresa que cotiza", "N° Cotización", "Total"],
                "Valor": [nombre_cotizante, empresa_cliente, empresa_proveedora, numero_cotizacion, total],
            })
            meta.to_excel(writer, sheet_name="Resumen", index=False)

        buffer.seek(0)

        st.download_button(
            label="Descargar cotización en Excel",
            data=buffer,
            file_name=f"cotizacion_{numero_cotizacion or 'sin_numero'}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.info("Ingresa al menos un producto (código o descripción) para generar la cotización.")