import pandas as pd
import requests
import logging
import time

logger = logging.getLogger(__name__)

def cargar(config: dict):
    """
    Conector robusto para APIs externas de inteligencia comercial.
    Se espera en config: 
    - api_endpoint: URL base
    - api_key: Token de autenticación
    - client_ids: Lista de IDs a consultar
    """
    endpoint = config.get("api_endpoint")
    api_key = config.get("api_key")
    ids = config.get("client_ids", [])
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "HPE-IA-Analytics/1.0"
    }

    resultados = []
    
    logger.info(f"[API Connector] Iniciando consulta para {len(ids)} clientes.")

    for client_id in ids:
        try:
            # Ejemplo de consulta: buscando stack tecnológico y tamaño de empresa
            # Usamos params para no ensuciar la URL
            params = {"id": client_id, "fields": "tech_stack,revenue_range,employees"}
            
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            
            # Manejo de Rate Limiting (Error 429)
            if response.status_code == 429:
                logger.warning("⚠️ Rate limit alcanzado. Esperando 5 segundos...")
                time.sleep(5)
                response = requests.get(endpoint, headers=headers, params=params, timeout=10)

            response.raise_for_status()
            data = response.json()
            
            # Normalizamos la respuesta de la API a nuestra estructura
            resultados.append({
                "id_cliente": client_id,
                "ingresos_est": data.get("revenue_range"),
                "empleados": data.get("employees"),
                "tech_stack": str(data.get("tech_stack", [])), # Convertir lista a string para DF
                "fecha_consulta": pd.Timestamp.now()
            })

        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ Error HTTP para cliente {client_id}: {e}")
            continue # Seguimos con el siguiente cliente
        except Exception as e:
            logger.error(f"❌ Error inesperado en API para cliente {client_id}: {e}")
            continue

    if not resultados:
        logger.warning("⚠️ La API no devolvió datos válidos para los IDs proporcionados.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # Convertimos a DataFrame para el Extractor
    df_api = pd.DataFrame(resultados)
    
    # Siguiendo tu contrato, devolvemos (clientes, eventos, historial)
    # Aquí la API suele enriquecer la tabla de CLIENTES o EVENTOS
    return df_api, pd.DataFrame(), pd.DataFrame()