# src/recolector/recolector_main.py

import logging
import traceback
from typing import Any, Dict, Optional

# Configurar logging básico si no existe
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
except Exception:
    print("Advertencia: No se pudo configurar logging")

logger = logging.getLogger(__name__)

def validar_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida que la configuración tenga los campos requeridos.
    """
    tipo_entrada = config.get("input_type", "local")
    
    configuraciones_requeridas = {
        "local": ["data_path"],
        "url": ["url_fuente"],
        "scraping": ["url_empresa"],
        "datasets_limpios": ["data_path"],
        "api": ["api_endpoint", "api_key", "client_ids"]  # Agregado
    }
    
    campos_requeridos = configuraciones_requeridas.get(tipo_entrada, [])
    
    for campo in campos_requeridos:
        if not config.get(campo):
            raise ValueError(
                f"Configuración inválida para '{tipo_entrada}': "
                f"falta el campo obligatorio '{campo}'"
            )
    
    return config

def carga_datos(config: Optional[Dict[str, Any]] = None) -> Optional[Any]:
    """
    Orquestador principal que selecciona la fuente según la config.
    Versión robusta con manejo completo de errores.
    """
    if config is None:
        config = {
            "input_type": "local",
            "data_path": "proyecto/data/synthetic" # Asegúrate que esta ruta exista
        }

    if not isinstance(config, dict):
        raise TypeError("La configuración debe ser un diccionario")
    
    tipo_entrada = None  # Inicializar para el except final
    
    try:
        # Validar configuración primero
        config_validada = validar_config(config)
        tipo_entrada = config_validada.get("input_type", "local")
        
        logger.info(f"[Recolector] Modo de entrada detectado: {tipo_entrada}")
        
        # Importar conectores con manejo de errores
        try:
            from .conectores import (
                conector_local, 
                conector_url, 
                conector_scraping,
                conector_api  # Importar conector_api
            )
        except ImportError as e:
            logger.error(f"Error importando conectores: {e}")
            logger.error(traceback.format_exc())
            raise ImportError(
                "No se pudieron importar los conectores. "
                "Verifica que los módulos existan en src/recolector/conectores/"
            )
        
        # Mapa de conectores para fácil mantenimiento
        conectores = {
            "local": conector_local.cargar,
            "url": conector_url.cargar,
            "scraping": conector_scraping.cargar,
            "datasets_limpios": conector_local.cargar,
            "api": conector_api.cargar,  # Corregido aquí
        }
        
        conector_func = conectores.get(tipo_entrada)
        if not conector_func:
            raise ValueError(
                f"Tipo de entrada '{tipo_entrada}' no soportado. "
                f"Opciones válidas: {list(conectores.keys())}"
            )
        
        # Llamar al conector correspondiente
        resultado = conector_func(config_validada)
        
        if resultado is None:
            logger.warning(f"Conector '{tipo_entrada}' devolvió None")
        
        logger.info(f"[Recolector] Datos cargados exitosamente con {tipo_entrada}")
        return resultado
        
    except ValueError as e:
        logger.error(f"Error de configuración: {e}")
        raise
    except ImportError as e:
        logger.error(f"Error de importación: {e}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado en carga_datos: {e}")
        logger.error(traceback.format_exc())
        raise Exception(
            f"Error crítico al cargar datos con '{tipo_entrada}': {str(e)}"
        )
