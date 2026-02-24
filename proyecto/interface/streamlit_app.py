from proyecto.src.utils.my_config import BASE_DIR
from scripts.run_pipeline import run_pipeline
import streamlit as st
from PIL import Image
from pathlib import Path
import time 
"""
sample code for streamlit app
screen 1 
me puse gringo por el cansancio me debe una coca 
"""
#configuracion base
BASE_DIR = Path(__file__).resolve().parent.parent.parent

config = {
    "data_path": BASE_DIR / "data" / "synthetic",
    "output_path": BASE_DIR / "results",
    "modo": "test"
}
#HEAD o CABESON 
st.set_page_config(page_title="Analizador de Clientes HPE", page_icon=":bar_chart:", layout="wide")
st.title("analizador de clientes de HPE")
#chingue asu amdre el amerioca xdxddddd
st.write(
    """
Este sistema analiza señales de mercado, historial de cleitnes y datos empresariales para detectar
 oportunidades de venta y recomendar soluciones HPE."""
)
st.divider()
#control de pipiline
col1,col2,col3 = st.columns(3)
with col1:
    cargar = st.button("Cargar Datos")
with col2:
    ejecutar = st.button("Ejecutar Analisis")
with col3:
    limpiar = st.button("Descargar Resultados")
# sesion estate o estado de la sesion para los frijoleros mejicanos xdxdxd
if "resultados" not in st.session_state:
    st.session_state.resultados = None
if "stats " not in st.session_state:
    st.session_state.stats = {}
    #carga simulacion sumulada simulistica
if cargar:
    #nota esto muestra de donde se esta tomando los datos por lo que 
    #es importante que el path este bien configurado en el archivo de configuracion
    #si el path es correcto se mostrara un mensaje de exito y si no se mostrara un error
    # y como yo me avente el esqueleto de la app sin probarlo, es probable que el path este mal configurado y por eso es importante que se muestre un mensaje de error si el path no es correcto
    #asi qwue si peuden revisenlo y si no ni modo xdxdxd
    st.success ("dataset detectado en: " + str(config["data_path"]))


    #ejecutar pipiline
    if ejecutar:
        with st.spinner("ejecuntando pipiline..."):
            inicio = time.time()
            time.sleep(2) #simulacion de tiempo de ejecucion
            try:
                resultados = run_pipeline(config)

                fin = time.time()

                st.session_state.resultados = resultados
                st.session_state.stats["tiempo_ejecucion"] = fin - inicio,
                st.success ("sismtea ejecutado con esito y corectamente .D")

            except Exception as e:
                st.error("Error al ejecutar el sistema: " + str(e))
# reiniciar o limpiar el resultado
if limpiar:
    st.session_state.resultados = None
    st.session_state.stats = {}
    st.success("Resultados limpiados correctamente.")
#metricas precosese (rapidas poes)
st.subheader( "resumen del sistema ")
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.metric("Clientes",st.session_state.stats.get("clientes","--"))
with col2:
    st.metric("Eventos",st.session_state.stats.get("ventas","--"))
with col3:
    st.metric("Leads Detectados",st.session_state.stats.get("margen","--"))
with col4:
    st.metric("Tiempo",st.session_state.stats.get("clientes","--"))

#resultados preview
st.subheader("top cleitnes detectados")
if st.session_state.resultados is not None:
    try:
        st.dataframe(st.session_state.resultados.head(10))
    except:
        st.info("Resultados generados pero no en formato tabla.")
else:
    st.info("Ejecuta el pipeline para ver resultados.")

st.divider()

st.caption("Proyecto IA HPE - Equipo Devcode")


#como correr la chingadera esta

# python -m streamlit run your_script.py