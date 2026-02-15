"""
test_speech.py
Prueba básica del generador de speech
"""

from modules.speech import generar_speech


def test_speech_basico():

    texto = generar_speech({
        "id_cliente": 1,
        "empresa": "TechCorp",
        "recomendacion": "Ofrecer servidor cloud"
    })

    assert isinstance(texto, str)
    assert len(texto) > 10
