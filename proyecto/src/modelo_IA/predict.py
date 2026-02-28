import joblib

def predecir (X):
    modelo = joblib.load("models/modelo_HPE.pkl")
    return modelo.predict(X)

