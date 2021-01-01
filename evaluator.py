from error_handling import EvalError, ApplyError

underlying_eval = eval


def eval(exp, env):
    if is_self_evaluating(exp):
        return exp
    elif is_variable(exp):
        try:
            return env.get_binding(exp)
        except NameError:
            tokens = exp.split(".", 1)
            if len(tokens) > 1:
                procedure = getattr(env.get_binding(tokens[0]), tokens[1])
                return ['primitive', procedure]
    elif is_quoted(exp):
        return text_of_quotation(exp)
    elif is_assignment(exp):
        return eval_assignment(exp, env)
    elif is_definition(exp):
        return eval_definition(exp, env)
    elif is_if(exp):
        return eval_if(exp, env)
    elif is_lambda(exp):
        return make_procedure(lambda_parameters(exp), lambda_body(exp), env)
    elif is_begin(exp):
        return eval_sequence(begin_actions(exp), env)
    elif is_cond(exp):
        return eval(cond2if(exp), env)
    elif is_import(exp):
        return eval_import(import_operand(exp), env)
    # Any non-empty list not processed yet will be regarded as procedure
    elif is_application(exp):
        return apply(eval(operator(exp), env), list_of_values(operands(exp), env))
    else:
        raise EvalError("Unknown expression {} in function EVAL".format(exp))


def apply(procedure, arguments):
    if is_primitive_procedure(procedure):
        return apply_primitive_procedure(procedure, arguments)
    elif is_compound_procedure(procedure):
        return eval_sequence(procedure_body(procedure),
                             procedure_environment(procedure).extend_environment(procedure_parameters(procedure),
                                                                                 arguments))
    else:
        raise ApplyError("Unknown procedure {} in function apply".format(procedure))


def is_primitive_procedure(procedure):
    """Determine whether `procedure` is a list of atoms
    whose tag is "primitive"
    """
    return is_tagged_list(procedure, "primitive")


def primitive_implementation(procedure):
    """Primitive procedure is of the form ["primitive", procedure-implementation].
    """
    return procedure[1]


def apply_primitive_procedure(procedure, arguments):
    # try:
    return primitive_implementation(procedure)(*arguments)


# except TypeError as e:
#     print("primitive_procedure {} ".format(e.message))
#     raise e


def is_compound_procedure(procedure):
    """Determine whether `procedure` is a list of atoms
    whose tag is "procedure"
    """
    return is_tagged_list(procedure, "procedure")


def make_procedure(parameters, body, env):
    return ["procedure", parameters, body, env]


def procedure_parameters(procedure):
    return procedure[1]


def procedure_body(procedure):
    return procedure[2]


def procedure_environment(procedure):
    return procedure[3]


def is_self_evaluating(exp):
    """Determine whether `exp` is an integer, a float or a string.
    """
    return is_number(exp) or is_string(exp)


def is_variable(exp):
    """Determine whether `exp` is a symbol
    """
    return is_symbol(exp)


def is_quoted(exp):
    """Determine whether `exp` is a list of atoms whose tag is "quote"
    """
    return is_tagged_list(exp, "quote")


def text_of_quotation(exp):
    """By Scheme standard, quote expression is of the form
    (quote datum)."""
    return exp[1]


def is_assignment(exp):
    """Determine whether `exp` is a list of atoms whose tag is "set!"
    """
    return is_tagged_list(exp, "set!")


def eval_assignment(exp, env):
    """Assignment expression of Scheme is of form `(set! variable value)`"""
    env.set_binding(assignment_variable(exp),
                    eval(assignment_value(exp), env))
    return "ok"


def assignment_variable(exp):
    return exp[1]


def assignment_value(exp):
    return exp[2]


def is_definition(exp):
    """Determine whether `exp` is a list of atoms whose tag is "define"
    """
    return is_tagged_list(exp, "define")


def eval_definition(exp, env):
    env.define_binding(definition_variable(exp), eval(definition_value(exp), env))
    return "ok"


def definition_variable(exp):
    # eg: (define n 1)
    if is_symbol(exp[1]):
        return exp[1]
    else:
        # eg: (define (foo n) (+ 1 n))
        return exp[1][0]


def definition_value(exp):
    # eg: (define n 1)
    if is_symbol(exp[1]):
        return exp[2]
    else:
        # eg: (define (foo n) (+ 1 n) (+ 3 n))
        return make_lambda(exp[1][1:], exp[2:])


def is_if(exp):
    """Determine whether `exp` is a list of atoms whose tag is "if"
    """
    return is_tagged_list(exp, "if")


def eval_if(exp, env):
    if eval(if_predicate(exp), env):
        return eval(if_consequent(exp), env)
    else:
        # When if_alternative(exp) returns `False`, eval(False) evaluates to False since 
        # boolean is subtype of int, and int is self-evaluating.
        return eval(if_alternative(exp), env)


def if_predicate(exp):
    # eg: (if (< n 1) 1 2)
    return exp[1]


def if_consequent(exp):
    return exp[2]


def if_alternative(exp):
    if len(exp) >= 4:
        return exp[3]
    else:
        # The value of an `if` expression when the predicate
        # is false and there is no alternative is unspecified
        # in Scheme; we have chosen here to make it false.
        return False


def is_lambda(exp):
    """Determine whether `exp` is a list of atoms whose tag is "lambda"
    """
    return is_tagged_list(exp, "lambda")


def lambda_parameters(exp):
    """Lambda expression of Scheme is of the form
    `(lambda formals expression...)`.
    """
    return exp[1]


def lambda_body(exp):
    """Lambda expression of Scheme is of the form
    `(lambda formals expression...)`, and lambda body is a list of experssions.
    """
    return exp[2:]


def make_lambda(parameters, body):
    """Lambda expression of Scheme is of the form
    `(lambda formals expression...)`.
    """
    return ["lambda", parameters] + body


def is_begin(exp):
    """Determine whether `exp` is a list of atoms whose tag is "begin"
    """
    return is_tagged_list(exp, "begin")


def begin_actions(exp):
    return exp[1:]


def eval_sequence(exps, env):
    for exp in exps:
        result = eval(exp, env)
    return result


def is_cond(exp):
    """Determine whether `exp` is a list of atoms whose tag is "cond"
    """
    return is_tagged_list(exp, "cond")


def cond2if(exp):
    """Convert `cond` expression to `if` expression"""
    return expand_clauses(cond_clauses(exp))


def cond_clauses(exp):
    """`cond` expression of Scheme has the form (cond clause...).
    """
    return exp[1:]


def is_cond_else_clause(clause):
    return cond_predicate(clause) == "else"


def cond_predicate(clause):
    """Each clause of cond expression has the form (predicate expression...).
    """
    return clause[0]


def cond_actions(clause):
    """Each clause of cond expression has the form (predicate expression...).
    """
    return clause[1:]


def expand_clauses(clauses):
    """The value of a cond expression when all the predicates are false
    and there is no `else` clause is unspecified in Scheme; we have chosen here to make it False. 
    The `else` clause must be the last clause of the cond expression.
    """
    if len(clauses) == 0:
        return False
    else:
        first = clauses[0]
        rest = clauses[1:]
        if is_cond_else_clause(first):
            if len(rest) == 0:
                return sequence2exp(cond_actions(first))
            else:
                raise SyntaxError("ELSE clause {} isn't the last clause of the cond expression".format(first))
        else:
            return make_if(cond_predicate(first), sequence2exp(cond_actions(first)), expand_clauses(rest))


def sequence2exp(seq):
    """If seq is empty list, return empty list; if seq is a list of one expression, return the expression;
    otherwise, convert seq to `begin` expression.
    """
    if len(seq) == 0:
        return seq
    elif len(seq) == 1:
        return seq[0]
    else:
        return make_begin(seq)


def make_if(predicate, consequent, alternative):
    """Given `predicate` part, `consequent` part and `alternative` part,
    construct a new `if` expression.
    """
    return ["if", predicate, consequent, alternative]


def make_begin(seq):
    return ["begin"] + seq


def is_application(exp):
    return is_non_empty_list(exp)


def operator(exp):
    return exp[0]


def operands(exp):
    return exp[1:]


def list_of_values(exps, env):
    return [eval(exp, env) for exp in exps]


def is_tagged_list(exp, tag):
    """Determine whether `exp` is a non-empty list
       and the first element of `exp` is `tag`
    """
    return is_non_empty_list(exp) and (exp[0] == tag)


def is_non_empty_list(exp):
    return isinstance(exp, list) and len(exp) > 0


def is_number(exp):
    """Determine whether `exp` is a number.
    """
    try:
        float(exp)
        return True
    except:
        return False


def is_string(exp):
    return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'


def is_symbol(exp):
    return isinstance(exp, str) and (exp[0] != '"' or exp[-1] != '"')


def is_import(exp):
    return is_tagged_list(exp, "import")


def eval_import(exp, env):
    exec("import " + exp)
    module = exp.split(".", 1)[0]
    env.define_binding(module, underlying_eval(module))


def import_operand(exp):
    return exp[1]
