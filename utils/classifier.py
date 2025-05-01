# utils/classifier.py
def clasificar_ticket(descripcion):
    descripcion = descripcion.lower()

    if any(palabra in descripcion for palabra in ['agua', 'fuga', 'goteo']):
        return "Agua"
    elif any(palabra in descripcion for palabra in ['luz', 'electricidad', 'corto circuito']):
        return "Electricidad"
    elif any(palabra in descripcion for palabra in ['alarma', 'robo', 'seguridad']):
        return "Seguridad"
    elif any(palabra in descripcion for palabra in ['ruido', 'bulla', 'fiesta']):
        return "Ruido"
    elif any(palabra in descripcion for palabra in ['basura', 'limpieza', 'suciedad']):
        return "Limpieza"
    else:
        return "General"
