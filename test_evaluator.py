#!/usr/bin/env python
# coding=utf-8

import unittest
import evaluator as eval
from environment import Environment
from primitive_procedure import primitive_procedure_names, primitive_procedure_objects
from error_handling import EvalError, ApplyError


class EvaluatorTestCase(unittest.TestCase):
    def test_is_self_evaluating(self):
        self.assertTrue(eval.is_self_evaluating(123))
        self.assertTrue(eval.is_self_evaluating('"abc"'))
        self.assertFalse(eval.is_self_evaluating([]))
        self.assertFalse(eval.is_self_evaluating("abc"))
        # Since bool is subtype of int, it is also self-evaluating.
        self.assertTrue(eval.is_self_evaluating(False))
        self.assertTrue(eval.is_self_evaluating(True))

    def test_is_application(self):
        self.assertTrue(eval.is_application(['square', 1, 2]))
        self.assertFalse(eval.is_application(1))
        self.assertFalse(eval.is_application([]))

    def test_is_assignment(self):
        self.assertTrue(eval.is_assignment(["set!", "x", 1]))
        self.assertFalse(eval.is_assignment(["begin", "x", 1]))

    def test_is_begin(self):
        self.assertTrue(eval.is_begin(["begin", 1, 2, 3]))
        self.assertFalse(eval.is_begin([]))
        self.assertFalse(eval.is_begin(1))
        self.assertFalse(eval.is_begin("fad"))

    def test_is_compound_procedure(self):
        self.assertTrue(eval.is_compound_procedure(["procedure", 1, 2, 3]))
        self.assertFalse(eval.is_compound_procedure([]))
        self.assertFalse(eval.is_compound_procedure(1))
        self.assertFalse(eval.is_compound_procedure("fad"))

    def test_is_cond(self):
        self.assertTrue(eval.is_cond(["cond", 1, 2, 3]))
        self.assertFalse(eval.is_cond([]))
        self.assertFalse(eval.is_cond(1))
        self.assertFalse(eval.is_cond("fad"))

    def test_is_definition(self):
        self.assertTrue(eval.is_definition(["define", "x", 1]))
        self.assertFalse(eval.is_definition(["set!", "x", 1]))

    def test_is_if(self):
        self.assertTrue(eval.is_if(["if", "a", "1"]))
        self.assertFalse(eval.is_if(["set!", "x", 1]))

    def test_is_lambda(self):
        self.assertTrue(eval.is_lambda(["lambda"]))
        self.assertFalse(eval.is_lambda(["set!"]))
        self.assertFalse(eval.is_lambda([]))
        self.assertFalse(eval.is_lambda(1))

    def test_is_number(self):
        self.assertTrue(eval.is_number(1))
        self.assertTrue(eval.is_number(1.0))
        self.assertFalse(eval.is_number([]))
        self.assertFalse(eval.is_number([1, 2, 3]))
        # bool is subtype of int
        self.assertTrue(eval.is_number(True))
        self.assertTrue(eval.is_number(False))

    def test_is_primitive_procedure(self):
        self.assertTrue(eval.is_primitive_procedure(["primitive", 1, 2, 3]))
        self.assertFalse(eval.is_primitive_procedure([]))
        self.assertFalse(eval.is_primitive_procedure(1))
        self.assertFalse(eval.is_primitive_procedure("fad"))

    def test_is_quoted(self):
        self.assertTrue(eval.is_quoted(["quote"]))
        self.assertTrue(eval.is_quoted(["quote", 123]))
        self.assertTrue(eval.is_quoted(["quote", 1, 2, 3]))
        self.assertTrue(eval.is_quoted(["quote", "abc", "cde"]))
        self.assertFalse(eval.is_quoted([]))
        self.assertFalse(eval.is_quoted(["begin", "abc"]))

    def test_is_string(self):
        self.assertTrue(eval.is_string('"abc"'))
        self.assertFalse(eval.is_string('abc'))
        self.assertFalse(eval.is_string(1))
        self.assertFalse(eval.is_string([]))
        self.assertFalse(eval.is_string([1, 2, 3]))

    def test_is_symbol(self):
        self.assertTrue(eval.is_symbol("abc"))
        self.assertFalse(eval.is_symbol(1))
        self.assertFalse(eval.is_symbol([]))
        self.assertFalse(eval.is_symbol([1, 2, 3]))

    def test_is_tagged_list(self):
        self.assertFalse(eval.is_tagged_list([], "begin"))
        self.assertTrue(eval.is_tagged_list(["begin", 1, 2], "begin"))

    def test_is_variable(self):
        self.assertTrue(eval.is_variable("adc"))
        self.assertFalse(eval.is_variable([]))
        self.assertFalse(eval.is_variable([1, 2, 3]))

    # def test_is_cond_else_clause(self):
    # self.assertTrue(eval.is_cond_else_clause())
    # self.assertTrue(eval.is_cond_else_clause())

    def test_text_of_quotation(self):
        exp = ['quote', 2]
        self.assertEqual(eval.text_of_quotation(exp), 2)
        exp = ['quote', [1, 2, 3]]
        self.assertEqual(eval.text_of_quotation(exp), [1, 2, 3])

    def test_eval_assignment(self):
        env = Environment(["x"], [1])
        eval.eval_assignment(["set!", "x", 2], env)
        self.assertEqual(env.get_binding("x"), 2)
        with self.assertRaises(NameError):
            eval.eval_assignment(["set!", "y", 1], env)

    def test_assignment_variable(self):
        exp = ["set!", "x", 1]
        self.assertEqual(eval.assignment_variable(exp), "x")

    def test_assignment_value(self):
        exp = ["set!", "x", 1]
        self.assertEqual(eval.assignment_value(exp), 1)

    def test_eval_definition(self):
        env = Environment()
        exp = ["define", "n", 1]
        eval.eval_definition(exp, env)
        self.assertEqual(env.get_binding("n"), 1)
        exp = ["define", ["foo", "n"], ["+", 1, "n"], ["+", 2, "n"]]
        eval.eval_definition(exp, env)
        self.assertEqual(env.get_binding("foo"), ['procedure', ["n"], [["+", 1, "n"], ["+", 2, "n"]], env])

    def test_definition_variable(self):
        exp = ["define", "n", 1]
        self.assertEqual(eval.definition_variable(exp), "n")
        exp = ["define", ["foo", "n"], ["+", 1, "n"], ["+", 2, "n"]]
        self.assertEqual(eval.definition_variable(exp), "foo")

    def test_definition_value(self):
        exp = ["define", "n", 1]
        self.assertEqual(eval.definition_value(exp), 1)
        exp = ["define", ["foo", "n"], ["+", 1, "n"], ["+", 2, "n"]]
        self.assertEqual(eval.definition_value(exp), ['lambda', ["n"], ["+", 1, "n"], ["+", 2, "n"]])

    def test_make_lambda(self):
        parameters = ['x', 'y']
        body = [1, 2]
        self.assertEqual(eval.make_lambda(parameters, body), ['lambda', parameters, 1, 2])
        parameters = ["n"]
        body = [["+", 1, "n"], ["+", 2, "n"]]
        self.assertEqual(eval.make_lambda(parameters, body), ['lambda', ["n"], ["+", 1, "n"], ["+", 2, "n"]])

    def test_lambda_parameters(self):
        exp = ['lambda', ['x', 'y'], 1, 2]
        self.assertEqual(eval.lambda_parameters(exp), ['x', 'y'])

    def test_lambda_body(self):
        exp = ['lambda', ['x', 'y'], 1, 2]
        self.assertEqual(eval.lambda_body(exp), [1, 2])

    def test_make_procedure(self):
        env = Environment()
        parameters = ["x"]
        body = [1, 2]
        self.assertEqual(eval.make_procedure(parameters, body, env), ['procedure', parameters, body, env])

    def test_eval_if(self):
        env = Environment(primitive_procedure_names, primitive_procedure_objects)
        env.define_binding("n", 1)
        exp = ["if", ["<", "n", 1], 1, 2]
        self.assertEqual(eval.eval_if(exp, env), 2)
        env.define_binding("n", 0)
        self.assertEqual(eval.eval_if(exp, env), 1)

    def test_if_predicate(self):
        exp = ["if", ["<", "n", 1], 1, 2]
        self.assertEqual(eval.if_predicate(exp), ["<", "n", 1])

    def test_if_consequent(self):
        exp = ["if", ["<", "n", 1], 1, 2]
        self.assertEqual(eval.if_consequent(exp), 1)

    def test_if_alternative(self):
        exp = ["if", ["<", "n", 1], 1, 2]
        self.assertEqual(eval.if_alternative(exp), 2)
        exp = ["if", ["<", "n", 1], 1]
        self.assertFalse(eval.if_alternative(exp))

    def test_eval_sequence(self):
        env = Environment(primitive_procedure_names, primitive_procedure_objects)
        env.define_binding('n', 1)
        exp = [['set!', 'n', ['+', 'n', 1]], ['set!', 'n', ['+', 'n', 1]]]
        eval.eval_sequence(exp, env)
        self.assertEqual(env.get_binding('n'), 3)

    def test_begin_actions(self):
        exp = ['begin', ['+', 'n', 1], ['*', 'n', 2]]
        self.assertEqual(eval.begin_actions(exp), [['+', 'n', 1], ['*', 'n', 2]])

    def test_cond2if(self):
        clauses = ['cond', ["else", ["-", "n", 1]], [["<", "n", 1], 1]]
        with self.assertRaises(SyntaxError):
            eval.cond2if(clauses)
        clauses = ['cond', [["=", "n", 1], 1], [["=", "n", 2], 2], ["else", 3]]
        if_expr = ["if", ["=", "n", 1], 1, ["if", ["=", "n", 2], 2, 3]]
        self.assertEqual(eval.cond2if(clauses), if_expr)
        clauses = ['cond', [["=", "n", 1], 1], [["=", "n", 2], 2]]
        if_expr = ["if", ["=", "n", 1], 1, ["if", ["=", "n", 2], 2, False]]
        self.assertEqual(eval.cond2if(clauses), if_expr)

    def test_expand_clauses(self):
        clauses = [["else", ["-", "n", 1]], [["<", "n", 1], 1]]
        with self.assertRaises(SyntaxError):
            eval.expand_clauses(clauses)
        clauses = [[["=", "n", 1], 1], [["=", "n", 2], 2], ["else", 3]]
        if_expr = ["if", ["=", "n", 1], 1, ["if", ["=", "n", 2], 2, 3]]
        self.assertEqual(eval.expand_clauses(clauses), if_expr)
        clauses = [[["=", "n", 1], 1], [["=", "n", 2], 2]]
        if_expr = ["if", ["=", "n", 1], 1, ["if", ["=", "n", 2], 2, False]]
        self.assertEqual(eval.expand_clauses(clauses), if_expr)

    def test_cond_clauses(self):
        exp = ['cond', [["<", "n", 1], 1], [[">", "n", 3], 3]]
        clauses = [[["<", "n", 1], 1], [[">", "n", 3], 3]]
        self.assertEqual(eval.cond_clauses(exp), clauses)

    def test_cond_predicate(self):
        clause = [["<", "n", 1], 1]
        self.assertEqual(eval.cond_predicate(clause), ["<", "n", 1])

    def test_cond_actions(self):
        clause = [["<", "n", 1], 1, 2]
        self.assertEqual(eval.cond_actions(clause), [1, 2])

    def test_sequence2exp(self):
        self.assertEqual(eval.sequence2exp([]), [])
        self.assertEqual(eval.sequence2exp([1]), 1)
        self.assertEqual(eval.sequence2exp([1, 2]), ['begin', 1, 2])

    def test_make_if(self):
        predicate = ["<", "n", 1]
        consequent = 1
        alternative = 2
        if_exp = ["if", predicate, consequent, alternative]
        self.assertEqual(eval.make_if(predicate, consequent, alternative), if_exp);

    def test_is_cond_else_clause(self):
        clause = ['else', ["+", "n", 1]]
        self.assertTrue(eval.is_cond_else_clause(clause))
        clause = [["<", "n", 1], ["+", "n", 1]]
        self.assertFalse(eval.is_cond_else_clause(clause))

    def test_operator(self):
        exp = ["square", "n"]
        self.assertEqual(eval.operator(exp), "square")

    def test_operands(self):
        exp = ["square", "n"]
        self.assertEqual(eval.operands(exp), ["n"])

    def test_list_of_values(self):
        env = Environment(primitive_procedure_names, primitive_procedure_objects)
        env.define_binding("n", 1)
        operands = [["+", "n", 1], ["*", "n", "n"]]
        result = [2, 1]
        self.assertEqual(eval.list_of_values(operands, env), result)

    def test_apply_primitive_procedure(self):
        env = Environment(primitive_procedure_names, primitive_procedure_objects)
        add = env.get_binding('+')
        self.assertEqual(eval.apply_primitive_procedure(add, [1, 2]), 3)
        with self.assertRaises(TypeError):
            eval.apply_primitive_procedure(add, [1, 2, 3])

    def test_primitive_implementation(self):
        env = Environment(primitive_procedure_names, primitive_procedure_objects)
        add = env.get_binding('+')
        self.assertEqual(eval.primitive_implementation(add), add[1])

    def test_procedure_body(self):
        env = Environment()
        parameters = ["x"]
        body = [1, 2]
        procedure = eval.make_procedure(parameters, body, env)
        self.assertEqual(eval.procedure_body(procedure), [1, 2])

    def test_procedure_parameters(self):
        env = Environment()
        parameters = ["x"]
        body = [1, 2]
        procedure = eval.make_procedure(parameters, body, env)
        self.assertEqual(eval.procedure_parameters(procedure), parameters)

    def test_procedure_environment(self):
        env = Environment()
        parameters = ["x"]
        body = [1, 2]
        procedure = eval.make_procedure(parameters, body, env)
        self.assertEqual(eval.procedure_environment(procedure), env)

    def test_apply(self):
        env = Environment(primitive_procedure_names, primitive_procedure_objects)
        # test compound procedure
        parameters = ["x"]
        body = [1, 2]
        procedure = eval.make_procedure(parameters, body, env)
        self.assertEqual(eval.apply(procedure, [1]), 2)
        # test primitive procedure
        add = env.get_binding('+')
        self.assertEqual(eval.apply(add, [1, 2]), 3)
        # test exception
        procedure = ["!!!!!", ["x"], [1, 2], env]
        with self.assertRaises(ApplyError):
            eval.apply(procedure, [1])

    def test_eval(self):
        pass
