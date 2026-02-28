import joblib
import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from datetime import datetime
from .config import MODEL_DIR, MODEL_NAME, RANDOM_STATE

def entrenar_nuevo_modelo(df, target_col):
    """Crea un pipeline robusto que escala y entrena"""
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Creamos un Pipeline para que el escalado sea parte del modelo
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', SGDRegressor(max_iter=1000, tol=1e-3, random_state=RANDOM_STATE))
    ])
    
    pipeline.fit(X, y)
    
    # Guardamos meta-información para auditoría
    metadata = {
        'pipeline': pipeline,
        'features': list(X.columns),
        'fecha_entrenamiento': datetime.now().isoformat(),
        'n_muestras': len(df)
    }
    
    joblib.dump(metadata, MODEL_DIR / MODEL_NAME)
    print(f" [IA] Master Model creado con {len(X.columns)} features.")
    return metadata