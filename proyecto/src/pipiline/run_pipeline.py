import pandas as pd
import logging
from proyecto.src.utils.my_config import config

# Imports directos confiando en la jerarquía de carpetas
from src.recolector.recolector_main import carga_datos
from src.extractor.extractor import extraer_senales
from src.scoring.scoringGen import generar_scoreing_heuristioco
from src.recomendador.recomendador import generar_recomendaciones_expertas
from src.speech.speech_Gen import generar_speech_personalizado

def ejecutar_pipeline_completo(config_pesos):
    try:
        # Preparamos la config para el recolector
        # Convertimos Path a string para evitar errores de tipo
        config_recoleccion = {
            "input_type": "local", 
            "data_path": str(config["data_path"])
        }

        # 1. Recolección
        print("\n[STEP 1] Recolectando datos de mercado...")
        datos_crudos = carga_datos(config_recoleccion)
        
        if datos_crudos is None:
            print("❌ ERROR: El recolector no devolvió datos.")
            return None

        # 2. Extracción de Features
        print("[STEP 2] Extrayendo variables numéricas y sentimiento...")
        # Desempaquetamos el diccionario que viene del recolector
        df_features = extraer_senales(
            clientes=datos_crudos['clientes'],
            eventos=datos_crudos['eventos'],
            historial=datos_crudos['historial']
        )
        
        # 3. Scoring Heurístico
        print("[STEP 3] Aplicando lógica de negocio (3 Capas)...")
        df_scores = generar_scoreing_heuristioco(df_features, config_pesos)
        
        # 4. Recomendación de Producto
        print("[STEP 4] Mapeando portafolio de infraestructura HPE...")
        df_estrategia = generar_recomendaciones_expertas(df_scores)
        
        # 5. Generación de Speech
        print("[STEP 5] Redactando guiones de venta personalizados...")
        df_final = generar_speech_personalizado(df_estrategia)
        
        # Merge final
        return pd.merge(df_estrategia, df_final, on="id_cliente")

    except Exception as e:
        print(f"❌ Error crítico en el Pipeline: {e}")
        return None