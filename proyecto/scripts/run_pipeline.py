"""
run_pipeline.py
pipeline principal del sistema IA HPE
Equipo Devcode
"""

import time
import pandas as pd

from src.recolector.recolector import carga_datos
from src.extractor.extractor import extraer_senales
from src.scoring.scoring import calcular_score
from src.clasificador.modelo import clasificar_clientes
from src.recomendador.recomendador import recomendar_hpe
from src.salida.reportes import guardar_resultados
from src.speech.speech import generar_speech


def log_paso(nombre):
    print("\n" + "=" * 50)
    print(f"Ejecutando modulo: {nombre}")


def run_pipeline(config):
    inicio_total = time.time()

    try:
        log_paso("1. Recolector")
        clientes, eventos, historial = carga_datos(config)

        log_paso("2. Extractor")
        features = extraer_senales(clientes, eventos, historial)

        log_paso("3. Scoring")
        scores = calcular_score(features)

        log_paso("4. Clasificador")
        segmentos = clasificar_clientes(scores)

        log_paso("5. Recomendador")
        recomendaciones = recomendar_hpe(segmentos)

        log_paso("6. Speech")
        speech = generar_speech(recomendaciones)

        log_paso("7. Combinar resultados")
        df_final = pd.concat(
            [recomendaciones.reset_index(drop=True),
             speech.reset_index(drop=True)],
            axis=1
        )

        log_paso("8. Guardar resultados")
        guardar_resultados(df_final, config)

        fin_total = time.time()
        print(f"\nPipeline completado en {fin_total - inicio_total:.2f} segundos")

        return df_final

    except Exception as e:
        print(f"Error en pipeline: {e}")
        raise


if __name__ == "__main__":
    config = {
        "data_path": "data/synthetic/",
        "output_path": "results/",
        "modo": "test"
    }
    run_pipeline(config)