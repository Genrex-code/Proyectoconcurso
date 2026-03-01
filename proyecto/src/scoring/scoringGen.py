import pandas as pd 
import logging
#imports de capas 
from src.scoring.capas.capa_valor import calcular_capa_valor
from src.scoring.capas.capa_intencion import calcular_capa_intencion
from src.scoring.capas.capa_relacion import calcular_capa_relacion
# se que debi asumirlos pero fui al baño y se me olvido cambiarlos jajasjasjas+
#y hablo del config
#esquisofrenico 
# datos para que tenga un norte
def generar_scoreing_heuristioco(df_features,pesos = {"valor": 0.33, "intencion": 0.34, "relacion": 0.33}):
    """
    orquestador principal que une las 3 capas de scoring
"""
    # agregar consistencia al logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__) 

    try:
        print(f"[ScoringGen] Calculando heurística con pesos: {pesos}")

        # 1. Obtener scores de cada capa de forma independiente
        s_valor = calcular_capa_valor(df_features)
        s_intencion = calcular_capa_intencion(df_features)
        s_relacion = calcular_capa_relacion(df_features)

        # 2. Aplicar la fórmula maestra (Suma ponderada)
        # Usamos los pesos dinámicos que configuraste
        score_final = (
            (s_valor * pesos.get('valor', 0.33)) +
            (s_intencion * pesos.get('intencion', 0.34)) +
            (s_relacion * pesos.get('relacion', 0.33))
        )

        # 3. Guardar desglose para que el Recomendador sepa POR QUÉ el score es alto
        # Esto es "IA Explicable" para humanos
        df_resultados = pd.DataFrame({
            'id_cliente': df_features.get('id_cliente', df_features.index),
            'score_heuristico': score_final,
            'detalle_valor': s_valor,
            'detalle_intencion': s_intencion,
            'detalle_relacion': s_relacion
        })

        print(f"[ScoringGen] Proceso completado para {len(df_resultados)} clientes.")
        return df_resultados

    except Exception as e:
        print(f"[ScoringGen] ERROR CRÍTICO: {e}")
        return pd.DataFrame() # retorbno vacio para no romper el pipiline principal 