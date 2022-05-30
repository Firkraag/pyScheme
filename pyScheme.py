#!/usr/bin/env python

import sys
from environment import Environment
from evaluator import eval
from io_handling import parseInput, formatOutput
from primitive_procedure import primitive_procedure_names, primitive_procedure_objects


def load(filename):
    """Load scheme source file `filename`
    """
    # The parameter filename is of the form '"path"'
    filename = filename[1:-1]
    with open(filename) as file:
        input = file.read()
    result = []
    parseInput(input, 0, result)
    for exp in result:
        output = eval(exp, the_global_environment)
    return output


primitive_procedure_objects.append(['primitive', load])
the_global_environment = Environment(list(primitive_procedure_names) + ['load'], primitive_procedure_objects)
load('"./init.scm"')

if __name__ == "__main__":
    if len(sys.argv) == 1:
        while True:
            expressions = input("Input: ")
            result = []
            parseInput(expressions, 0, result)
            for exp in result:
                print(formatOutput(eval(exp, the_global_environment)))
    else:
        with open(sys.argv[1]) as file:
            input = file.read()
        result = []
        parseInput(input, 0, result)
        for exp in result:
            print(formatOutput(eval(exp, the_global_environment)))
