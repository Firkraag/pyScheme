#!/usr/bin/env python
# coding=utf-8

def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def sub(a, b):
    return a - b


def div(a, b):
    return 1.0 * a / b


def less(a, b):
    return a < b


def equal(a, b):
    return a == b


def cons(exp, l):
    """The primitive `cons` takes two arguments.
    The second argument to `cons` must be a list. The result is a list.
    """
    if isinstance(l, list):
        return [exp] + l
    else:
        raise TypeError("The second argument to cons must be a list")


def car(l):
    """Returns the first element of a list.
    
    The primitive `car` is defined only for non-empty list
    """
    if isinstance(l, list) and len(l) > 0:
        return l[0]
    else:
        raise TypeError("The argument to car must be a non-empty list")


def cdr(l):
    """Return rest elements of a list.
    
    The primitive `cdr` is defined only for non-empty list 
    The `cdr` of any non-empty list is always another list."""
    if isinstance(l, list) and len(l) > 0:
        return l[1:]
    else:
        raise TypeError("The argument to cdr must be a non-empty list")


def null(l):
    """Determine whether the list is null.

    The primitive `null?` is defined only for lists.
    """
    if isinstance(l, list):
        return len(l) == 0
    else:
        raise TypeError("The argument to null? must be a list")


def set_car(pair, value):
    pair[0] = value


def set_cdr(pair, value):
    pair[1] = value


def same(obj1, obj2):
    """The primitive eq'l takes two arguments.
    Each must be a non-numeric atom."""
    return obj1 is obj2


def assignment(x, y):
    x = y


def pair(item):
    """Determine whether `item` is a not-empty list.
    """
    return isinstance(item, list) and len(item) >= 1


def atom(exp):
    """Determine whether `exp` is an atom.
    """
    return not isinstance(exp, list)


def And(bool1, bool2):
    return bool1 and bool2


def Or(bool1, bool2):
    return bool1 or bool2


def eq(exp1, exp2):
    pass


def Not(bool):
    return not bool


def length(list):
    return len(list)


def display(item):
    print(item, end=' ')


def newline():
    print()


primitive_procedures = {"+": add, "-": sub, "*": mul, "/": div, "<": less, "=": equal, "cons": cons, "car": car,
                        "cdr": cdr, "set-car!": set_car, "set-cdr!": set_cdr, "eq?": equal, "null?": null,
                        "pair?": pair, "and": And, "or": Or, "not": Not, "atom?": atom, "length": length,
                        "display": display, "newline": newline}
primitive_procedure_names = primitive_procedures.keys()
primitive_procedure_objects = map(lambda proc: ["primitive", proc], primitive_procedures.values())
