import os
import sys
from pathlib import Path

# CONFIGURACIÓN DE RUTAS (Solo aquí)
# Agregamos la raíz del proyecto al path de Python
root_path = Path(__file__).resolve().parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# Ahora sí importamos el pipeline
from src.pipiline.run_pipeline import ejecutar_pipeline_completo

def mostrar_banner():
    print("="*60)
    print("      HPE AI-SALES ENHANCER - MOTOR DE INTELIGENCIA")
    print("="*60)

def main():
    mostrar_banner()
    
    # Pesos por defecto (puedes cambiarlos aquí)
    pesos = {
        "valor": 0.30,
        "intencion": 0.40,
        "relacion": 0.30
    }
    
    print(f"Configuración de Scoring: {pesos}")
    input("\nPresione ENTER para ejecutar el pipeline...")
    
    resultados = ejecutar_pipeline_completo(pesos)
    
    if resultados is not None:
        print("\n" + "!"*60)
        print(f"ÉXITO: Se generaron {len(resultados)} recomendaciones.")
        print("!"*60)
        
        # Mostrar los primeros 3 resultados para la demo
        for i, row in resultados.head(3).iterrows():
            print(f"\n🏢 CLIENTE: {row['id_cliente']}")
            print(f"🛠️ SOLUCIÓN: {row['oferta_principal']}")
            print(f"📝 SPEECH: {row['speech_final'][:150]}...") # Mostramos solo el inicio
            print("-" * 40)
            
        print("\n✅ Proceso completado. Listo para la presentación.")
    else:
        print("\nFallo en la ejecución. Revisa los logs arriba.")

if __name__ == "__main__":
    main()