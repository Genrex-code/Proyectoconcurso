import pandas as pd
from .train import entrenar_modelo
from .predict import cargar_modelo

def actualizar_modelo ( df_nuevo, target_col):
    #aca es el mecanismo de regrecion o como se escriba
    # que cihngue asu amdre el america
    df_hist = pd.read_csv ("models /" \
    "historico_entrenamiento.csv")

    df_total = pd.concat([df_hist,df_nuevo])

    df_total.to_csv ("models / " \
    "historico_entrenamiento.csv", index= False)

    resultado = entrenar_modelo ( df_total,target_col)
    return resultado

