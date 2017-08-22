#!/usr/bin/env python
# coding=utf-8

def parseInput(input, index, result):
    n = len(input)
    i = index
    while i < n:
        if input[i].isspace():
            while i < n and input[i].isspace():
                i += 1
        elif input[i] == "'":
            pass
        elif input[i] == '(':
            result.append([])
            i = parseInput(input, i + 1, result[-1])
        elif input[i] == ')':
            return i + 1
        else:
            l = []
            while i < n and (not input[i].isspace()) and input[i] != '(' and input[i] != ')':
                l.append(input[i])
                i += 1
            string = ''.join(l)
            if string.isdigit():
                result.append(int(string))
            else:
                try:
                    result.append(float(string))
                except:
                    result.append(string)

def formatOutput(output):
    if isinstance(output, list):
        return '(' + ' '.join(str(formatOutput(element)) for element in output) + ')'
    else:
        return str(output)

