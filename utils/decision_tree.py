from dataclasses import dataclass
from typing import Dict, List

@dataclass
class DecisionNode:
    question: str
    keywords: List[str]
    priority: str = None
    professional_required: bool = False
    yes_branch: 'DecisionNode' = None
    no_branch: 'DecisionNode' = None

def create_decision_tree() -> Dict[str, DecisionNode]:
    trees = {
        "agua": DecisionNode(
            "¿Es una emergencia grave?",
            ["inundación", "inundado", "mucha agua", "desbordamiento"],
            yes_branch=DecisionNode(
                "¿Hay daños estructurales?",
                ["pared", "techo", "filtración grave"],
                priority="Alta",
                professional_required=True
            ),
            no_branch=DecisionNode(
                "¿Es una fuga menor?",
                ["goteo", "gota", "pequeña fuga"],
                priority="Baja",
                professional_required=False
            )
        ),
        "electricidad": DecisionNode(
            "¿Hay riesgo inmediato?",
            ["chispas", "humo", "quemado", "corto circuito"],
            yes_branch=DecisionNode(
                "¿Hay fuego o humo visible?",
                ["fuego", "llamas", "incendio"],
                priority="Alta",
                professional_required=True
            ),
            no_branch=DecisionNode(
                "¿Es una falla menor?",
                ["parpadeo", "no enciende", "fusible"],
                priority="Media",
                professional_required=True
            )
        ),
    }
    return trees

def decidir_prioridad(descripcion: str, categoria: str) -> dict:
    descripcion = descripcion.lower()
    trees = create_decision_tree()
    
    if categoria.lower() not in trees:
        return {
            "prioridad": "Media",
            "professional_required": True,
            "razon": "Categoría no específica"
        }
    
    current_node = trees[categoria.lower()]
    while current_node.yes_branch or current_node.no_branch:
        if any(keyword in descripcion for keyword in current_node.keywords):
            if not current_node.yes_branch:
                break
            current_node = current_node.yes_branch
        else:
            if not current_node.no_branch:
                break
            current_node = current_node.no_branch
    
    return {
        "prioridad": current_node.priority or "Media",
        "professional_required": current_node.professional_required,
        "razon": current_node.question
    }
