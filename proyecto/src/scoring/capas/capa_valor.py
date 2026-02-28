import numpy as np


def calcular_capa_valor(df_features):
    """
    Analiza la capacidad financiera del cliente.
    
    Args:
        df_features (pd.DataFrame): DataFrame con features del extractor.
                                   Requiere columna 'ingresos_log'
    
    Returns:
        pd.Series: Score financiero normalizado [0-100]
                   50.0 si no hay datos o error
        
    Proceso:
        1. Verifica existencia de 'ingresos_log'
        2. Normaliza valores entre 0-100 usando min-max scaling
        3. Retorna 50.0 (neutro) si datos insuficientes
    """
    try:
        # Verificar columna requerida 
        if "ingresos_log" not in df_features.columns:
            return 50.0  # Valor neutro placeholder
    
        # Extraer columna de ingresos  
        ingresos = np.asarray(df_features["ingresos_log"])
        
        # Normalización rápida 0-100 basada en datos del dataset 
        v_min = ingresos.min()
        v_max = ingresos.max()
        
        # Evitar división por cero 
        if v_max == v_min:
            return 50.0
        
        # Calcular score normalizado [0,100] 
        score = 100 * (ingresos - v_min) / (v_max - v_min)
        
        # Rellenar NaN con valor neutro
        return np.where(np.isnan(score), 50.0, score)  # Más eficiente que fillna
    
    except Exception:
        # Retorna neutro ante cualquier error
        return 50.0
