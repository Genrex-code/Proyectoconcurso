import joblib
import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error , r2_score

#impórts ratos (corregir despues) 
from .config import MODEL_DIR
from .config import Model_NAME
from .config import RANDOM_STATE
from .config import N_ESTIMATORS
from .config import MAX_DEPTH
from .config import TEST_SIZE
from .utils import validar_features

#def raros que debo escalar luego 

def entrenar_modelo(df,target_col):
    X = df.drop(columns =[target_col])
    Y = df[target_col]
#traduccion
    X_train, X_test, Y_train,Y_test = train_test_split(
        X,Y,
        test_size= TEST_SIZE,
        random_state= RANDOM_STATE
    )

    modelo = RandomForestRegressor( 
        n_estimators = N_ESTIMATORS,
        max_depth=MAX_DEPTH,
        random_state= RANDOM_STATE,
        n_jobs=-1
    )
    modelo.fit(X_train,Y_train)
    pred = modelo.predict(X_test)
    mae = mean_absolute_error(Y_test,pred)
    r2 = r2_score(Y_test,pred)
    joblib.dump(modelo,MODEL_DIR / Model_NAME)

    #usaremos esto para graficas en la interfaz despues 
    return {
        "modelo": modelo,
        "mae" : mae,
        "r2" : r2
    }
    