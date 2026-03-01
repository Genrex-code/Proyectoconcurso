import pandas as pd
import numpy as np

def log(msg):
    print(f'[Extractor V2] {msg}')

PESO_EVENTO = {
    "expansion": 3,
    "nueva inversion": 3,
    "crecimiento ventas": 1.5,
    "tecnologia cloud": 4,
    "despidos": -2,
    "problemas legal": -4
}

def extraer_senales(clientes, eventos, historial):
    log("Iniciando extracción con lógica de señales de intención...")
    log("por favor sea paciente")
    
    # 0. Inicializar features
    features = clientes.copy()
    
    # 1. Estandarización de IDs
    for df in [features, eventos, historial]:
        if 'id_clientes' in df.columns:
            df.rename(columns={'id_clientes': 'id_cliente'}, inplace=True)
        if 'id' in df.columns and 'id_cliente' not in df.columns:
            df.rename(columns={'id': 'id_cliente'}, inplace=True)

    # 2. Manejo de fechas y recencia
    if not eventos.empty and 'fecha' in eventos.columns:
        eventos['fecha'] = pd.to_datetime(eventos['fecha'])
        max_fecha = eventos['fecha'].max()
        eventos['factor_recencia'] = eventos['fecha'].apply(
            lambda x: max(0.5, 1 - (max_fecha - x).days / 365)
        )
    else:
        eventos['factor_recencia'] = 1.0

    # 3. Keywords HPE y procesamiento de eventos
    keywords_hpe = ['cloud', 'hibrid', 'server', 'greenlake', 'edge', 'storage']
    
    def detectar_intencion_hpe(row):
        texto = str(row.get('descripcion', '')).lower()
        return sum(1.5 for word in keywords_hpe if word in texto)

    # ❌ BUG1: Código DUPLICADO eliminado
    # Usar columna correcta del CSV (tipo_evento)
    eventos["peso_evento"] = eventos["tipo_evento"].map(PESO_EVENTO).fillna(0)
    eventos["bonus_hpe"] = eventos.apply(detectar_intencion_hpe, axis=1)
    eventos["score_total_eventos"] = (eventos["peso_evento"] * eventos["factor_recencia"]) + eventos["bonus_hpe"]

    # 4. Agregación de eventos
    eventos_agg = eventos.groupby("id_cliente")["score_total_eventos"].agg(['sum', 'count']).reset_index()
    eventos_agg.rename(columns={"sum": "score_eventos", "count": "volumen_noticias"}, inplace=True)

    # 5. Historial y Lealtad
    if not historial.empty:
        historial_agg = historial.groupby("id_cliente").agg({
            "compras_previas": "sum",
            "contactos_previos": "mean",
            "respuesta_email": lambda x: (x.str.upper() == "POSITIVA").sum() - (x.str.upper() == "NEGATIVA").sum()
        }).reset_index()
        historial_agg.rename(columns={"respuesta_email": "sentimiento_cliente"}, inplace=True)
    else:
        historial_agg = pd.DataFrame()

    # 6. Features de clientes
    features["score_interes"] = features["interes_producto"].map({
        "Alto": 3, "Medio": 1, "Bajo": -1, "Alta": 3, "Media": 1, "Baja": -1
    }).fillna(0)
    
    # Soporte para ambas columnas de ingresos
    if "ingresos_anuales" in features.columns:
        features["ingresos_log"] = np.log1p(features["ingresos_anuales"])
    elif "ingresosAP" in features.columns:
        features["ingresos_log"] = np.log1p(features["ingresosAP"])

    # 7. Crear columna 'segmento' PARA EL DISCURSO
    if 'tamano_empresa' in features.columns:
        features['segmento'] = features['tamano_empresa'].map({
            'Grande': 'ENTERPRISE', 'Mediana': 'ENTERPRISE', 'Pequeña': 'PYME'
        }).fillna('PYME')
    else:
        features['segmento'] = 'PYME'

    # 8. Merge final consolidado
    features = features.merge(eventos_agg, on="id_cliente", how="left")
    if not historial_agg.empty:
        features = features.merge(historial_agg, on="id_cliente", how="left")

    # 9. Relleno inteligente
    columnas_numericas = features.select_dtypes(include=[np.number]).columns
    features[columnas_numericas] = features[columnas_numericas].fillna(0)
    features = features.fillna('')

    log(f"Extracción finalizada: {len(features)} perfiles generados.")
    return features
