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

    # 1. Estandarización de IDs
    for df in [clientes, eventos, historial]:
        if 'id_clientes' in df.columns:
            df.rename(columns={'id_clientes': 'id_cliente'}, inplace=True)

    # 2. Manejo de fechas y recencia
    if not eventos.empty and 'fecha' in eventos.columns:
        eventos['fecha'] = pd.to_datetime(eventos['fecha'])
        max_fecha = eventos['fecha'].max()
        eventos['factor_recencia'] = eventos['fecha'].apply(
            lambda x: max(0.5, 1 - (max_fecha - x).days / 365)
        )
    else:
        eventos['factor_recencia'] = 1.0

    keywords_hpe = ['cloud', 'hibrid', 'server', 'greenlake', 'edge', 'storage']

    def detectar_intencion_hpe(row):
        texto = str(row.get('descripcion', '')).lower()
        return sum(1.5 for word in keywords_hpe if word in texto)

    # --- CORRECCIÓN CLAVE AQUÍ ---
    # Cambiamos "tipo de evento" por "tipo_evento" para que coincida con tu CSV
    eventos["peso_evento"] = eventos["tipo_evento"].map(PESO_EVENTO).fillna(0)
    eventos["bonus_hpe"] = eventos.apply(detectar_intencion_hpe, axis=1)
    eventos["score_total_eventos"] = (eventos["peso_evento"] * eventos["factor_recencia"]) + eventos["bonus_hpe"]

    # Agregación de eventos
    eventos_agg = eventos.groupby("id_cliente")["score_total_eventos"].agg(['sum', 'count']).reset_index()
    eventos_agg.rename(columns={"sum": "score_eventos", "count": "volumen_noticias"}, inplace=True)

    # 3. Historial y Lealtad
    if not historial.empty:
        # Aseguramos que respuesta_email se lea bien
        historial_agg = historial.groupby("id_cliente").agg({
            "compras_previas": "sum",
            "contactos_previos": "mean",
            "respuesta_email": lambda x: (x == "Positiva").sum() - (x == "Negativa").sum()
        }).reset_index()
        historial_agg.rename(columns={"respuesta_email": "sentimiento_cliente"}, inplace=True)
    else:
        historial_agg = pd.DataFrame()

    # 4. Clientes y segmentación
    # Ajustamos el mapeo a los valores de tus CSV (Alto, Medio, Bajo)
    clientes["score_interes"] = clientes["interes_producto"].map({
        "Alto": 3, "Medio": 1, "Bajo": -1
    }).fillna(0)
    
    # Cambiamos "ingresosAP" por "ingresos_anuales" según tu foto
    if "ingresos_anuales" in clientes.columns:
        clientes["ingresos_log"] = np.log1p(clientes["ingresos_anuales"])

    # Merge final
    features = clientes.copy()
    features = features.merge(eventos_agg, on="id_cliente", how="left")
    if not historial_agg.empty:
        features = features.merge(historial_agg, on="id_cliente", how="left")

    # Relleno de nulos para que el modelo no truene
    columnas_numericas = features.select_dtypes(include=[np.number]).columns
    features[columnas_numericas] = features[columnas_numericas].fillna(0)

    log(f"Extracción finalizada: {len(features)} perfiles generados.")
    return features