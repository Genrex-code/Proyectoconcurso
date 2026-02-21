def test_speech_texto():
    from src.speech.speech import generar_speech

    txt = generar_speech("Empresa X", "segmento alto")

    assert isinstance(txt,str)
    assert len(txt) > 5