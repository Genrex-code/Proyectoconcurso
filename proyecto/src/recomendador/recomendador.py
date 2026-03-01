import pandas as pd 
from src.recomendador.productos.catalogo_hpe import CATALOGO

def generar_recomendaciones_expertas(df_scoring):
    """
    Recomendador avanzado con lógica de Cross-selling y Trigger de Venta.
    """
    resultados = []

    for _, row in df_scoring.iterrows():
        # --- 1. LÓGICA DE SEGMENTACIÓN ---
        valor = row['detalle_valor']
        intencion = row['detalle_intencion']
        relacion = row['detalle_relacion']
        segmento = "ENTERPRISE" if valor > 60 else "PYME"
        
        # --- 2. SELECCIÓN DE SOLUCIÓN INTEGRAL ---
        # Inicializamos variables de la oferta
        primario = None
        complemento = "HPE InfoSight (Monitoreo Predictivo IA)" # Default para todos
        
        if intencion > 75:
            # Caso: Necesidad de Cómputo/IA detectada
            primario = CATALOGO[segmento].get("computo_ia") or CATALOGO[segmento].get("computo")
            complemento = CATALOGO[segmento].get("storage_ia") or CATALOGO["ESTRATEGICO"]["software_ia"]
        elif relacion < 30:
            # Caso: Riesgo financiero o cliente nuevo
            primario = CATALOGO["ESTRATEGICO"]["consumo"] # GreenLake
            complemento = CATALOGO[segmento].get("almacenamiento")
        else:
            # Caso: Mantenimiento / Consolidación
            primario = CATALOGO[segmento].get("hiperconvergencia") or CATALOGO[segmento].get("almacenamiento")

        # --- 3. CÁLCULO DE CONFIANZA DEL "MATCH" ---
        # Si la intención y el valor están alineados, la confianza sube
        confianza = (intencion + valor) / 2
        
        # --- 4. CONSTRUCCIÓN DEL TRIGGER (Basado en PDF) ---
        trigger = "Acelerar el time-to-market de modelos de IA" if segmento == "ENTERPRISE" else "Simplificar la TI para enfoque en el negocio"

        resultados.append({
            "id_cliente": row['id_cliente'],
            "propuesta_base": primario["producto"] if primario else "Consultoría HPE",
            "cross_sell": complemento["producto"] if isinstance(complemento, dict) else complemento,
            "match_confidence": f"{confianza:.1f}%",
            "justificacion_comercial": primario["descripcion"] if primario else "Optimización general",
            "trigger_venta": trigger,
            "prioridad_llamada": "URGENTE" if intencion > 85 else "ESTRÁTEGICA"
        })

    return pd.DataFrame(resultados)