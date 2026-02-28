""" se creo un promp para investigar todos los productos
HPE y para organizarlos en un diccionario que podemos llamar
mas facilmente lo que nos ahorra horas de trabajo tedioso
nota del programador 
me voy a volver loco 
JAJA
"""
# catalogo_hpe.py

CATALOGO = {
    "PYME": { # Para scores de valor bajos/medios
        "computo": {
            "producto": "HPE ProLiant MicroServer / ML30",
            "descripcion": "Servidores compactos para etapas iniciales de IA como preprocesamiento de datos.", # [cite: 4, 5]
            "keywords": ["base de datos", "virtualización ligera", "sucursal"]
        },
        "hiperconvergencia": {
            "producto": "HPE SimpliVity",
            "descripcion": "Ideal para desplegar rápidamente entornos de desarrollo y test de IA con gestión centralizada.", # [cite: 7, 8]
            "keywords": ["consolidación", "desarrollo", "simplicidad"]
        },
        "almacenamiento": {
            "producto": "HPE MSA",
            "descripcion": "Arreglos SAN híbridos económicos para alimentar pipelines de IA pequeños.", # [cite: 29, 30]
            "keywords": ["respaldo", "san básico", "económico"]
        }
    },
    "ENTERPRISE": { # Para scores de valor altos
        "computo_ia": {
            "producto": "HPE ProLiant DL/ML Gen12 con GPUs",
            "descripcion": "Servidores escalables diseñados para entrenar redes neuronales y modelos de IA a gran escala.", # [cite: 10, 11]
            "keywords": ["redes neuronales", "entrenamiento", "alto rendimiento"]
        },
        "composable": {
            "producto": "HPE Synergy",
            "descripcion": "Infraestructura modular para componer pools de recursos físicos y virtuales dinámicamente.", # [cite: 12, 13]
            "keywords": ["híbrido", "escalabilidad rápida", "blade"]
        },
        "storage_ia": {
            "producto": "HPE Alletra",
            "descripcion": "Almacenamiento nativo de la nube con IA operacional (InfoSight) para grandes volúmenes de datos.", # [cite: 35, 36]
            "keywords": ["cloud native", "misión crítica", "latencia ultrabaja"]
        }
    },
    "ESTRATEGICO": { # Soluciones transversales de alto nivel
        "consumo": {
            "producto": "HPE GreenLake",
            "descripcion": "Plataforma as-a-service que permite ampliar capacidad de entrenamiento de IA on-demand sin inversión inicial.", # [cite: 116, 117]
            "keywords": ["opex", "pago por uso", "nube híbrida"]
        },
        "software_ia": {
            "producto": "HPE Ezmeral Unified Analytics",
            "descripcion": "Plataforma para agilizar el desarrollo, implementación y supervisión de modelos de IA.", # [cite: 86, 87]
            "keywords": ["ml ops", "data fabric", "frameworks"]
        }
    }
}