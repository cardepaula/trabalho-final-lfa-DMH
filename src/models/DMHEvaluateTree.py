# -*- coding: utf-8 -*-

'''
    Classe responsável por realizar o evaluation da árvore (AST) da expressão/código 
    passada como entrada seguindo as regras definidas pela gramática da linguagem DMH
'''

import sys, os, math
from lark import Tree


class DMHEvaluateTree:
    def __init__(self, tree: Tree = None):
        self._vars = {}
        self._functs = {}
        self._tree = tree

    @property
    def tree(self) -> Tree:
        return self._tree

    @tree.setter
    def tree(self, value: Tree):
        self._tree = value

    def evaluete(self):
        return self.__start(self._tree)

    def teste(self, *args):
        return "Testing"

    # Métodos relativos a operações lógicas e matemáticas #
    from operator import add, sub, mul, truediv as div, floordiv, mod, pos, neg, pow, eq, ne, lt, le, gt, ge

    # Método de conversão para um float #
    def __number(self, t: Tree):
        token = t.children[0]
        return float(token.value)

    # Métodos para o handler de variáveis (assinatura, reassinatura e recuperação) #
    def __assign_var(self, t: Tree):

        name = t.children[1]
        value = t.children[2]

        if (name not in self._vars):
            print("VAR '{0}' Nao existe ainda.".format(name))
            print("VALUE:", value)
            self.__aexpr(value)
        else:
            raise Exception("Error: Variable '{0}' is already defined".format(name))

        # for child in t.children:
            # if child.children == "var" :
            # if (name not in self.vars):
            #     self.vars[name] = value
            #     return value

    def __reassign_var(self, t: Tree):

        name = t.children[0]
        value = t.children[1]

        if name in self._vars:
            print("VAR '{0}' Existe.".format(name))
            print("VALUE:", value)
            self.__aexpr(value)
        else:
            raise Exception("Error: Variable '{0}' is not defined".format(name))



    def __get_var(self, name):
        pass
        #if (name in self._vars):
        #    return self._vars[name]
        
        raise Exception("Error: Variable {0} does not exist".format(name))

    # Métodos lida com operações trigonométricas recebendo valor em graus #
    def __sen(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.sin(radian), 10)

    def __cos(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.cos(radian), 10)

    def __tang(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.tan(radian), 10)

    def __arcsen(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.asin(radian), 10)

    def __arccos(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.acos(radian), 10)

    def __arctang(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.atan(radian), 10)

    # Métodos que lida com estruturas de condição(if) e repetição(while)
    def __if_expr(self, valExpr1, valExpr2, valExpr3 = None):
        # if (valExpr1):
        #     return valExpr2
        # else:
        #     return valExpr3
        # print("xD")
        pass

    def __while_expr(self, valExpr1, valExpr2):
        #while (valExpr1):
        #     valExpr2
        # print("xD")
        pass

    ###
    def __start(self, t: Tree):
        print(t.children)
        child = t.children[0]
        return self.__expr(child)

    def __expr(self, t: Tree):
        child = t.children[0]

        if child.data == 'assign_var':
            return self.__assign_var(child)
        elif child.data == 'if_expr':
            return self.__if_expr(child)
        elif child.data == 'while_expr':
            return self.__while_expr(child)
        elif child.data == 'def_function':
            return self.__def_function(child)
        elif child.data == 'block':
            return self.__block(child)
        elif child.data == 'aexpr':
            return self.__aexpr(child)
        elif child.data == 'print_screen':
            return self.__print_screen(child)
        elif child.data == 'term_operation':
            return self.__term_operation(child)


    def __def_function(self, t: Tree):
        print("DEF_FUNCTION >>>", t.data)

    def __block(self, t: Tree):
        print("BLOCK >>>", t.data)

    def __aexpr(self, t: Tree):
        first_child = t.children[0]

        if first_child.data == "term":
            return self.__term(first_child)
        elif first_child.data == "aexpr":
            return self.__term_operation(first_child)
        elif first_child.data == "factor_operation":
            return self.__factor_operation(first_child)

    def __term(self, t: Tree):
        child = t.children[0]

        if child.data == "factor":
            return self.__factor(child)
        elif child.data == "factor_operation":
            return self.__factor_operation(child)
        elif child.data == "pow_operation":
            return self.__pow_operation(child)

    def __term_operation(self, t: Tree):
        aexpr = self.__aexpr(t.children[0])
        op = t.children[1]
        term = self.__term(t.children[2])

        if op == "+":
            return aexpr + term
        elif op == "-":
            return aexpr - term

    def __factor(self, t: Tree):
        if t.children[0].data == "trig":
            return self.__trig(t.children[0])
        elif t.children[2].data == "factor":
            return self.__pow_operation(t.children[2])
        elif t.children[0].data == "trig_operation":
            return self.__trig_operation(t.children[0])

    def __factor_operation(self, t: Tree):
        term = self.__term(t.children[0])
        op = t.children[1]
        factor = self.__factor(t.children[2])
        if op == "//":
            return term // factor
        elif op == "*":
            return term * factor
        elif op == "/":
            return term / factor
        elif op == "%":
            return term % factor

    def __trig(self, t: Tree):
        child = t.children[0]
        if child.data == "base":
            return self.__base(child)
        elif child.data == "left_operation":
            return self.__left_operation(child)
        elif child.data == "number":
            return self.__number(child)
        elif child.data == "get_var":
            return self.__get_var(child)
        elif child.data == "trig_operation":
            return self.__trig_operation(child)

    def __pow_operation(self, t: Tree):
        trig = self.__term(t.children[0])
        factor = self.__factor(t.children[2])
        return trig ** factor

    def __base(self, t: Tree):
        child = t.children[0]
        if child.data == "functcall":
            pass
        elif child.data == "aexpr":
            return self.__aexpr(child)


    def __trig_operation(self, t: Tree):
        op = t.children[0]
        base = t.children[1]

        if op == 'sen':
            self.__sen(base)
        elif op == 'cos':
            self.__cos(base)
        elif op == 'tang':
            self.__tang(base)
        elif op == 'arcsen':
            self.__arcsen(base)
        elif op == 'arccos':
            self.__arccos(base)
        elif op == 'arctang':
            self.__arctang(base)


    def __print_screen(self, t: Tree):
        print("PRINT_SCREEN >>>", t.data)


def testExpressions():
    from DMHParser import DMHParser

    parser: DMHParser = DMHParser()
    valueteTree: DMHEvaluateTree = DMHEvaluateTree()
    expressions: list = ["2 + 2;",
                         "3 * 23;",
                         "3 - 2 * 7;",
                         "2 // 20;",
                         "+++2 - 4.0 / ----1.;",
                         "34 + 213 + 2.12 / 21;",
                         "10 * 5 + 100 / 10 - 5 + 7 % 2;",
                         "(10) * 5 + (100 // 10) - 5 + (7 % 2);",
                         "-((2+2)*2)-((2-0)+2);",
                         "(2.*(2.0+2.))-(2.0+(2.-0));",
                         "-(100) + 21 / (43 % 2);",
                         "3^4+5*(2-5);",
                         "3^2+5//(2-5);",
                         "2^2^2^-2;",
                         "0.02e2 + 0.02e-2;",
                         "8^-2 + 2E1 * 2e-1 + 3e+3 / 2.012;",
                         "8^2 + 2E1 * 2e-1 + 3e+3 // 2.;",
                         "(-2.3)^2 + 2.2E1 * 2e-12 + 1e+3;"]

    for expr in expressions:
        tree = parser.parseTree(expr)
        valueteTree.tree = tree
        aux = valueteTree.evaluete()
        print("Expression: {0} = {1}".format(expr, aux))


if __name__ == '__main__':
    testExpressions()
