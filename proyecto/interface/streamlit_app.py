from proyecto.scripts.run_pipeline import run_pipeline
import streamlit as st
from pathlib import Path
import time
import io
from datetime import datetime
import plotly.express as px
import pandas as pd

"""
sample code for streamlit app
screen 1 
me puse gringo por el cansancio me debe una coca 
"""

# configuracion base de direcctorios
BASE_DIR = Path(__file__).resolve().parent.parent.parent

config = {
    "data_path": BASE_DIR / "data" / "synthetic",
    "output_path": BASE_DIR / "results",
    "modo": "test"
}

# HEAD o CABESON de entrada 
# SI YA SE QUE SUENA MAL PERO ES PARA QUE SE ENTIENDA RAPIDOoOOoOoOooOoOooOo
st.set_page_config(page_title="Analizador de Clientes HPE", page_icon=":bar_chart:", layout="wide")
st.title("Analizador de clientes de HPE")

st.write("""
Este sistema analiza señales de mercado, historial de clientes y datos empresariales 
para detectar oportunidades de venta y recomendar soluciones HPE.
""")

st.divider()

# barra lateral
pagina = st.sidebar.radio(
    "Navegación",
    ["Dashboard", "Resultados", "Detalle Cliente", "Gráficas", "Exportar"]
)

# estado de sesion para los frijoleros mejicanos xdxdxd
if "resultados" not in st.session_state:
    st.session_state.resultados = None

if "stats" not in st.session_state:
    st.session_state.stats = {}

# ===============================
# PAGINA 1 - DASHBOARD
# ===============================
if pagina == "Dashboard":

    st.header("Bienvenido al Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        cargar = st.button("Cargar Datos")

    with col2:
        ejecutar = st.button("Ejecutar Analisis")

    with col3:
        limpiar = st.button("Limpiar Resultados")

    if cargar:
        st.success("Dataset detectado en: " + str(config["data_path"]))

    if ejecutar:
        with st.spinner("ejecutando pipeline..."):
            inicio = time.time()
            try:
                resultados = run_pipeline(config)
                fin = time.time()

                st.session_state.resultados = resultados
                st.session_state.stats["tiempo"] = round(fin - inicio, 2)
                st.session_state.stats["clientes"] = len(resultados)

                st.success("Sistema ejecutado correctamente")

            except Exception as e:
                st.error("Error: " + str(e))

    if limpiar:
        st.session_state.resultados = None
        st.session_state.stats = {}
        st.success("Resultados limpiados")

    st.subheader("Resumen del sistema")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Clientes", st.session_state.stats.get("clientes", "--"))
    with col2:
        st.metric("Tiempo (s)", st.session_state.stats.get("tiempo", "--"))

    if st.session_state.resultados is not None:
        st.subheader("Top clientes detectados")
        st.dataframe(st.session_state.resultados.head(10))

# ===============================
# PAGINA 2 - RESULTADOS
# ===============================
if pagina == "Resultados":

    st.header("Resultados Detallados")

    if st.session_state.resultados is None:
        st.warning("Ejecuta el pipeline primero en el Dashboard")
    else:
        df = st.session_state.resultados

        score_min = st.slider("Score mínimo", 0, 100, 50)

        filtrado = df

        if "score" in df.columns:
            filtrado = filtrado[filtrado["score"] >= score_min]

        st.subheader(f"Resultados Filtrados: {len(filtrado)}")
        st.dataframe(filtrado)

        if "score" in df.columns:
            st.subheader("Top 10 clientes potenciales")
            top10 = df.sort_values("score", ascending=False).head(10)
            st.dataframe(top10)

# ===============================
# PAGINA 3 - DETALLE
# ===============================
if pagina == "Detalle Cliente":

    st.header("Detalle por Cliente")

    if st.session_state.resultados is None:
        st.info("Ejecuta el pipeline primero.")
    else:
        df = st.session_state.resultados

        cliente_nombre = st.selectbox(
            "Selecciona una empresa",
            df["empresa"].unique()
        )

        cliente = df[df["empresa"] == cliente_nombre].iloc[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Score", cliente.get("score", "--"))
        with col2:
            st.metric("Industria", cliente.get("industria", "--"))
        with col3:
            st.metric("Segmento", cliente.get("segmento", "--"))

        st.subheader("Recomendación HPE")
        st.success(cliente.get("recomendacion", "Sin recomendación"))

        st.subheader("Datos completos")
        st.json(cliente.to_dict())

# ===============================
# PAGINA 4 - GRAFICAS
# ===============================
if pagina == "Gráficas":

    st.header("Visualización del Modelo")

    if st.session_state.resultados is None:
        st.warning("Ejecuta el pipeline primero.")
    else:
        df = st.session_state.resultados

        if "score" in df.columns:
            fig = px.histogram(df, x="score")
            st.plotly_chart(fig)

        if "industria" in df.columns:
            conteo = df["industria"].value_counts()
            st.bar_chart(conteo)

# ===============================
# PAGINA 5 - EXPORTAR
# ===============================
if pagina == "Exportar":

    st.header("Exportar Resultados")

    if st.session_state.resultados is None:
        st.warning("Ejecuta el pipeline primero.")
    else:
        df = st.session_state.resultados

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="clientes_analizados.csv",
            mime="text/csv"
        )

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)

        st.download_button(
            label="Descargar Excel",
            data=output.getvalue(),
            file_name="clientes_analizados.xlsx"
        )



        # que chinfue asu madre el america
