#!/usr/bn/env python
# coding=utf-8

import unittest
from environment import Environment
from error_handling import ExtendEnvironmentError


class EnvironmentTestCase(unittest.TestCase):
    def setUp(self):
        self.environment = Environment()

    def test_set_binding(self):
        # set binding in first frame
        with self.assertRaises(NameError):
            self.environment.set_binding("a", 1)
        self.environment.define_binding("a", 1)
        self.environment.set_binding("a", 2)
        self.assertEqual(self.environment.get_binding("a"), 2)
        # set binding in other frames
        env = Environment(enclosing_environment=self.environment)
        with self.assertRaises(NameError):
            env.set_binding("b", 1)
        self.environment.set_binding("a", 3)
        self.assertEqual(self.environment.get_binding("a"), 3)

    def test_get_binding(self):
        # get binding from first frame
        with self.assertRaises(NameError):
            self.environment.get_binding("a")
        self.environment.define_binding("a", 1)
        self.assertEqual(self.environment.get_binding("a"), 1)
        # get binding from other frames
        env = Environment(enclosing_environment=self.environment)
        with self.assertRaises(NameError):
            env.get_binding("b")
        self.assertEqual(self.environment.get_binding("a"), 1)

    def test_extend_environment(self):
        variables = "abc"
        values = [1]
        with self.assertRaises(ExtendEnvironmentError):
            self.environment.extend_environment(variables, values)
        variables = "abc"
        values = [1, 2, 3]
        env = self.environment.extend_environment(variables, values)
        frames = env.frames
        it = iter(frames)
        self.assertEqual(next(it), {"a": 1, "b": 2, "c": 3})
        self.assertEqual(next(it), self.environment.first_frame)

    def test_define_binding(self):
        self.environment.define_binding("a", 1)
        self.assertEqual(self.environment.first_frame["a"], 1)
