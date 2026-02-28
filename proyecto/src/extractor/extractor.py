import pandas as pd
import numpy as np

def log(msg):
    print(f'[Extractor V2] {msg}')

# Extensión de pesos de decisión para el scraping
PESO_EVENTO = {
    "expansion": 3,
    "nueva inversion": 3,
    "crecimiento ventas": 1.5,
    "tecnologia cloud": 4,  # es una venta segura según el estándar HPE
    "despidos": -2,
    "problemas legal": -4
}

def extraer_senales(clientes, eventos, historial):
    log("Iniciando extracción con lógica de señales de intención...")
    log("por favor sea paciente")

    # ========================================
    # ERRORES CORREGIDOS:
    # 1. 'id_clientes' → 'id_cliente' (estandarización)
    # ========================================
    for df in [clientes, eventos, historial]:
        if 'id_clientes' in df.columns:
            df.rename(columns={'id_clientes': 'id_cliente'}, inplace=True)
        if 'id' in df.columns and 'id_cliente' not in df.columns:
            df.rename(columns={'id': 'id_cliente'}, inplace=True)  # ✅ Corregido espacio

    # Asumimos que hoy es la fecha máxima en eventos
    if not eventos.empty and 'fecha' in eventos.columns:
        eventos['fecha'] = pd.to_datetime(eventos['fecha'])
        max_fecha = eventos['fecha'].max()
        eventos['factor_recencia'] = eventos['fecha'].apply(
            lambda x: max(0.5, 1 - (max_fecha - x).days / 365)
        )
    else:
        eventos['factor_recencia'] = 1.0

    # ========================================
    # ERRORES CORREGIDOS:
    # 2. Función check_hpe_intent NO USADA → Eliminada
    # 3. keywords_hpe movido fuera de función
    # 4. detectar_intencion_hpe corregida
    # ========================================
    keywords_hpe = ['cloud', 'hibrid', 'server', 'greenlake', 'edge', 'storage']

    def detectar_intencion_hpe(row):
        texto = str(row.get('descripcion', '')).lower()
        puntos = sum(1.5 for word in keywords_hpe if word in texto)
        return puntos

    # Eventos map 
    eventos["peso_evento"] = eventos["tipo de evento"].map(PESO_EVENTO).fillna(0)
    eventos["bonus_hpe"] = eventos.apply(detectar_intencion_hpe, axis=1)  # ✅ axis=1 agregado
    eventos["score_final"] = eventos["peso_evento"] * eventos["factor_recencia"]
    eventos["score_total_eventos"] = eventos["peso_evento"] + eventos["bonus_hpe"]  # ✅ Corregido nombre columna

    # ========================================
    # ERRORES CORREGIDOS:
    # 5. DUPLICACIÓN de eventos_agg → Eliminada
    # 6. "score_total_evento" → "score_total_eventos"
    # ========================================
    eventos_agg = eventos.groupby("id_cliente")["score_total_eventos"].agg(['sum', 'count']).reset_index()
    eventos_agg.rename(columns={"sum": "score_eventos", "count": "volumen_noticias"}, inplace=True)

    # Intento de hacer un calculador de "lealtad"
    # ========================================
    # ERRORES CORREGIDOS:
    # 7. .egg() → .agg()
    # 8. Sintaxis lambda corregida
    # 9. rename corregido
    # ========================================
    if not historial.empty:
        historial_agg = historial.groupby("id_cliente").agg({
            "compras_previas": "sum",
            "contactos_previos": "mean",  # frecuencia de contacto
            "respuesta_email": lambda x: (x == "POSITIVA").sum() - (x == "NEGATIVA").sum()
        }).reset_index()
        historial_agg.rename(columns={"respuesta_email": "sentimiento_cliente"}, inplace=True)  # ✅ Corregido nombre
    else:
        historial_agg = pd.DataFrame()

    # Clientes y segmentación por tamaño
    # Estandarización de ingresos
    clientes["score_interes"] = clientes["interes_producto"].map({
        "Alta": 3, "Media": 1, "Baja": -1, "Nulo": 0
    }).fillna(0)
    
    if "ingresosAP" in clientes.columns:
        clientes["ingresos_log"] = np.log1p(clientes["ingresosAP"])

    # ========================================
    # ERRORES CORREGIDOS:
    # 10. Nombres de columnas inconsistentes ('idcliente' vs 'id_cliente')
    # 11. DUPLICACIÓN de merges → Simplificado
    # 12. features redefinido múltiples veces
    # ========================================
    # Merge final reforzado
    features = clientes.copy()
    features = features.merge(eventos_agg, on="id_cliente", how="left")
    if not historial_agg.empty:
        features = features.merge(historial_agg, on="id_cliente", how="left")

    # Relleno inteligente
    # ========================================
    # ERRORES CORREGIDOS:
    # 13. Espacios en select_dtypes
    # 14. DUPLICACIÓN de fillna → Consolidado
    # ========================================
    columnas_numericas = features.select_dtypes(include=[np.number]).columns
    features[columnas_numericas] = features[columnas_numericas].fillna(features[columnas_numericas].median())
    features = features.fillna(0)  # Relleno de seguridad final

    log(f"Extracción finalizada: {len(features)} perfiles generados.")
    return features
