# -*- coding: utf-8 -*-

'''
    Classe responsável por realizar o evaluation da árvore (AST) da expressão/código 
    passada como entrada seguindo as regras definidas pela gramática da linguagem DMH
'''

import sys, os, math
from lark import Tree, Token

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
        '''Pega o evaluate tree da parse árvore do objeto'''
        return self.__start(self._tree)

    # Início da gramática
    def __start(self, t: Tree):
        child = t.children[0]
        return self.__expr(child)

    # Seleção das expressões definidas na gramática
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
        else:
            raise Exception("It's not a valid expression.")

    # Assinatura, reassinatura e recuperação de variável
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

    # Estruturas de seleção(if) e repetição(while)
    def __if_expr(self, valExpr1 = None, valExpr2 = None, valExpr3 = None):
        # if (valExpr1):
        #     return valExpr2
        # else:
        #     return valExpr3
        # print("xD")
        pass

    def __while_expr(self, valExpr1 = None, valExpr2 = None):
        #while (valExpr1):
        #     valExpr2
        # print("xD")
        pass

    # Definições e chamadas de funções
    def __def_function(self, t: Tree):
        print("DEF_FUNCTION >>>", t.data)

    # Definição de blocos de escopo do código
    def __block(self, t: Tree):
        print("BLOCK >>>", t.data)

    # Printar informações na tela
    def __print_screen(self, t: Tree):
        print("PRINT_SCREEN >>>", t.data)

    # Lidar com números e cálculos matemáticos em geral #

    # <term> | <aexpr> (+ | -) term
    def __aexpr(self, t: Tree):
        first_child = t.children[0]

        if (first_child.data == "term" and len(t.children) == 1):
            return self.__term(first_child)
        elif (first_child.data == "aexpr" and len(t.children) == 3) :
            return self.__term_operation(t)
        else:
            raise Exception("Invalid math expression.")

    # <factor> | <term> (* | / | // | %) factor
    def __term(self, t: Tree):
        first_child = t.children[0]

        if (first_child.data == "factor" and len(t.children) == 1):
            return self.__factor(first_child)
        elif (first_child.data == "term" and len(t.children) == 3):
            return self.__factor_operation(t)
        else:
            raise Exception("Invalid math expression.")

    # <aexpr> (+ | -) <term> #
    def __term_operation(self, t: Tree):
        aexpr = self.__aexpr(t.children[0])
        op_term = t.children[1].value
        term = self.__term(t.children[2])

        if op_term == '+':
            return aexpr + term
        elif op_term == '-':
            return aexpr - term
        else:
            raise Exception("Invalid term operator. Expect (+ or -) given {0}".format(op_term))

    # <trig> | <factor> ^ <trig>
    def __factor(self, t: Tree):
        first_child = t.children[0]

        if (first_child.data == "trig" and len(t.children) == 1):
            return self.__trig(first_child)
        elif (first_child.data == "factor" and len(t.children) == 3):
            return self.__pow_operation(t)
        else:
            raise Exception("Invalid math expression.")

    # <term> (* | / | // | %) factor #
    def __factor_operation(self, t: Tree):
        term = self.__term(t.children[0])
        op_factor = t.children[1].value
        factor = self.__factor(t.children[2])

        if op_factor == '//':
            return term // factor
        elif op_factor == '*':
            return term * factor
        elif op_factor == '/':
            return term / factor
        elif op_factor == '%':
            return term % factor
        else:
            raise Exception("Invalid factor operator. Expect (*, /, // or %) given {0}".format(op_factor))

    # <factor> ^ <trig> #
    def __pow_operation(self, t: Tree):
        factor = self.__factor(t.children[0])
        op_pow = t.children[1].value
        trig = self.__trig(t.children[2])

        if (op_pow != '^'):
            raise Exception("Invalid pow operator. Expect (^) given {0}".format(op_pow))

        return factor ** trig

    # ('sen' | 'cos' | 'tang' | 'arcsen' | 'arccos' | 'arctang') <base>
    def __trig(self, t: Tree):
        first_child = t.children[0]

        if (isinstance(first_child, Token) and first_child.type == 'TRIG'):
            return self.__trig_operation(t)
        elif (first_child.data == 'base' and len(t.children) == 1):
            return self.__base(first_child)
        else:
            raise Exception("Invalid math expression")
    
    # ('sen' | 'cos' | 'tang' | 'arcsen' | 'arccos' | 'arctang') <base> #
    def __trig_operation(self, t: Tree):
        op_trig = t.children[0].value
        base = self.__base(t.children[1])

        if op_trig == 'sen':
            return self.__sen(base)
        elif op_trig == 'cos':
            return self.__cos(base)
        elif op_trig == 'tang':
            return self.__tang(base)
        elif op_trig == 'arcsen':
            return self.__arcsen(base)
        elif op_trig == 'arccos':
            return self.__arccos(base)
        elif op_trig == 'arctang':
            return self.__arctang(base)
        else:
            raise Exception("Invalid trigonometric operator. Expect (sen, cos, tang, arcsen, arccos or arctang) given {0}".format(op_trig))

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

    # Operações básicas da linguagem
    def __base(self, t: Tree):
        child = t.children[0]

        if child.data == 'leftoperation':
            return self.__left_operation(child)
        elif child.data == 'number':
            return self.__number(child)
        elif child.data == 'getvar':
            pass
        elif child.data == 'functcall':
            pass
        elif child.data == 'aexpr':
            return self.__aexpr(child)

    # (+ | -) <base>
    def __left_operation(self, t: Tree):
        op_left = t.children[0].value
        base = self.__base(t.children[1])

        if (op_left == '-'):
            return -1 * base
        
        return base

    # <number>
    def __number(self, t: Tree):
        token = t.children[0]
        return float(token.value)
    


################################### TESTANDO A CLASSE DE FORMA UNITÁRIA ###################################
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
                         "(-2.3)^2 + 2.2E1 * 2e-12 + 1e+3;",
                         "sen(60);",
                         "cos(90);",
                         "tang(20);",
                         "arccos(15);",
                         "sen(63) * 12 - 321 // 213;"]

    for expr in expressions:
        tree = parser.parseTree(expr)
        valueteTree.tree = tree
        aux = valueteTree.evaluete()
        print("Expression: {0} = {1}".format(expr, aux))


if __name__ == '__main__':
    testExpressions()
