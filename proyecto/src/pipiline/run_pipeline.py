# import pandas as pd
# import logging
# # from recolector.recolector_main import carga_datos
# # from proyecto.src.extractor.extractor import extraer_senales
# # from proyecto.src.scoring.scoringGen import generar_scoreing_heuristioco # Respetando tu typo ;)
# # from proyecto.src.recomendador.recomendador import generar_recomendaciones_expertas
# # from proyecto.src.speech.speech_Gen import generar_speech_personalizado

# import os
# import sys
# from pathlib import Path

# # 1. Detectamos la carpeta raíz del proyecto (donde está main.py)
# BASE_DIR = Path(__file__).resolve().parent

# # 2. Agregamos la raíz al "mapa" de búsqueda de Python
# if str(BASE_DIR) not in sys.path:
#     sys.path.insert(0, str(BASE_DIR))

# # 3. Ahora sí, hacemos los imports desde la carpeta 'src'
# try:
#     from src.recolector.recolector_main import carga_datos
#     from src.extractor.extractor import extraer_senales
#     from src.scoring.scoringGen import generar_scoreing_heuristioco
#     from src.recomendador.recomendador import generar_recomendaciones_expertas
#     from src.speech.speech_Gen import generar_speech_personalizado
#     print("✅ Módulos cargados exitosamente.")
# except ModuleNotFoundError as e:
#     print(f"❌ Error de importación: {e}")
#     print(f"🔍 Python está buscando en: {sys.path[0]}")


    
# def ejecutar_pipeline_completo(config_pesos):
#     """
#     Coordina el flujo desde la recolección hasta el guion de venta.
#     """
#     try:
#         # --- ARREGLO AQUÍ ---
#         # Creamos la configuración que el recolector_main.py espera
#         config_recoleccion = {
#             "input_type": "local", 
#             "data_path": "proyecto/data/synthetic"}#ruta para pruebas

#         # 1. Recolección
#         print("\n[STEP 1] Recolectando datos de mercado...")
#         datos_crudos = carga_datos(config_recoleccion)
#         # Validamos que no sea None antes de seguir
#         if datos_crudos is None:
#             print("❌ ERROR CRÍTICO: El recolector no encontró datos. Revisa la ruta 'proyecto/data/synthetic'")
#             return None
#         # 2. Extracción de Features
#         print("[STEP 2] Extrayendo variables numéricas y sentimiento...")
#         df_features = extraer_senales(
#         clientes=datos_crudos['clientes'],
#         eventos=datos_crudos['eventos'],
#         historial=datos_crudos['historial']
#         )
        
#         # 3. Scoring Heurístico
#         print("[STEP 3] Aplicando lógica de negocio (3 Capas)...")
#         df_scores = generar_scoreing_heuristioco(df_features, config_pesos)
        
#         # 4. Recomendación de Producto
#         print("[STEP 4] Mapeando portafolio de infraestructura HPE...")
#         df_estrategia = generar_recomendaciones_expertas(df_scores)
        
#         # 5. Generación de Speech
#         print("[STEP 5] Redactando guiones de venta personalizados...")
#         df_final = generar_speech_personalizado(df_estrategia)
        
#         # Retornamos el merge de todo para el CLI
#         return pd.merge(df_estrategia, df_final, on="id_cliente")

#     except Exception as e:
#         print(f" Error en el Pipeline: {e}")
#         return None

# proyecto/src/pipiline/run_pipeline.py
import pandas as pd
import logging

# Importes limpios y directos (sin sys.path hacks)
from src.recolector.recolector_main import carga_datos
from src.extractor.extractor import extraer_senales
from src.scoring.scoringGen import generar_scoreing_heuristioco 
from src.recomendador.recomendador import generar_recomendaciones_expertas
from src.speech.speech_Gen import generar_speech_personalizado

# Importamos tu configuración global absoluta (my_config.py)
from src.utils.my_config import config 

def ejecutar_pipeline_completo(config_pesos):
    try:
        # Usamos la ruta absoluta y blindada de my_config.py
        config_recoleccion = {
            "input_type": "local", 
            "data_path": str(config["data_path"]) # str() asegura que sea texto
        }

        # 1. Recolección
        print("\n[STEP 1] Recolectando datos de mercado...")
        datos_crudos = carga_datos(config_recoleccion)
        
        if datos_crudos is None:
            print("❌ ERROR: El recolector no encontró datos.")
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
        
        # 4. Recomendación
        print("[STEP 4] Mapeando portafolio HPE...")
        df_estrategia = generar_recomendaciones_expertas(df_scores)
        
        # 5. Speech
        print("[STEP 5] Redactando guiones de venta...")
        df_final = generar_speech_personalizado(df_estrategia)
        
        return pd.merge(df_estrategia, df_final, on="id_cliente")

    except Exception as e:
        print(f"❌ Error crítico en el Pipeline: {e}")
        return None