import joblib
import pandas as pd
import numpy as np
from .config import MODEL_DIR, MODEL_NAME

def actualizar_modelo(df_nuevo, target_col):
    """Actualiza el modelo con lógica de protección de datos"""
    path = MODEL_DIR / MODEL_NAME
    if not path.exists():
        from .train import entrenar_nuevo_modelo
        return entrenar_nuevo_modelo(df_nuevo, target_col)
    
    meta = joblib.load(path)
    pipeline = meta['pipeline']
    
    X_nuevo = df_nuevo.drop(columns=[target_col])
    y_nuevo = df_nuevo[target_col]

    # --- RAZONAMIENTO DE ROBUSTEZ ---
    # 1. Verificación de integridad de columnas
    if list(X_nuevo.columns) != meta['features']:
        raise ValueError(" Drift detectado: Las columnas de entrada no coinciden con el entrenamiento original.")

    # 2. Protección contra valores nulos/infinitos
    X_nuevo = X_nuevo.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    # 3. Acceso al paso del modelo dentro del pipeline para partial_fit
    # El scaler ya fue ajustado en train.py, aquí solo transformamos
    scaler = pipeline.named_steps['scaler']
    model = pipeline.named_steps['model']
    
    X_scaled = scaler.transform(X_nuevo)
    model.partial_fit(X_scaled, y_nuevo)
    
    # Actualizamos metadata
    meta['n_muestras'] += len(df_nuevo)
    meta['ultima_actualizacion'] = pd.Timestamp.now().isoformat()
    
    joblib.dump(meta, path)
    print(f" [IA] Conocimiento expandido. Total muestras procesadas: {meta['n_muestras']}")
    return meta