import pandas as pd
import logging
from recolector.recolector_main import carga_datos
from proyecto.src.extractor.extractor import extraer_senales
from proyecto.src.scoring.scoringGen import generar_scoreing_heuristioco # Respetando tu typo ;)
from proyecto.src.recomendador.recomendador import generar_recomendaciones_expertas
from proyecto.src.speech.speech_Gen import generar_speech_personalizado

def ejecutar_pipeline_completo(config_pesos):
    """
    Coordina el flujo desde la recolección hasta el guion de venta.
    """
    try:
        # --- ARREGLO AQUÍ ---
        # Creamos la configuración que el recolector_main.py espera
        config_recoleccion = {
            "input_type": "local", 
            "data_path": "proyecto/data/synthetic"}#ruta para pruebas

        # 1. Recolección
        print("\n[STEP 1] Recolectando datos de mercado...")
        datos_crudos = carga_datos(config_recoleccion)
        # Validamos que no sea None antes de seguir
        if datos_crudos is None:
            print("❌ ERROR CRÍTICO: El recolector no encontró datos. Revisa la ruta 'proyecto/data/synthetic'")
            return None
        # 2. Extracción de Features
        print("[STEP 2] Extrayendo variables numéricas y sentimiento...")
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
        
        # Retornamos el merge de todo para el CLI
        return pd.merge(df_estrategia, df_final, on="id_cliente")

    except Exception as e:
        print(f" Error en el Pipeline: {e}")
        return None