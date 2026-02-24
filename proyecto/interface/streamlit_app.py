from proyecto.src.utils.my_config import BASE_DIR
from scripts.run_pipeline import run_pipeline
import streamlit as st
from PIL import Image
from pathlib import Path
import time 
import io
from datetime import datetime
import plotly.express as px
"""
sample code for streamlit app
screen 1 
me puse gringo por el cansancio me debe una coca 
"""
#configuracion base de direcctorios
BASE_DIR = Path(__file__).resolve().parent.parent.parent

config = {
    "data_path": BASE_DIR / "data" / "synthetic",
    "output_path": BASE_DIR / "results",
    "modo": "test"
}
#HEAD o CABESON de entrada 
#SI YA SE QUE SUENA MAL PERO ES PARA QUE SE ENTIENDA RAPIDOoOOoOoOooOoOooOo
st.set_page_config(page_title="Analizador de Clientes HPE", page_icon=":bar_chart:", layout="wide")
st.title("analizador de clientes de HPE")
#chingue asu amdre el amerioca xdxddddd

#entrada de pagina 
#el css lo arregla
#NOTA EL PIPILINE debe debolver esto 
# empresa | score | segmento | recomendacion
# para que funcione pero no tengo tiepo primer escribo y luego lo hago funcionar 
st.write(
    """
Este sistema analiza señales de mercado, historial de cleitnes y datos empresariales para detectar
 oportunidades de venta y recomendar soluciones HPE."""
)
st.divider()
#barra lateral de navegacion
#corregir tiene un bug donde se sobreponen las paginas y se pueden seleccionar varias a la vez, esto se puede corregir con un radio button
# o algo asi pero por ahora asi se queda porque ya no tengo tiempo para corregirlo
pagina = st.sidebar.radio(
    "Navegación",
    ["Dashboard", "Resultados", "Detalle Cliente", "Gráficas", "Exportar"]
)
#control para mostrar la pagina seleccionada
#se me paso un if :c
if pagina == "Dashboard": 
    st.header("Bienvenido al Dashboard de Análisis de Clientes HPE")
    st.write(
        """En esta sección puedes cargar datos, ejecutar el análisis y visualizar resultados clave sobre tus clientes y oportunidades de venta."""
    )
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
            #IMPORTANTE QUITAR PROXIMAMENTE PORQUE SI NO DA UN MUY MAL EJEMPLO
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

# aca empiesa la pagina 2 
#que chingue asu madre el america
#NOTA: el pipiline debe debolver algo como
#id_cliente
# empresa
# industria
# score
# segmento
# recomendacion
#para que funcione
if pagina == "Resultados":
    st.header("Resultados Detallados")
    st.write(
        """Aquí puedes explorar los resultados detallados del análisis, incluyendo métricas clave, insights y recomendaciones específicas para cada cliente."""
    )
if st.session_state.resultados is not None:
    try:
        st.dataframe(st.session_state.resultados)
        st.warning("ejecuta el pipeline primer enj el dashboard")
    except:
        df = st.session_state.resultados

        st.subheader("filtros")
        col1,col2,col3 = st.columns(3)
        #separador de coplumnas porque emepizo a ver borroso

        with col1:
            score_min = st.slider("score minimo",0,100,50)
            #separador de columnas porque veo ya borroso
        with col2:
            if "industria" in df.columns:
                industria = st.selectbox(
                    "industia",
                    #el ordenamiento es un sorted de toda la vida se nesesita mejorar proximamente para asi
                   # hacerlo mas eficiente pero como ya tenemos los dias de entrega ya proximos lo mejor 
                    # es hacer esto de forma rapida y luego ya mejorar el codigo despues
                    #como con algun ordenamiento de gran escala o algo asi pero por ahora esto es lo que hay
                    #es lo mejor que puedo hacer con las pocas horas de sueño que llevo encima
                    ["todas"] + sorted(df["industria"].dropna().unique().tolist())
                )
            else:
                industria = "todas"
#separador de columnas porque ya veo borroso ( vendito autocorrecotr)
        with col3:
            if "segmento" in df.columns:
                segmento = st.selectbox(
                    "segmento",
                    ["todos"] + sorted(df["segmento"].dropna().unique().tolist())
                )
            else:
                segmento = "todos"
 #filtros y filtador NOTA: SI SON 3 COLUMANS TONOTO 
filtrado = df
#separador de anidacion porque veo borroso
if "score" in df.columns:
    filtrado = filtrado[filtrado["score"] >= score_min]
    if industria != "todas":
        #separador y que chingue asu madre el america
        filtrado = filtrado[filtrado["industria"] == industria]
    if segmento != "todos":
        #separador y que chinmgue asu madre el america
        filtrado = filtrado[filtrado["segmento"] == segmento]

#separador para la linea de resultados 
st.subheader(f"Resultados Filtrados: {len(filtrado)} clientes detectados")
st.dataframe(filtrado)


#top clientes por puntaje o score no me acuerdo como lonobmnre
#si es score todo tonoto el que escribio lo de arriba
#que chinguge asu madre el america

if "score" in df.columns:
    st.subheader("Top 10 clientes potenciales")
#le puse top 10 aca es donde lo podemos correggir pero por default asi se queda 
    top10 = df.sort_values("score", ascending=False).head(10)
    st.dataframe(top10)



#aqui empiesa la pagina 3

#el pipiline espera 
""" score 
segmento
recomendacion 
señales_clave
 """

if pagina == "Detalle Cliente":
    st.header("Detalle por Cliente")
    st.write(
        """Selecciona un cliente para ver detalles específicos, incluyendo su historial, señales de mercado relevantes y recomendaciones personalizadas."""
    )
    st.title("detalle cliente")
    
if st.session_state.resultados is None:
    st.info("Ejecuta el pipeline para ver resultados.")
else:
    df = st.session_state.resultados

#esto son las posibles selecciones del cleinte para teomar ne cuenta en 
# caso de que agregos alguna mas adelante
if "empresa" in df.columns:
    cliente_nombre = st.selectbox(
        "Selecciona una empresa",
        df["empresa"].unique()
    )
    #al chile no se que hace el iloc pero me lo sugirio el vscode y funciona asi que no cuestiono
    #que cihnge asu madle el america
    cliente = df[df["empresa"] == cliente_nombre].iloc[0]
else: 
    cliente_id = st.selectbox(
        "selecciona un cliente (id)",
        df.index
        )
    cliente = df.loc[cliente_id]
    st.divider()

#info principal del cliente seleccionado

col1,col2,col3 = st.columns(3)
with col1:
    st.metric("score", cliente.get("score","--"))
with col2:
    st.metric("industria", cliente.get("industria","--"))
with col3:
    st.metric("segmento", cliente.get("segmento","--"))

#recomendacion de venta 
st.subheader("recomendacion de venta HPE")

recomendacion = cliente .get("recomendacion","sin recomendacion aun")
st.success(recomendacion)

#explicacion con la IA que aun no tenemos hecha a la fecha que escribo esto
#pido ayuda a dios o al santanas lo que ayude primero para que esto funcione pero proximamente se agregara una explicacion detallada de porque se hizo esa recomendacion y cuales fueron las señales o datos que mas influyeron en esa recomendacion
#resuman de la nota esa 
#MUCHO TEXTO
st.subheader("explicacion de la recomendacion")
if "señales_clave" in df.columns:
    st.write(cliente["señales_clave"])
else:
    st.info("""Explicación detallada próximamente...
            mentiraaaa 
            el score se calcula usando:
            * señales de crecimiento
            *historial de compras 
            *tamaño de la empresa 
            * interes en productos tecnologicos
            * y mas señales que se iran agregando proximamente
            """)

#detalles completo de finalizacion finalizado final
st.subheader("datos completos del cliente")
st.json(cliente.to_dict())

#ejemplo de señales clave que entrega es mas del tipo
# Expancion reciente + alto interes + compras previas = señales de crecimiento


# aca empieza la pagina 4

if pagina == "Gráficas":
    st.header("Gráficas e Insights")
    st.write(
        """Visualiza gráficas interactivas que muestran tendencias, distribuciones y relaciones clave entre las variables analizadas para obtener insights profundos sobre tus clientes."""
    )
st.title("Visualización del Modelo")

if st.session_state.resultados is None:
        st.warning("Ejecuta el pipeline primero.")
else:
        df = st.session_state.resultados

        st.subheader("Distribución de Scores")

        if "score" in df.columns:
            st.bar_chart(df["score"])
        else:
            st.info("No hay columna score aún.")

        st.divider()

        st.subheader("Clientes por Industria")

        if "industria" in df.columns:
            conteo = df["industria"].value_counts()
            st.bar_chart(conteo)
        else:
            st.info("No hay columna industria.")

        st.divider()

        st.subheader("Segmentos de Clientes")

        if "segmento" in df.columns:
            conteo = df["segmento"].value_counts()
            st.bar_chart(conteo)
        else:
            st.info("No hay columna segmento.")

        st.divider()

        st.subheader("Top 10 Clientes por Score")

        if "score" in df.columns:
            top = df.sort_values("score", ascending=False).head(10)
            st.dataframe(top)
#el pipiline nesesita devolver esto :3 
"""
empresa
industria
score
segmento
recomendacion
"""
# y opcional esto :3
"""
tipo_evento
impacto
señales_clave
"""

# aca empeiza la pagina 5 y la final para ya dormir
# bendito sea el chatgpt para esto neta 

if pagina == "Exportar":

    st.title("Exportar Resultados")

    if st.session_state.resultados is None:
        st.warning("Ejecuta el pipeline primero.")
    else:
        df = st.session_state.resultados

        st.success(f"{len(df)} clientes listos para exportar")

        st.divider()

        # ==========================
        # EXPORTAR CSV
        # ==========================
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="clientes_analizados.csv",
            mime="text/csv"
        )

        # ==========================
        # EXPORTAR EXCEL
        # ==========================
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Resultados")

        st.download_button(
            label="Descargar Excel",
            data=output.getvalue(),
            file_name="clientes_analizados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.divider()

        # ==========================
        # REPORTE RESUMEN
        # ==========================
        st.subheader("Reporte Ejecutivo")

        total = len(df)
        top = df.sort_values("score", ascending=False).head(5)

        reporte = f"""
REPORTE IA HPE
Fecha: {datetime.now().strftime('%Y-%m-%d')}

Total clientes analizados: {total}

Top 5 clientes:
{top[['empresa','score','segmento','recomendacion']].to_string(index=False)}

Conclusión:
Se identificaron clientes con alta probabilidad de compra
usando señales de mercado, historial y scoring automático.
        """

        st.text_area("Vista previa", reporte, height=250)

        st.download_button(
            label="Descargar Reporte TXT",
            data=reporte,
            file_name="reporte_hpe.txt"
        )
# el pipiline nesesita debolber esto 
"""
empresa
score
segmento
recomendacion
"""