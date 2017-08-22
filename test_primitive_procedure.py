#!/usr/bin/env python
# coding=utf-8

import unittest
from primitive_procedure import And, Not, Or, add, assignment, car, cdr, cons, div, equal, less, mul, null, pair, same, set_car, set_cdr, sub

class PrimitiveProceduresTestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_mul(self):
        self.assertEqual(mul(1, 2), 2)

    def test_sub(self):
        self.assertEqual(sub(2, 1), 1)

    def test_div(self):
        self.assertEqual(round(div(1, 3), 2), 0.33)

    def test_less(self):
        self.assertTrue(less(1, 2))
        self.assertFalse(less(2, 1))

    def test_equal(self):
        self.assertTrue(equal(2, 2))
        self.assertFalse(equal(1, 2))

    def test_cons(self):
        self.assertTrue(cons(1, [2, 3]), [1, 2, 3])
        with self.assertRaises(TypeError):
            cons(1, 1)

    def test_car(self):
        self.assertEqual(car([1,2,3]), 1)
        with self.assertRaises(TypeError):
            car(1)
        with self.assertRaises(TypeError):
            car([])

    def test_cdr(self):
        self.assertEqual(cdr([1,2,3]), [2, 3])
        self.assertEqual(cdr([1]), [])
        with self.assertRaises(TypeError):
            cdr(1)
        with self.assertRaises(TypeError):
            cdr([])

    def test_null(self):
        self.assertFalse(null([1, 2, 3]))
        self.assertTrue(null([]))
        with self.assertRaises(TypeError):
            null(1)

    def test_And(self):
        self.assertTrue(And(True,  True))
        self.assertFalse(And(True,  False))
        self.assertFalse(And(False, True))
        self.assertFalse(And(False, False))

    def test_Or(self):
        self.assertTrue(Or(True,  True))
        self.assertTrue(Or(True,  False))
        self.assertTrue(Or(False, True))
        self.assertFalse(Or(False, False))

    def test_Not(self):
        self.assertTrue(Not(False))
        self.assertFalse(Not(True))

    def test_atom(exp):
        pass
