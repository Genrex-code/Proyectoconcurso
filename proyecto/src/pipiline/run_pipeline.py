import pandas as pd
import logging
from src.recolector.recolector_main import recolectar_datos
from src.extractor.extractor import extraer_features
from src.scoring.scoringGen import generar_scoreing_heuristioco # Respetando tu typo ;)
from src.recomendador.recomendador import generar_recomendaciones
from src.speech.speech_Gen import generar_speech_personalizado

def ejecutar_pipeline_completo(config_pesos):
    """
    Coordina el flujo desde la recolección hasta el guion de venta.
    """
    try:
        # 1. Recolección
        print("\n[STEP 1] Recolectando datos de mercado...")
        datos_crudos = recolectar_datos()
        
        # 2. Extracción de Features
        print("[STEP 2] Extrayendo variables numéricas y sentimiento...")
        df_features = extraer_features(datos_crudos)
        
        # 3. Scoring Heurístico
        print("[STEP 3] Aplicando lógica de negocio (3 Capas)...")
        df_scores = generar_scoreing_heuristioco(df_features, config_pesos)
        
        # 4. Recomendación de Producto
        print("[STEP 4] Mapeando portafolio de infraestructura HPE...")
        df_estrategia = generar_recomendaciones(df_scores)
        
        # 5. Generación de Speech
        print("[STEP 5] Redactando guiones de venta personalizados...")
        df_final = generar_speech_personalizado(df_estrategia)
        
        # Retornamos el merge de todo para el CLI
        return pd.merge(df_estrategia, df_final, on="id_cliente")

    except Exception as e:
        print(f" Error en el Pipeline: {e}")
        return None