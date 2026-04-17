"""
robo_uniandes.py — El Robo del Algoritmo en Los Andes

Pepito, estudiante de Ingenieria de Sistemas, desarrollo un algoritmo revolucionario en el mundo de los juegos en la pecera durante el semestre pasado.
El codigo fue copiado del portatil de Pepito sin su conocimiento y la grabadora de audio desaparecio del puesto donde estaba trabajabando.
El Profesor Rubén estaba dictando clase en el salon G_101 durante toda la tarde, la lista de asistencia firmada por sus 30 estudiantes lo confirma.
La Profesora Olga declara que Perensejo estuvo con ella en un salon del ML toda la tarde resolviendo unas dudas para el parcial.
Perensejo no tiene coartada verificada.
Las huellas de Perensejo estan en el portatil y en la grabadora de audio de Pepito.
Santiago, el monitor del curso, fue amenazado por Perensejo para que no reportara lo ocurrido.
Perensejo tiene historial de copiar trabajos y parciales desde el colegio.
Perensejo acusa a Santiago de haberle robado el codigo a Pepito.
La Profesora Olga acusa a Santiago tambien, defendiendo a Perensejo.

Como detective, he llegado a las siguientes conclusiones:
Quien tiene lista de asistencia de clase queda descartado de sospechoso.
Quien tiene huellas en los objetos robados tiene evidencia fisica en su contra.
Quien tiene historial de copia tiene antecedentes academicos deshonestos.
Quien tiene antecedentes academicos deshonestos tiene motivo para robar el algoritmo.
Quien tiene motivo, evidencia y no tiene coartada verificada es culpable.
Quien respalda la coartada falsa de un culpable es complice.
Cuando el culpable acusa a otro para desviar la investigacion, esa acusacion es una desviacion sospechosa.
Cuando el complice acusa al mismo inocente que el culpable, la acusacion es coordinada.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB segun la narrativa del modulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    ruben      = Term("ruben")
    santiago   = Term("santiago")
    pepito     = Term("pepito")
    olga       = Term("olga")
    perensejo  = Term("perensejo")
    portatil   = Term("portatil")
    grabadora  = Term("grabadora")

    kb.add_fact(Predicate("persona", (ruben,)))
    kb.add_fact(Predicate("persona", (santiago,)))
    kb.add_fact(Predicate("persona", (pepito,)))
    kb.add_fact(Predicate("persona", (olga,)))
    kb.add_fact(Predicate("persona", (perensejo,)))

    kb.add_fact(Predicate("victima", (pepito,)))

    kb.add_fact(Predicate("asistencia_clase", (ruben,)))

    kb.add_fact(Predicate("huellas", (perensejo, portatil)))
    
    kb.add_fact(Predicate("huellas", (perensejo, grabadora)))

    kb.add_fact(Predicate("historial", (perensejo,)))

    kb.add_fact(Predicate("sin_coartada", (perensejo,)))

    kb.add_fact(Predicate("testimonio_falso", (olga, perensejo)))

    kb.add_fact(Predicate("acusa", (perensejo, santiago)))
    
    kb.add_fact(Predicate("acusa", (olga, santiago)))

    X = Term("$X")
    Y = Term("$Y")

    kb.add_rule(Rule(
        head=Predicate("descartado", (X,)),
        body=(Predicate("asistencia_clase", (X,)),),
    ))

    kb.add_rule(Rule(
        head=Predicate("evidencia", (X,)),
        body=(Predicate("huellas", (X, Term("$O"))),),
    ))

    kb.add_rule(Rule(
        head=Predicate("antecedentes", (X,)),
        body=(Predicate("historial", (X,)),),
    ))

    kb.add_rule(Rule(
        head=Predicate("tiene_motivo", (X,)),
        body=(Predicate("antecedentes", (X,)),),
    ))

    kb.add_rule(Rule(
        head=Predicate("culpable", (X,)),
        body=(
            Predicate("tiene_motivo", (X,)),
            Predicate("evidencia", (X,)),
            Predicate("sin_coartada", (X,)),
        ),
    ))

    kb.add_rule(Rule(
        head=Predicate("complice", (X,)),
        body=(
            Predicate("testimonio_falso", (X, Y)),
            Predicate("culpable", (Y,)),
        ),
    ))

    kb.add_rule(Rule(
        head=Predicate("desvio_sospechoso", (X, Y)),
        body=(
            Predicate("culpable", (X,)),
            Predicate("acusa", (X, Y)),
        ),
    ))

    kb.add_fact(Predicate("acusa_coordinado", (perensejo, santiago)))

    kb.add_rule(Rule(
        head=Predicate("acusacion", (X, Y)),
        body=(
            Predicate("complice", (X,)),
            Predicate("acusa", (X, Y)),
            Predicate("acusa_coordinado", (Term("$C"), Y)),
        ),
    ))

    return kb


CASE = CrimeCase(
    id="robo_uniandes",
    title="El robo del algoritmo en Los Andes",
    suspects=("ruben", "santiago", "perensejo", "olga"),
    narrative=__doc__,
    description=(
        "Pepito desarrollo un algoritmo revolucionario de juegos en la pecera."
        "El codigo fue robado de su portatil y su grabadora de audio desaparecio."
        "El Profesor Rubén tiene coartada de asistencia en un salon en el Franco. Perensejo tiene huellas en ambos objetos, historial de copia y ninguna coartada."
        "La profesora Olga lo encubre y ambos acusan coordinadamente al monitor Santiago."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="El Profesor Rubén esta descartado?",
            goal=Predicate("descartado", (Term("ruben"),)),
        ),
        QuerySpec(
            description="Perensejo tiene evidencia fisica en su contra?",
            goal=Predicate("evidencia", (Term("perensejo"),)),
        ),
        QuerySpec(
            description="Perensejo tiene motivo para robar el algoritmo?",
            goal=Predicate("tiene_motivo", (Term("perensejo"),)),
        ),
        QuerySpec(
            description="Perensejo es culpable?",
            goal=Predicate("culpable", (Term("perensejo"),)),
        ),
        QuerySpec(
            description="La profesora Olga es complice?",
            goal=Predicate("complice", (Term("olga"),)),
        ),
        QuerySpec(
            description="La acusacion de Perensejo contra Santiago es un desvio sospechoso?",
            goal=Predicate("desvio_sospechoso", (Term("perensejo"), Term("santiago"))),
        ),
        QuerySpec(
            description="La acusacion de Olga contra Santiago es coordinada con Perensejo?",
            goal=Predicate("acusacion", (Term("olga"), Term("santiago"))),
        ),
        QuerySpec(
            description="Existe algun culpable en el caso?",
            goal=ExistsGoal("$X", Predicate("culpable", (Term("$X"),))),
        ),
        QuerySpec(
            description="Todo culpable tiene evidencia en su contra?",
            goal=ForallGoal(
                "$X",
                Predicate("culpable", (Term("$X"),)),
                Predicate("evidencia", (Term("$X"),)),
            ),
        ),
    ),
)