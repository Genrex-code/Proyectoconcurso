"""
extractor.py
convierte datos crudos en features para scoring
sistema IA HPE
"""

import pandas as pd 

def log (msg):
    print(f'[extractor] {msg}')

PESO_EVENTOS = {
    "expansion": 2,
    "nueva inversion": 2,
    "crecimiento ventas":1,
    "despidos":-2,
    "problema legar":-3
    }

PESO_INTERES = {
    "Alta": 2,
    "Media": 1,
    "Baja": -1,
    "Nulo":0
}

PESO_RESPUESTA = {
    "Positiva": 1,
    "Neutral": 0,
    "Negativa": -1
}
"""
funcionamiento principal
"""
def extraer_senales(clientes, eventos, historial):

    log("Iniciando extracción de señales")

    # -------- EVENTOS --------
    eventos["peso_evento"] = eventos["tipo_evento"].map(PESO_EVENTOS).fillna(0)

    eventos_agg = eventos.groupby("id_cliente")["peso_evento"].sum().reset_index()
    eventos_agg.rename(columns={"peso_evento": "score_eventos"}, inplace=True)

    log("Eventos procesados")

    # -------- HISTORIAL --------
    historial["peso_respuesta"] = historial["respuesta_email"].map(PESO_RESPUESTA).fillna(0)

    historial_agg = historial.groupby("id_cliente").agg({
        "compras_previas": "sum",
        "contactos_previos": "sum",
        "peso_respuesta": "sum"
    }).reset_index()

    log("Historial procesado")

    # -------- CLIENTES --------
    clientes["score_interes"] = clientes["interes_producto"].map(PESO_INTERES).fillna(0)

    clientes_feat = clientes[[
        "id_clientes",
        "score_interes",
        "ingresosAP"
    ]].rename(columns={"id_clientes": "id_cliente"})

    log("Clientes procesados")

    # -------- MERGE FINAL --------
    features = clientes_feat.merge(eventos_agg, on="id_cliente", how="left")
    features = features.merge(historial_agg, on="id_cliente", how="left")

    features = features.fillna(0)

    log(f"Features generadas: {len(features)} clientes")

    return features