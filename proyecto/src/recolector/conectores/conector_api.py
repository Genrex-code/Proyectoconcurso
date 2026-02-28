import pandas as pd
import requests
import logging
import time
from typing import Dict, List, Tuple, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

def validar_config(config: Dict[str, Any]) -> None:
    """Valida que la configuración tenga todos los campos obligatorios."""
    campos_requeridos = ["api_endpoint", "api_key", "client_ids"]
    
    for campo in campos_requeridos:
        if campo not in config or not config[campo]:
            raise ValueError(
                f"Falta campo obligatorio en config: '{campo}'. "
                f"Valor recibido: {config.get(campo, 'None')}"
            )
    
    if not isinstance(config["client_ids"], list):
        raise ValueError("client_ids debe ser una lista")
    
    if not config["client_ids"]:
        raise ValueError("client_ids no puede estar vacío")

def crear_session_robusta() -> requests.Session:
    """Crea una sesión HTTP con retry automático y timeouts."""
    session = requests.Session()
    
    # Configurar retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def normalizar_respuesta(data: Dict[str, Any], client_id: str) -> Dict[str, Any]:
    """Normaliza la respuesta de la API a estructura estándar."""
    try:
        return {
            "id_cliente": str(client_id),
            "ingresos_est": data.get("revenue_range", ""),
            "empleados": data.get("employees", 0),
            "tech_stack": str(data.get("tech_stack", [])),
            "fecha_consulta": pd.Timestamp.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error normalizando respuesta para {client_id}: {e}")
        return {
            "id_cliente": str(client_id),
            "ingresos_est": "",
            "empleados": 0,
            "tech_stack": "",
            "fecha_consulta": pd.Timestamp.now().isoformat()
        }

def manejar_rate_limit(response: requests.Response, headers: Dict[str, str], 
                      params: Dict[str, str], session: requests.Session) -> requests.Response:
    """Manejo inteligente de rate limiting."""
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 5))
        logger.warning(f"⚠️ Rate limit (429). Esperando {retry_after}s...")
        time.sleep(retry_after)
        
        # Reintentar una vez más
        response = session.get(
            response.url, 
            headers=headers, 
            params=params, 
            timeout=15
        )
    
    return response

def cargar(config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Conector robusto para APIs externas de inteligencia comercial.
    
    Args:
        config: Diccionario con:
            - api_endpoint (str): URL base de la API
            - api_key (str): Token de autenticación
            - client_ids (List[str]): Lista de IDs a consultar
    
    Returns:
        Tuple[DataFrame, DataFrame, DataFrame]: (clientes, eventos, historial)
    """
    # Validar entrada
    try:
        validar_config(config)
    except ValueError as e:
        logger.error(f"❌ Configuración inválida: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    endpoint = config["api_endpoint"]
    api_key = config["api_key"]
    ids = config["client_ids"]
    
    # Validar URL
    if not endpoint.startswith(('http://', 'https://')):
        logger.error(f"❌ URL inválida: {endpoint}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "HPE-IA-Analytics/1.0"
    }
    
    session = crear_session_robusta()
    resultados = []
    exitosos = 0
    
    logger.info(f"[API Connector] Iniciando consulta para {len(ids)} clientes...")
    
    for i, client_id in enumerate(ids, 1):
        try:
            logger.debug(f"Procesando cliente {i}/{len(ids)}: {client_id}")
            
            params = {
                "id": str(client_id), 
                "fields": "tech_stack,revenue_range,employees"
            }
            
            response = session.get(
                endpoint, 
                headers=headers, 
                params=params, 
                timeout=15
            )
            
            # Manejo específico de rate limiting
            response = manejar_rate_limit(response, headers, params, session)
            
            # Verificar status
            if not response.ok:
                logger.error(f"❌ HTTP {response.status_code} para {client_id}")
                continue
            
            # Parse JSON seguro
            try:
                data = response.json()
            except ValueError as e:
                logger.error(f"❌ Respuesta no JSON para {client_id}: {e}")
                continue
            
            # Normalizar y agregar resultado
            resultado = normalizar_respuesta(data, client_id)
            resultados.append(resultado)
            exitosos += 1
            
            logger.debug(f"✅ Cliente {client_id} procesado correctamente")
            
        except requests.exceptions.Timeout:
            logger.error(f"⏰ Timeout para cliente {client_id}")
        except requests.exceptions.ConnectionError:
            logger.error(f"🌐 Error de conexión para cliente {client_id}")
        except Exception as e:
            logger.error(f"❌ Error inesperado para {client_id}: {str(e)}")
        finally:
            # Pequeña pausa entre requests
            time.sleep(0.1)
    
    logger.info(f"[API Connector] Completado: {exitosos}/{len(ids)} exitosos")
    
    if not resultados:
        logger.warning("⚠️ No se obtuvieron datos válidos")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    # Crear DataFrames
    try:
        df_api = pd.DataFrame(resultados)
        logger.info(f"📊 DataFrame creado: {len(df_api)} registros")
        return df_api, pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        logger.error(f"❌ Error creando DataFrame: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
