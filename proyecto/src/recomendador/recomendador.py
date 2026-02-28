import pandas as pd 
from recomendador.productos.catalogo_hpe import CATALOGO

def generar_recomendaciones(df_scoring):
    """
    Cabeza de búsqueda que asigna productos basados en los scores de las capas.
    """
    recomendaciones = []

    for _, row in df_scoring.iterrows():
        id_cliente = row['id_cliente']
        valor = row['detalle_valor']
        intencion = row['detalle_intencion']
        relacion = row['detalle_relacion']
        
        # 1. Determinamos el Segmento (Cabeza de Búsqueda de Valor)
        segmento = "ENTERPRISE" if valor > 60 else "PYME"
        
        # 2. Selección de Oferta Principal
        # Si la intención es alta, buscamos algo específico del segmento
        if intencion > 70:
            if segmento == "ENTERPRISE":
                propuesta = CATALOGO["ENTERPRISE"]["computo_ia"]
            else:
                propuesta = CATALOGO["PYME"]["hiperconvergencia"]
        # Si la relación es baja (cliente nuevo) o quiere ahorrar, sugerimos GreenLake
        elif relacion < 30:
            propuesta = CATALOGO["ESTRATEGICO"]["consumo"]
        else:
            # Oferta por defecto del segmento
            propuesta = CATALOGO[segmento]["computo"] if segmento == "PYME" else CATALOGO[segmento]["storage_ia"]

        recomendaciones.append({
            "id_cliente": id_cliente,
            "segmento": segmento,
            "producto_sugerido": propuesta["producto"],
            "justificacion": propuesta["descripcion"],
            "urgencia": "ALTA" if intencion > 80 else "MEDIA"
        })

    return pd.DataFrame(recomendaciones)