# utils/decision_tree.py
def decidir_prioridad(descripcion):
    descripcion = descripcion.lower()

    if "corto circuito" in descripcion or "fuga grande" in descripcion:
        return "Alta"
    elif "goteo pequeño" in descripcion or "basura" in descripcion:
        return "Media"
    else:
        return "Baja"
