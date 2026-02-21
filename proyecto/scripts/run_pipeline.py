"""
run_pipeline.py
pipeline principal de lsistema de analisis de cleitnes HPE
Equipo Devcode

"""

import time

#modulos del proyecto ( sujeto a cambios)
from src.recolector.recolector import carga_datos  # recolector.py en src/
from src.extractor.extractor import extraer_senales  # extractor/extractor.py -> desde extractor/
from src.scoring.scoring import calcular_score  # scoring.py en src/
from src.clasificador.modelo import clasificar_clientes  # Ajustado a src/clasificador/modelo.py
from src.recomendador.recomendador import recomendar_hpe  # Ajustado a src/recomendador/
from src.salida.reportes import guardar_resultados  # Ajustado a src/reportes/
from run_pipeline import run_pipeline  # run_pipeline.py en scripts/

def log_paso(nombre):
    """Imprime separador bonito para debug"""
    print("\n" + "="*50)
    print(f"--> Ejecutando módulo: {nombre}")
    print("="*50)


def run_pipeline(config):
    """
    ejecucion de todo el flujo del sistema IA
    config = diccionario con rutas y parametros
    """
    inicio_total = time.time()
    try:
        log_paso("recolector")
        clientes,eventos,historial = carga_datos(config)
        
        # ---------------------------
        log_paso("2. Extractor de señales")
        features = extraer_senales(clientes, eventos, historial)

        # ---------------------------
        log_paso("3. Scoring")
        scores = calcular_score(features)

        # ---------------------------
        log_paso("4. Clasificador")
        segmentos = clasificar_clientes(scores)

        # ---------------------------
        log_paso("5. Recomendador HPE")
        recomendaciones = recomendar_hpe(segmentos)

        # ---------------------------
        log_paso("6. Salida")
        guardar_resultados(recomendaciones, config)
    except Exception as e:
        print(f"Error en ejecución del pipeline: {e}")
        raise
    fin_total = time.time()
    print(f"Pipeline completado en {fin_total - inicio_total:.2f} segundos")

if __name__ == "__main__":
    config = {
        "data_path": "data/synthetic/",
        "output_path": "results/",
        "modo": "test"
    }
    run_pipeline(config)


def test_pipeline():
    config = {
        "data_path":"tests/data",
        "output_path":"tests/output",
        "modo":"test"
    }

    run_pipeline(config)
