import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Descarga de datos NLTK necesarios
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
except Exception as e:
    print(f"Advertencia: No se pudieron descargar los datos NLTK: {e}")

def clasificar_ticket(descripcion):
    try:
        descripcion = descripcion.lower()
        # Tokenización simple para mayor confiabilidad
        tokens = descripcion.split()
        
        # Sistema de puntuación mejorado
        puntuaciones = {}
        
        for categoria, palabras in categorias.items():
            puntuacion = 0
            for palabra in palabras:
                # Búsqueda exacta
                if palabra in tokens:
                    puntuacion += 3
                # Búsqueda en la descripción completa
                elif palabra in descripcion:
                    puntuacion += 1
                # Búsqueda de palabras parciales
                else:
                    for token in tokens:
                        if palabra in token or token in palabra:
                            puntuacion += 0.5
            puntuaciones[categoria] = puntuacion

        # Determinar la mejor categoría
        if puntuaciones:
            mejor_categoria = max(puntuaciones.items(), key=lambda x: x[1])
            if mejor_categoria[1] > 0:
                return mejor_categoria[0]
                
        return "General"
        
    except Exception as e:
        print(f"Error en clasificación: {e}")
        return "General"


# Categorías y palabras clave mejoradas
categorias = {
    'Agua': [
        'agua', 'fuga', 'goteo', 'inundación', 'tubería', 'grifo', 'humedad',
        'filtración', 'gotera', 'presión', 'drenaje', 'caño', 'cisterna',
        'tanque', 'sanitario', 'lavabo', 'ducha', 'cañería'
    ],
    'Electricidad': [
        'luz', 'electricidad', 'corto', 'circuito', 'enchufe', 'apagón',
        'voltaje', 'tomacorriente', 'interruptor', 'cables', 'fusible',
        'breaker', 'chispa', 'transformador', 'lámpara', 'conexión'
    ],
    'Seguridad': [
        'alarma', 'robo', 'seguridad', 'intruso', 'sospechoso', 'cámara',
        'vigilancia', 'emergencia', 'amenaza', 'violencia', 'vandalismo',
        'cerradura', 'llave', 'acceso', 'guardia', 'protección', 'incidente'
    ],
    'Ruido': [
        'ruido', 'bulla', 'fiesta', 'escándalo', 'música', 'alto',
        'volumen', 'grito', 'construcción', 'obra', 'martillo',
        'taladro', 'mascota', 'ladrido', 'alboroto', 'discusión'
    ],
    'Limpieza': [
        'basura', 'limpieza', 'suciedad', 'desorden', 'manchas', 'desperdicios',
        'plagas', 'insectos', 'roedores', 'olor', 'residuos', 'desechos',
        'acumulación', 'derrame', 'polvo', 'contaminación'
    ],
    'Mantenimiento': [
        'ascensor', 'elevador', 'escalera', 'puerta', 'ventana', 'pared',
        'techo', 'piso', 'pintura', 'aire acondicionado', 'calefacción',
        'jardín', 'piscina', 'gimnasio', 'reparación', 'mantenimiento'
    ]
}
