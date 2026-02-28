# # por el momento hice un algoritmo de ordenamineto simple
# # pero el plan es cambiarlo a un modelo de IA (o mejorar el algoritmo)
# """
# clasificador.py
# Segmenta clientes según score
# Sistema IA HPE
# """

# import pandas as pd


# def clasificar(score):
#     """Reglas de negocio"""
#     if score >= 70:
#         return "Caliente"
#     elif score >= 40:
#         return "Tibio"
#     else:
#         return "Frio"


# def clasificar_clientes(scores_df):
#     """
#     scores_df = dataframe con columnas:
#     id_cliente | score
#     """

#     df = scores_df.copy()

#     df["segmento"] = df["score"].apply(clasificar)

#     print("Clientes clasificados:", len(df))
#     print(df["segmento"].value_counts())

#     return df
