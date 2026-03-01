import sys
from src.pipiline.run_pipeline import ejecutar_pipeline_completo

def mostrar_banner():
    print("="*60)
    print("      HPE AI-SALES ENHANCER - PIPELINE HEURÍSTICO")
    print("="*60)

def main():
    mostrar_banner()
    
    # Configuración dinámica de pesos (puedes pedir inputs aquí)
    pesos = {
        "valor": 0.30,
        "intencion": 0.40,
        "relacion": 0.30
    }
    
    print(f"Configuración actual: {pesos}")
    input("\nPresione ENTER para iniciar el motor de inteligencia...")
    
    resultados = ejecutar_pipeline_completo(pesos)
    
    if resultados is not None:
        print("\n" + "="*60)
        print(f"RESULTADOS GENERADOS: {len(resultados)} prospectos encontrados")
        print("="*60)
        
        for i, row in resultados.iterrows():
            print(f"\n🚀 CLIENTE: {row['id_cliente']} | SEGMENTO: {row['segmento']}")
            print(f"🎯 PRODUCTO: {row['oferta_principal']} (Match: {row['confianza_match']})")
            print(f"📢 SPEECH SUGERIDO:\n{row['speech_final']}")
            print("-" * 40)
            
        print("\n✅ Proceso finalizado exitosamente.")
    else:
        print("\nHubo un problema en la ejecución.")

if __name__ == "__main__":
    main()