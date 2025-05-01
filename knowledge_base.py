# knowledge_base.py

soluciones_predefinidas = {
    "agua": {
        "fuga_grave": "URGENTE: Cierre inmediatamente la llave principal de agua y contacte al número de emergencia: 555-0123. Un técnico será enviado de inmediato.",
        "fuga_menor": "Por favor cierre la llave de paso más cercana al área afectada. Mantenimiento programará una visita en las próximas 24 horas.",
        "sin_agua": "Se ha registrado su reporte. Verificaremos si es un problema general del edificio o específico de su unidad. Tiempo estimado de respuesta: 2 horas.",
        "default": "Por favor cierre la llave principal de agua y contacte a mantenimiento al 555-0123."
    },
    "electricidad": {
        "corto_circuito": "URGENTE: No toque ningún aparato eléctrico. Diríjase al tablero principal y baje el interruptor general. El electricista está en camino.",
        "apagon": "Verificaremos si es un problema interno o de la compañía eléctrica. Por favor, espere nuestra confirmación en los próximos 15 minutos.",
        "falla_parcial": "Revise el tablero de su unidad. Si el problema persiste, un técnico realizará la inspección en las próximas 3 horas.",
        "default": "Apague el interruptor principal y espere al electricista del residencial."
    },
    "seguridad": {
        "robo": "URGENTE: Se ha notificado a seguridad y policía. Por favor, manténgase en un lugar seguro. Personal en camino.",
        "sospechoso": "Seguridad realizará un patrullaje inmediato en el área. Se aumentará la vigilancia en las próximas 24 horas.",
        "camaras": "Se revisarán las grabaciones de seguridad y se le informará de los hallazgos en las próximas 2 horas.",
        "default": "Se ha notificado al equipo de seguridad del residencial. Tiempo de respuesta estimado: 10 minutos."
    },
    "ruido": {
        "fiesta": "Se enviará personal de seguridad para verificar. El reglamento establece silencio después de las 22:00 horas.",
        "construccion": "Se verificará si cuentan con los permisos correspondientes. Los horarios permitidos son de 9:00 a 17:00 horas.",
        "mascotas": "Se notificará al propietario. El reglamento establece control de ruidos de mascotas según normativa vigente.",
        "default": "Se notificará al vecino sobre la queja. En caso de reincidencia, se aplicarán las sanciones correspondientes."
    },
    "limpieza": {
        "areas_comunes": "El equipo de limpieza atenderá el área en la siguiente hora. Se realizará supervisión posterior.",
        "basura": "Se programará recolección especial. Por favor, mantenga los residuos en bolsas cerradas mientras tanto.",
        "plaga": "Se coordinará visita del servicio de control de plagas en las próximas 24 horas.",
        "default": "El equipo de mantenimiento programará la limpieza correspondiente en las próximas 12 horas."
    },
    "general": {
        "default": "Su solicitud ha sido registrada. Personal de mantenimiento evaluará la situación en las próximas 24 horas."
    }
}

# Función para obtener solución específica
def obtener_solucion(categoria, descripcion=None):
    categoria = categoria.lower()
    
    # Si no hay categoría específica
    if categoria not in soluciones_predefinidas:
        return soluciones_predefinidas["general"]["default"]
    
    # Obtener subcategoría si es posible
    subcategoria = determinar_subcategoria(categoria, descripcion) if descripcion else None
    
    # Retornar solución específica si existe
    if subcategoria and subcategoria in soluciones_predefinidas[categoria]:
        return soluciones_predefinidas[categoria][subcategoria]
    
    # Retornar solución por defecto de la categoría
    return soluciones_predefinidas[categoria]["default"]

def determinar_subcategoria(categoria, descripcion):
    descripcion = descripcion.lower()
    
    subcategorias = {
        "agua": {
            "fuga_grave": ["inundación", "fuga grande", "mucha agua", "desbordamiento", "agua por todas partes"],
            "fuga_menor": ["goteo", "fuga pequeña", "gota", "gotera pequeña", "fuga lenta"],
            "sin_agua": ["no hay agua", "sin suministro", "no sale agua", "sin servicio de agua"]
        },
        "electricidad": {
            "corto_circuito": ["corto", "chispa", "quemado", "humo", "olor a quemado", "chispas"],
            "apagon": ["sin luz", "apagón", "no hay electricidad", "sin energía", "todo apagado"],
            "falla_parcial": ["parpadea", "intermitente", "bajo voltaje", "luz débil"]
        },
        "seguridad": {
            "robo": ["robo", "ladrón", "robando", "forzando", "sustrajeron", "hurto"],
            "sospechoso": ["sospechoso", "persona extraña", "actitud sospechosa", "merodeando"],
            "camaras": ["cámara", "vigilancia", "grabación", "video", "cctv"]
        },
        "ruido": {
            "fiesta": ["fiesta", "música alta", "escándalo", "ruido fuerte", "celebración"],
            "construccion": ["construcción", "obra", "martillo", "taladro", "remodelación"],
            "mascotas": ["perro", "mascota", "ladrido", "animal", "gato"]
        },
        "limpieza": {
            "areas_comunes": ["área común", "pasillo", "entrada", "lobby", "escalera"],
            "basura": ["basura", "desperdicio", "residuos", "desechos", "contenedor"],
            "plaga": ["plaga", "cucaracha", "rata", "insecto", "roedor", "hormiga"]
        }
    }
    
    if categoria in subcategorias:
        for subcategoria, palabras in subcategorias[categoria].items():
            if any(palabra in descripcion for palabra in palabras):
                return subcategoria
    
    return "default"
