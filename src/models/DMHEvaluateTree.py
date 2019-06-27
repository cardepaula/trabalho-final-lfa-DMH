# -*- coding: utf-8 -*-

'''
    Classe responsável por realizar o evaluation da árvore (AST) da expressão/código 
    passada como entrada seguindo as regras definidas pela gramática da linguagem DMH
'''

import sys, os, math
from lark import Tree


class DMHEvaluateTree:
    def __init__(self, tree: Tree):
        self.__vars = {}
        self.__functs = {}
        self.__tree = tree

    def evaluete(self):
        self.__start(self.__tree)

    def teste(self, *args):
        return "Testing"

    # Métodos relativos a operações lógicas e matemáticas #
    from operator import add, sub, mul, truediv as div, floordiv, mod, pos, neg, pow, eq, ne, lt, le, gt, ge

    # Método de conversão para um float #
    def __number(self, value):
        return float(value)

    # Métodos para o handler de variáveis (assinatura, reassinatura e recuperação) #
    def __assign_var(self, t: Tree):

        name = t.children[1]
        value = t.children[2]

        if (name not in self.__vars):
            print("VAR '{0}' Nao existe ainda.".format(name))
            print("VALUE:", value)
            self.aexpr(value)
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

        if name in self.__vars:
            print("VAR '{0}' Existe.".format(name))
            print("VALUE:", value)
            self.aexpr(value)
        else:
            raise Exception("Error: Variable '{0}' is not defined".format(name))
        


    def __get_var(self, name):
        if (name in self.__vars):
            return self.__vars[name]
        
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
        if (valExpr1):
            return valExpr2
        else:
            return valExpr3
        print("xD")

    def __while_expr(self, valExpr1, valExpr2):
        while (valExpr1):
            valExpr2
        print("xD")

    ###
    def __start(self, t: Tree):
        print(t.children)
        for child in t.children:
            self.expr(child)

    def __expr(self, t: Tree):
        for child in t.children:
            if child.data == 'assign_var':
                print("EXPR_TREE >>>", child)
                print("EXPR >>>", child.data)
                print("EXPR >>>", child.children)
                self.__assign_var(child)
            elif child.data == 'if_expr':
                print("EXPR >>>", t.data)
                self.__if_expr(child)
            elif child.data == 'while_expr':
                print("EXPR >>>", t.data)
                self.__while_expr(child)
            elif child.data == 'def_function':
                print("EXPR >>>", t.data)
                self.__def_function(child)
            elif child.data == 'block':
                print("EXPR >>>", t.data)
                self.__block(child)
            elif child.data == 'aexpr':
                print("EXPR >>>", t.data)
                self.__aexpr(child)
            elif child.data == 'print_screen':
                print("EXPR >>>", t.data)
                self.__print_screen(child)
            elif child.data == 'term_operation':


    def __def_function(self, t: Tree):
        print("DEF_FUNCTION >>>", t.data)

    def __block(self, t: Tree):
        print("BLOCK >>>", t.data)

    def __aexpr(self, t: Tree):
        print("AEXPR >>>", t)
        for child in t.children:
            if child.data == "term":
                print("AEXPR-TERM:", child.data)
                self.__term(child)
            elif child.data == "term_operation":
                print("AEXPR-TERM-OP:", child.data)
                self.__term_operation(child)

    def __term(self, t: Tree):
        print("TERM >>>", t)
        for child in t.children:
            if child.data == "factor":
                print("TERM-FACTOR:", child.data)
                self.__factor(child)
            elif child.data == "factor_operation":
                print("TERM-FACTOR-OP:", child.data)
                self.__factor_operation(child)

    def __term_operation(self, t: Tree):
        print("TERM-OP >>>", t)
        print("TERM-OP-AEX >>>", t.children[0])
        print("TERM-OP-OP >>>", t.children[1])
        print("TERM-OP-TERM >>>", t.children[2])
        term1 = self.aexpr(t.children[0])
        op = t.children[1]
        term2 = t.children[2]
        if t.children[1] == "+":
            return term1 + term2
        elif t.children[1] == "-":
            return term1 + term2

            i
    def __print_screen(self, t: Tree):
        print("PRINT_SCREEN >>>", t.data)

    # print de debug da arvore
    def __p_debug(self, tree: Tree):
        print("DATA >>> ", tree.data)
        print("TREE >>> ", tree)
        print("CHILD >> ", tree.children)

