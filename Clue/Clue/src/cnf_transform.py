"""
cnf_transform.py — Transformaciones a Forma Normal Conjuntiva (CNF).
El pipeline completo to_cnf() llama a todas las transformaciones en orden.
"""

from __future__ import annotations

from src.logic_core import And, Atom, Formula, Iff, Implies, Not, Or


# --- FUNCION GUÍA SUMINISTRADA COMPLETA ---


def eliminate_double_negation(formula: Formula) -> Formula:
    """
    Elimina dobles negaciones recursivamente.

    Transformacion:
        Not(Not(a)) -> a

    Se aplica recursivamente hasta que no queden dobles negaciones.

    Ejemplo:
        >>> eliminate_double_negation(Not(Not(Atom('p'))))
        Atom('p')
        >>> eliminate_double_negation(Not(Not(Not(Atom('p')))))
        Not(Atom('p'))
    """
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula, Not):
        if isinstance(formula.operand, Not):
            return eliminate_double_negation(formula.operand.operand)
        return Not(eliminate_double_negation(formula.operand))
    if isinstance(formula, And):
        return And(*(eliminate_double_negation(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(eliminate_double_negation(d) for d in formula.disjuncts))
    return formula


# --- FUNCIONES QUE DEBEN IMPLEMENTAR ---


def eliminate_iff(formula: Formula) -> Formula:
    """
    Elimina bicondicionales recursivamente.

    Transformacion:
        Iff(a, b) -> And(Implies(a, b), Implies(b, a))

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> eliminate_iff(Iff(Atom('p'), Atom('q')))
        And(Implies(Atom('p'), Atom('q')), Implies(Atom('q'), Atom('p')))

    Hint: Usa pattern matching sobre el tipo de la formula.
          Para cada tipo, aplica eliminate_iff recursivamente a los operandos,
          y solo transforma cuando encuentras un Iff.
    """
    # === YOUR CODE HERE ===
    if isinstance(formula,Atom):
        return formula
    if isinstance(formula,Not):
        return Not(eliminate_iff(formula.operand))
    if isinstance(formula, And):
        return And(*(eliminate_iff(c) for c in formula.conjuncts))
    if isinstance(formula, Or):
        return Or(*(eliminate_iff(d) for d in formula.disjuncts))
    if isinstance(formula, Implies):
        left= eliminate_iff(formula.antecedent)
        right= eliminate_iff(formula.consequent)
        return Implies(left, right)

    if isinstance(formula, Iff):
        left= eliminate_iff(formula.left)
        right= eliminate_iff(formula.right)
        return And(Implies(left, right), Implies(right, left))

    return formula
    # === END YOUR CODE ===


def eliminate_implication(formula: Formula) -> Formula:
    """
    Elimina implicaciones recursivamente.

    Transformacion:
        Implies(a, b) -> Or(Not(a), b)

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> eliminate_implication(Implies(Atom('p'), Atom('q')))
        Or(Not(Atom('p')), Atom('q'))

    Hint: Similar a eliminate_iff. Recorre recursivamente y transforma
          solo los nodos Implies.
    """
    # === YOUR CODE HERE ===
    if isinstance(formula,Atom):
        return formula

    if isinstance(formula,Not):
        return Not(eliminate_implication(formula.operand))

    if isinstance(formula, And):
        return And(*(eliminate_implication(c) for c in formula.conjuncts))

    if isinstance(formula, Or):
        return Or(*(eliminate_implication(d) for d in formula.disjuncts))

    if isinstance(formula,Iff):
        left= eliminate_implication(formula.left)
        right= eliminate_implication(formula.right)
        return Iff(left,right)

    if isinstance(formula, Implies):
        left = eliminate_implication(formula.antecedent)
        right = eliminate_implication(formula.consequent)
        return Or(Not(left), right)

    return formula
    # === END YOUR CODE ===


def push_negation_inward(formula: Formula) -> Formula:
    """
    Aplica las leyes de De Morgan y mueve negaciones hacia los atomos.

    Transformaciones:
        Not(And(a, b, ...)) -> Or(Not(a), Not(b), ...)   (De Morgan)
        Not(Or(a, b, ...))  -> And(Not(a), Not(b), ...)   (De Morgan)

    Debe aplicarse recursivamente a todas las sub-formulas.

    Ejemplo:
        >>> push_negation_inward(Not(And(Atom('p'), Atom('q'))))
        Or(Not(Atom('p')), Not(Atom('q')))
        >>> push_negation_inward(Not(Or(Atom('p'), Atom('q'))))
        And(Not(Atom('p')), Not(Atom('q')))

    Hint: Cuando encuentres un Not, revisa que hay adentro:
          - Si es Not(And(...)): aplica De Morgan para convertir en Or de negaciones.
          - Si es Not(Or(...)): aplica De Morgan para convertir en And de negaciones.
          - Si es Not(Atom): dejar como esta.
          Para And y Or sin negacion encima, simplemente recursa sobre los hijos.

    Nota: Esta funcion se llama DESPUES de eliminar Iff e Implies,
          asi que no necesitas manejar esos tipos.
    """
    #DECLARACIÓN DE USO DE IA
    # Esta función fue refinada con apoyo de IA después de una versión inicial
    # La ayuda se enfocó en revisar la recursión y la correcta
    # aplicación de leyes de De Morgan y doble negación.
    #
    # Prompt usado:
    # "Revisa esta función en Python para push_negation_inward y sugiere
    # correcciones para empujar negaciones hacia adentro correctamente,
    # manejando Not, And, Or y doble negación sin cambiar la interfaz."

    # === YOUR CODE HERE ===
    if isinstance(formula, Atom):
        return formula
    if isinstance(formula,Not):
        inside = formula.operand

        if isinstance(inside,Atom):
            return formula

        if isinstance(inside, Not):
            return push_negation_inward(inside.operand)

        if isinstance(inside, And):
            return Or(*(push_negation_inward(Not(c)) for c in inside.conjuncts))

        if isinstance(inside,Or):
            return And(*(push_negation_inward(Not(d)) for d in inside.disjuncts))

    if isinstance(formula, And):
        return And(*(push_negation_inward(c) for c in formula.conjuncts))

    if isinstance(formula,Or):
        return Or(*(push_negation_inward(d) for d in formula.disjuncts))

    return formula
    # === END YOUR CODE ===


def distribute_or_over_and(formula: Formula) -> Formula:
    """
    Distribuye Or sobre And para obtener CNF.

    Transformacion:
        Or(A, And(B, C)) -> And(Or(A, B), Or(A, C))

    Debe aplicarse recursivamente hasta que no queden Or que contengan And.

    Ejemplo:
        >>> distribute_or_over_and(Or(Atom('p'), And(Atom('q'), Atom('r'))))
        And(Or(Atom('p'), Atom('q')), Or(Atom('p'), Atom('r')))

    Hint: Para un nodo Or, primero distribuye recursivamente en los hijos.
          Luego busca si algun hijo es un And. Si lo encuentras, aplica la
          distribucion y recursa sobre el resultado (podria haber mas).
          Para And, simplemente recursa sobre cada conjuncion.
          Atomos y Not se retornan sin cambio.

    Nota: Esta funcion se llama DESPUES de mover negaciones hacia adentro,
          asi que solo veras Atom, Not(Atom), And y Or.
    """

    #DECLARACIÓN DE USO DE IA
    # Esta función fue refinada con apoyo de IA después de una versión inicial
    #La ayuda se usó para revisar los casos en que una disyunción
    # debe distribuirse sobre una conjunción y cómo hacerlo de forma recursiva
    #sin alterar la semántica de la fórmula.
    #
    # Prompt usado:
    # "Ayúdame a corregir una función distribute_or_over_and en Python para
    # fórmulas lógicas, distribuyendo Or sobre And de manera recursiva y
    # conservando la estructura e interfaz existentes."

    # === YOUR CODE HERE ===
    if isinstance(formula, (Atom, Not)):
        return formula

    if isinstance(formula, And):
        return And(*(distribute_or_over_and(c) for c in formula.conjuncts))

    if isinstance(formula, Or):
        parts = [distribute_or_over_and(d) for d in formula.disjuncts]

        and_index = None
        for i, part in enumerate(parts):
            if isinstance(part, And):
                and_index = i
                break

        if and_index is None:
            return Or(*parts)

        and_part = parts[and_index]
        other_parts = parts[:and_index] + parts[and_index + 1:]

        new_conjuncts = []
        for conjunct in and_part.conjuncts:
            new_or = Or(conjunct, *other_parts)
            new_conjuncts.append(distribute_or_over_and(new_or))

        return And(*new_conjuncts)

    return formula
    # === END YOUR CODE ===


def flatten(formula: Formula) -> Formula:
    """
    Aplana conjunciones y disyunciones anidadas.

    Transformaciones:
        And(And(a, b), c) -> And(a, b, c)
        Or(Or(a, b), c)   -> Or(a, b, c)

    Debe aplicarse recursivamente.

    Ejemplo:
        >>> flatten(And(And(Atom('a'), Atom('b')), Atom('c')))
        And(Atom('a'), Atom('b'), Atom('c'))
        >>> flatten(Or(Or(Atom('a'), Atom('b')), Atom('c')))
        Or(Atom('a'), Atom('b'), Atom('c'))

    Hint: Para un And, recorre cada hijo. Si un hijo tambien es And,
          agrega sus conjuncts directamente en vez de agregar el And.
          Igual para Or con sus disjuncts.
          Si al final solo queda 1 elemento, retornalo directamente.
    """

    #DECLARACIÓN DE USO DE IA
    # Esta función fue refinada con apoyo de IA después de una versión inicial
    # La ayuda se centró en identificar cómo aplanar correctamente
    # conjunciones y disyunciones anidadas, evitando dejar estructuras
    # redundantes dentro del árbol de la fórmula.
    #
    #Prompt usado(aproximado):
    # "Revisa esta función flatten en Python y sugiere una forma correcta de
    # aplanar And y Or anidados recursivamente, manteniendo la misma interfaz
    # y sin cambiar el significado lógico de la expresión."

    # === YOUR CODE HERE ===
    if isinstance(formula, Atom):
        return formula

    if isinstance(formula, Not):
        return Not(flatten(formula.operand))

    if isinstance(formula, And):
        new_conjuncts = []

        for conjunct in formula.conjuncts:
            flat_conjunct = flatten(conjunct)
            if isinstance(flat_conjunct, And):
                new_conjuncts.extend(flat_conjunct.conjuncts)
            else:
                new_conjuncts.append(flat_conjunct)

        if len(new_conjuncts) == 1:
            return new_conjuncts[0]

        return And(*new_conjuncts)

    if isinstance(formula, Or):
        new_disjuncts = []

        for disjunct in formula.disjuncts:
            flat_disjunct = flatten(disjunct)
            if isinstance(flat_disjunct, Or):
                new_disjuncts.extend(flat_disjunct.disjuncts)
            else:
                new_disjuncts.append(flat_disjunct)

        if len(new_disjuncts) == 1:
            return new_disjuncts[0]

        return Or(*new_disjuncts)

    return formula
    # === END YOUR CODE ===


# --- PIPELINE COMPLETO ---


def to_cnf(formula: Formula) -> Formula:
    """
    [DADO] Pipeline completo de conversion a CNF.

    Aplica todas las transformaciones en el orden correcto:
    1. Eliminar bicondicionales (Iff)
    2. Eliminar implicaciones (Implies)
    3. Mover negaciones hacia adentro (Not)
    4. Eliminar dobles negaciones (Not Not)
    5. Distribuir Or sobre And
    6. Aplanar conjunciones/disyunciones

    Ejemplo:
        >>> to_cnf(Implies(Atom('p'), And(Atom('q'), Atom('r'))))
        And(Or(Not(Atom('p')), Atom('q')), Or(Not(Atom('p')), Atom('r')))
    """
    formula = eliminate_iff(formula)
    formula = eliminate_implication(formula)
    formula = push_negation_inward(formula)
    formula = eliminate_double_negation(formula)
    formula = distribute_or_over_and(formula)
    formula = flatten(formula)
    return formula
