import pandas as pd
import logging

def log(msg):
    print(f'[SpeechGen] {msg}')

def generar_speech_personalizado(df_estrategia):
    """
    Transforma la estrategia comercial en guiones narrativos de alto impacto.
    Utiliza datos del catálogo y la investigación de infraestructura HPE.
    """
    log(f"Generando guiones para {len(df_estrategia)} prospectos...")
    
    guiones_finales = []

    for _, row in df_estrategia.iterrows():
        cliente = row['id_cliente']
        segmento = row['segmento']
        producto = row['oferta_principal']
        cross_sell = row['venta_cruzada']
        trigger = row['trigger_negocio']
        argumento = row['argumento_venta']
        confianza = row['confianza_match']
        prioridad = row['prioridad']

        # --- DICCIONARIO DE PLANTILLAS POR SEGMENTO ---
        if segmento == "ENTERPRISE":
            # Tono: Estratégico, escalable, enfocado en ROI y Cargas Críticas
            intro = f"Estimado equipo de {cliente}, basándonos en los recientes indicadores de {trigger} en su sector..."
            cuerpo = (f"Hemos identificado que la implementación de {producto} es el paso lógico para escalar sus operaciones. "
                      f"Esta solución, combinada con {cross_sell}, garantiza una infraestructura composable capaz de "
                      f"soportar el entrenamiento masivo de IA, tal como se detalla en los estándares de alto desempeño de HPE.")
            cierre = "Dada la prioridad estratégica de este movimiento, ¿podemos agendar una breve sesión técnica para revisar el roadmap?"
        
        else:
            # Tono: Eficiencia, simplicidad, ahorro y "pago por uso"
            intro = f"Hola, me pongo en contacto con {cliente} porque vemos una oportunidad clave para {trigger}."
            cuerpo = (f"Para empresas con su dinamismo, recomendamos {producto}. Es una solución que 'se paga sola' "
                      f"gracias a la eficiencia operativa, y al integrarla con {cross_sell}, cuentan con el respaldo de "
                      "HPE InfoSight, que resuelve el 86% de los problemas de TI de forma automática antes de que ocurran.")
            cierre = "¿Le interesaría conocer cómo podemos implementar esto bajo un modelo flexible sin inversión inicial?"

        # --- ESTRUCTURA DE SALIDA PARA LA UI ---
        # Incluimos metadatos para que el vendedor sepa por qué el speech es así
        speech_completo = (
            f"--- GUION SUGERIDO (Prioridad: {prioridad}) ---\n"
            f"{intro}\n\n"
            f"{cuerpo}\n\n"
            f"{cierre}\n"
            f"-------------------------------------------\n"
            f"TIP DE VENTA: {argumento}"
        )

        guiones_finales.append({
            "id_cliente": cliente,
            "speech_final": speech_completo,
            "canal_recomendado": "Llamada Telefónica" if prioridad == "CRÍTICA" else "Email / LinkedIn",
            "match_score": confianza
        })

    log("Speeches generados exitosamente.")
    return pd.DataFrame(guiones_finales)