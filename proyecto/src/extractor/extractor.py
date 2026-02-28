import pandas as pd
import numpy as np

def log(msg):
    print(f'[Extractor V2] {msg}')

#extencion de pesos de decicion para el scrapping

PESO_EVENTO = {
    "expansion":3,
    "nueva inversion":3,
    "crecimiento ventas": 1.5,
    "tecnologia cloud":4, #es una venta segura segun el estandar HPE
    "despidos" : -2,
    "problemas legal" :-4
}

def extraer_senales(clientes,eventos,historial):
    log("Iniciando extraccion con logica de señales de intencion...")
    log("por favor sea paciente")

#mejora 1 
    #bucle para la estandarizacion de IDs (asi evitamos merge fallidos(chingue a su madre el america))
    for df in [clientes,eventos,historial]:
        if 'id_clientes' in df.columns:
            df.rename(columns={'id_clientes': 'id_cliente'}, inplace = True)
            if 'id' in df.columns and 'id_cliente' not in df.columns:
                df.rename(columns= {'id': 'id_cliente'},inplace= True)
    # Asumimos que hoy es la fecha máxima en eventos
    if not eventos.empty and 'fecha' in eventos.columns:
        eventos['fecha'] = pd.to_datetime(eventos['fecha'])
        max_fecha = eventos['fecha'].max()
        # Factor: 1.0 si es hoy, va bajando hacia 0.5 si es viejo
        eventos['factor_recencia'] = eventos['fecha'].apply(
            lambda x: max(0.5, 1 - (max_fecha - x).days / 365)
        )
    else:
        eventos['factor_recencia'] = 1.0

    #procesamineto de eventos + intencion (NPL basico)
    #no le entendi al tutorial help
    def check_hpe_intent(texto):
        texto = str(texto).lower()
        return 2.0 if any(word in texto for word in keywords_hpe) else 1.0

    def detectar_intencion_hpe(row):
        texto = str (row.get('descripcion','')).lower()
        keywords_hpe = ['cloud','hibrid','server','greenlake','edge','storage']
    
        puntos = sum(1.5 for word in keywords_hpe if word in texto)
        return puntos
    
    #eventos map 
    eventos["peso_evento"] = eventos["tipo de evento"].map(PESO_EVENTO).fillna(0)
    eventos["bonus_hpe"] = eventos.apply(detectar_intencion_hpe,axis=1)
    eventos["score_final"] = eventos["peso_evento"] * eventos["factor_recencia"]
    eventos["score_total_eventos"] = eventos ["peso_evento"] + eventos["bonus_hpe"]
# procesamiento agrupado 
    eventos_agg = eventos.groupby("id_cliente")["score_total_evento"].agg(['sum', 'count']).reset_index()
    eventos_agg.rename(columns={"sum": "score_eventos", "count": "volumen_noticias"}, inplace=True)
    eventos_agg = eventos.groupby("id_cliente")["score_final"].sum().reset_index()
    eventos_agg.rename(columns={"score_final": "score_eventos"}, inplace=True)

    #intento de hacer un calculador de "lealtad"
    historial_agg = historial.groupby("id_cliente").egg({
        "compras_previas":"sum",
        "contactos_previos":"mean", #frecuencai de contacto 
        "respuesta_email": lambda x: (x =="POSITIVA").sum() - (x == "NEGATIVA").sum()
    }).reset_index()
    historial_agg.rename(columns={"respuestas_email":"sentimiento_cliente"}, inplace=True)

    #cleintes y segmentacion por tamaño 
    #estandarizacion de ingresos
    clientes["score_interes"] = clientes["interes_producto"].map({
        "Alta":3, "Media":1,"Baja":-1, "Nulo":0
    }).fillna(0)
    if "ingresosAP" in clientes.columns:
        # Usamos logaritmo para suavizar ingresos muy dispares
        clientes["ingresos_log"] = np.log1p(clientes["ingresosAP"])

    #merge final refozardo para que no truene
    features = clientes[["idcliente","score_intereses","ingresosAP"]].copy()
    features = features.merge(eventos_agg, on="id_cliente",how="left")
    features = features.merge(historial_agg, on= "id_cliente", how="left")
    features = clientes.merge(eventos_agg, on="id_cliente", how="left")
    features = features.merge(historial_agg, on="id_cliente", how="left")
  

    #relleno inteligente no como los de mi rancho JASJASJASASJASJAS
    #intento de crear el aproximado es decir si no hay historial,
    #ponemos la media en lugar de 0 para no castigar a clientes nuevos
    
    columnas_numericas = features.select_dtypes(include =[np.number]).columns
    features[columnas_numericas] = features [columnas_numericas].fillna(0)
  # relleno de seguridad
    features = features.fillna(0)

    log(f"Extraccion finalizada: {len(features)} perfiles generados.")
    return features
