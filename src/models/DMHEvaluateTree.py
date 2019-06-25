# -*- coding: utf-8 -*-

'''
    Classe responsável por realizar o evaluation da árvore (AST) da expressão/código 
    passada como entrada seguindo as regras definidas pela gramática da linguagem DMH
'''

import sys, os, math

class DMHEvaluateTree:
    def __init__(self):
        self.vars = {}
        self.functs = {}

    def teste(self, *args):
        return "Testing"

    # Métodos relativos a operações lógicas e matemáticas #
    from operator import add, sub, mul, truediv as div, floordiv, mod, pos, neg, pow, eq, ne, lt, le, gt, ge

    # Método de conversão para um float #
    def number(self, value):
        return float(value)

    # Métodos para o handler de variáveis (assinatura, reassinatura e recuperação) #
    def assign_var(self, name, value):
        if (name not in self.vars):
            self.vars[name] = value
            return value
        
        raise Exception("Error: Variable '{0}' is already defined".format(name))

    def reassign_var(self, name, value):
        if (name in self.vars):
            self.vars[name] = value
            return value
        
        raise Exception("Error: Variable '{0}' is not defined".format(name))

    def get_var(self, name):
        if (name in self.vars):
            return self.vars[name]
        
        raise Exception("Error: Variable {0} does not exist".format(name))

    # Métodos lida com operações trigonométricas recebendo valor em graus #
    def sen(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.sin(radian), 10)

    def cos(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.cos(radian), 10)

    def tang(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.tan(radian), 10)

    def arcsen(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.asin(radian), 10)

    def arccos(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.acos(radian), 10)

    def arctang(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.atan(radian), 10)

    # Métodos que lida com operações lógicas AND e OR #
    def or_expr(self, value, *values):
        if (len(values) == 0):
            return value

    def and_expr(self, value, *values):
        if (len(values) == 0):
            return value

    # Métodos que lida com estruturas de condição(if) e repetição(while)
    def if_expr(self, valExpr1, valExpr2, valExpr3 = None):
        if (valExpr1):
            return valExpr2
        else:
            return valExpr3
        print("xD")

    def while_expr(self, valExpr1, valExpr2):
        print("xD")
