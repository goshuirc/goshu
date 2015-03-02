# Numeric String Parser
# See license text in pyparsing.py

# Modifications by Daniel Oaks, same license
#
# Comply more strictly with PEP8, traditional Python style.
# Add PI and E constants.
# Add sin, cos, etc functions.
# Add power ops, ^ and **
# Split out multMap, compMap, etc for better extensibility.
# Renamed Arith() to NumericStringParser() to be more general.

# Modifications by Glenn Linderman, same license
#
# Python 3.2
# Eliminate LE and friends, stick with Python comparison ops
# Merge separate precedence lists
# Make a single class Arith to be the interface
# Keep vars_ in Arith instances, so multiple instances could have
#   different vars/values
# Add // and % to multOp & EvalMultOp
# Keep integer values as integers until something converts them
# Allow longer var names

# Based on:
#
# eval_arith.py
#
# Copyright 2009, Paul McGuire
#
# Expansion on the pyparsing example simpleArith.py, to include evaluation
# of the parsed tokens.
from __future__ import print_function
from __future__ import division

import math

from pyparsing import (Word, nums, alphas, Combine, oneOf, Optional,
    opAssoc, operatorPrecedence)

# details
__version__ = '11.7.17'

# maps
constMap = {
    'pi': math.pi,  # 3.141592
    'PI': math.pi,  # 3.141592
    'E': math.e,  # 2.718281828
}

multMap = {
    '*': lambda a,b : a * b,
    '/': lambda a,b : a / b,
    '//': lambda a,b : a // b,
    '%': lambda a,b : a % b,
    '^': lambda a,b : a ** b,
    '**': lambda a,b : a ** b,
}

compMap = {
    '<': lambda a,b : a < b,
    '<=' : lambda a,b : a <= b,
    '>': lambda a,b : a > b,
    '>=' : lambda a,b : a >= b,
    '==' : lambda a,b : a == b,
    '!=' : lambda a,b : a != b,
    '<>' : lambda a,b : a != b,
}

fnMap = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'abs': abs,
    'trunc': lambda a: int(a),
    'round': round,
    'floor': math.floor,
    'ceil': math.ceil,
    'sgn': lambda a: abs(a) > epsilon and cmp(a, 0) or 0,
}


# classes
class EvalConstant():
    """Class to evaluate a parsed constant or variable."""
    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self, vars_):
        if self.value in vars_:
            return vars_[self.value]
        elif self.value in constMap:
            return constMap[self.value]
        else:
            try:
                return int( self.value )
            except:
                return float(self.value)


class EvalSignOp():
    """Class to evaluate expressions with a leading + or - sign."""
    def __init__(self, tokens):
        self.sign, self.value = tokens[0]

    def eval(self, vars_):
        mult = {'+': 1, '-': -1}[self.sign]
        return mult * self.value.eval(vars_)


def operatorOperands(tokenlist):
    """generator to extract operators and operands in pairs."""
    it = iter(tokenlist)
    while True:
        try:
            o1 = next(it)
            o2 = next(it)
            yield (o1, o2)
        except StopIteration:
            break


class EvalMultOp():
    """Class to evaluate multiplication and division expressions."""
    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self, vars_):
        prod = self.value[0].eval(vars_)
        for op, val in operatorOperands(self.value[1:]):
            fn = multMap[op]
            val2 = val.eval(vars_)
            prod = fn(prod, val2)
        return prod


class EvalAddOp():
    """Class to evaluate addition and subtraction expressions."""
    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self, vars_):
        sum = self.value[0].eval(vars_)
        for op,val in operatorOperands(self.value[1:]):
            if op == '+':
                sum += val.eval(vars_)
            if op == '-':
                sum -= val.eval(vars_)
        return sum


class EvalComparisonOp():
    """Class to evaluate comparison expressions."""
    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self, vars_):
        val1 = self.value[0].eval(vars_)
        for op, val in operatorOperands(self.value[1:]):
            fn = compMap[op]
            val2 = val.eval(vars_)
            if not fn(val1, val2):
                break
            val1 = val2
        else:
            return True
        return False


class EvalFnOp():
    """Class to evaluate functions."""
    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self, vars_):
        op, val = self.value
        return fnMap[op](val.eval(vars_))


# base parser
class NumericStringParser():
    """Parses the given input string, calculates it, and outputs a result.

    Most of this code comes from the arith.py pyparsing example
    """
    # define the parser
    integer = Word(nums)
    real = ( Combine(Word(nums) + Optional('.' + Word(nums))
                     + oneOf('E e') + Optional( oneOf('+ -')) + Word(nums))
             | Combine(Word(nums) + '.' + Word(nums))
             )
         
    variable = Word(alphas)
    operand = real | integer | variable

    signop = oneOf('+ -')
    multop = oneOf(' '.join(multMap.keys()))
    plusop = oneOf('+ -')
    comparisonop = oneOf(' '.join(compMap.keys()))
    fnop = oneOf(' '.join(fnMap.keys()))

    # use parse actions to attach EvalXXX constructors to sub-expressions
    operand.setParseAction(EvalConstant)
    arith_expr = operatorPrecedence(operand,
        [(signop, 1, opAssoc.RIGHT, EvalSignOp),
         (multop, 2, opAssoc.LEFT, EvalMultOp),
         (plusop, 2, opAssoc.LEFT, EvalAddOp),
         (comparisonop, 2, opAssoc.LEFT, EvalComparisonOp),
         (fnop, 1, opAssoc.RIGHT, EvalFnOp),
         ])

    def __init__(self, vars_={}):
        self.vars_ = vars_

    def setvars(self, vars_):
        self.vars_ = vars_

    def setvar(self, var, val):
        self.vars_[var] = val

    def eval(self, strExpr):
        ret = self.arith_expr.parseString(strExpr, parseAll=True)[0]
        result = ret.eval(self.vars_)
        return result


if __name__=='__main__': 
    def main():
        # sample expressions posted on comp.lang.python, asking for advice
        # in safely evaluating them
        rules=[
             '( A - B ) == 0', 
             '(A + B + C + D + E + F + G + H + I) == J', 
             '(A + B + C + D + E + F + G + H) == I', 
             '(A + B + C + D + E + F) == G', 
             '(A + B + C + D + E) == (F + G + H + I + J)', 
             '(A + B + C + D + E) == (F + G + H + I)', 
             '(A + B + C + D + E) == F', 
             '(A + B + C + D) == (E + F + G + H)', 
             '(A + B + C) == (D + E + F)', 
             '(A + B) == (C + D + E + F)', 
             '(A + B) == (C + D)', 
             '(A + B) == (C - D + E - F - G + H + I + J)', 
             '(A + B) == C', 
             '(A + B) == 0', 
             '(A+B+C+D+E) == (F+G+H+I+J)', 
             '(A+B+C+D) == (E+F+G+H)', 
             '(A+B+C+D)==(E+F+G+H)', 
             '(A+B+C)==(D+E+F)', 
             '(A+B)==(C+D)', 
             '(A+B)==C', 
             '(A-B)==C', 
             '(A/(B+C))', 
             '(B/(C+D))', 
             '(G + H) == I', 
             '-0.99 <= ((A+B+C)-(D+E+F+G)) <= 0.99', 
             '-0.99 <= (A-(B+C)) <= 0.99', 
             '-1000.00 <= A <= 0.00', 
             '-5000.00 <= A <= 0.00', 
             'A < B', 
             'A < 7000', 
             'A == -(B)', 
             'A == C', 
             'A == 0', 
             'A > 0', 
             'A > 0.00', 
             'A > 7.00', 
             'A <= B', 
             'A < -1000.00', 
             'A < -5000', 
             'A < 0', 
             'A==(B+C+D)', 
             'A==B', 
             'I == (G + H)', 
             '0.00 <= A <= 4.00', 
             '4.00 < A <= 7.00',
             '0.00 <= A <= 4.00 <= E > D',
             '123E0 > 1000E-1 > 99.0987',
             '123E+0',
             '1000E-1',
             '99.0987',
             'abc',
             '20 % 3',
             '14 // 3',
             '12e2 // 3.7',
            ] 
        vars_ = {'A': 0, 'B': 1.1, 'C': 2.2, 'D': 3.3, 'E': 4.4, 'F': 5.5,
                 'G': 6.6, 'H':7.7, 'I':8.8, 'J':9.9, 'abc': 20,}

        # define tests from given rules
        tests = []
        for t in rules:
            tests.append((t, eval(t,vars_)))

        # copy vars_ to EvalConstant lookup dict
        arith = NumericStringParser(vars_)
        for test, expected in tests:
            result = arith.eval(test)
            print(test, expected, result)
            # print(ret)
            if expected != result:
                print('*' * 60 )

    main()
