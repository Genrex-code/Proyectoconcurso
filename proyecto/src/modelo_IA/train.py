from sklearn.ensemble import RandomForestRegressor
import joblib

def entrenar_modelo(X,Y):
    modelo = RandomForestRegressor(
        n_estimators = 200,
        max_depth = 10,
        random_state = 42
    )

    modelo.fit(X,Y)
    joblib.dump(modelo,"models/modelo_HPE.pkl")
    return modelo