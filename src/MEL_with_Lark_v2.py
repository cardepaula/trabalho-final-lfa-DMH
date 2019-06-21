#
# This example shows how to write a basic calculator with variables.
#

from lark import Lark, Transformer, v_args
import sys
import math

# Constante do módulo definindo a gramática a ser utilizada utilizando a sintaxe Lark + EBNF
_MELGRAMMAR: str = """
    ?start: expr ";"

    ?expr: assignment
          | ifexpr
          | whileexpr
          | block
          | orexpr


    ?ifexpr: "if" expr ":" expr ["else" expr] -> ifexpr

    ?whileexpr: "while" expr ":" expr -> whileexpr

    ?block: "{" start* "}"

    ?assignment: "var" VARNAME "=" aexpr -> assign_var
               | VARNAME "=" aexpr -> reassign_var

    ?orexpr: andexpr ("||" andexpr)* -> orexpr

    ?andexpr: conj ("&&" conj)* -> andexpr

    ?conj: aexpr
        | aexpr "==" aexpr -> igualdade
        | aexpr "!=" aexpr -> diferenca
        | aexpr ">" aexpr -> maior_q
        | aexpr ">=" aexpr -> maior_igual_q
        | aexpr "<" aexpr -> menor_q
        | aexpr "<=" aexpr -> menor_iqual_q

    ?aexpr: term
          | aexpr "+" term -> add
          | aexpr "-" term -> sub

    ?term: factor
         | term "*" factor -> mul
         | term "/" factor -> div
         | term "//" factor -> floordiv
         | term "%" factor -> mod

    ?factor: trig
           | trig "^" factor -> pow

    ?trig: base
            | "sen" base ->  sen
            | "cos" base ->  cos
            | "tang" base ->  tang
            | "arcsen" base ->  arcsen
            | "arccos" base ->  arccos
            | "arctang" base ->  arctang

    ?base: "-" base -> neg
         | NUMBER -> number
         | VARNAME -> getvar
         | "(" expr ")"

    %import common.CNAME -> VARNAME
    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

class DMHParser:
    def __init__(self):
        self._inputExpr: str = ""
        self._parser: Lark = Lark(_MELGRAMMAR, parser='lalr', start='start') #, transformer=CalculateTree())

    @property
    def expression(self) -> str:
        return self._inputExpr

    def checkExpression(self, inputExpr: str) -> bool:
        '''Checa se a expressão de entrada é válida de acordo com a gramática MEL definida'''
        
        self._inputExpr = inputExpr

        # Usa a instancia do parser e cria a sua árvore parser de execução
        isValidExpr: bool = True
        try:
            self._parser.parse(inputExpr)
        except Exception:
            isValidExpr = False
        finally:
            return isValidExpr

    def calcResult(self, inputExpr: str) -> float:
        '''Faz o cálculo da expressão e retorna o valor'''

        self._inputExpr = inputExpr
        return self._parser.parse(inputExpr)


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, floordiv, mod, neg, pow
    # from math import sin, cos, tan, asin, acos, atan, radians
    number = float

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def reassign_var(self, name, value):
        if (name in self.vars):
            self.vars[name] = value
            return value
        else:
            return "Variable '{0}' is not defined".format(name)

    def getvar(self, name):
        return self.vars[name]

    def sen(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.sin(radian),10)

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

    def igualdade(self, value1, value2):
        if (value1 == value2):
            return True
        else:
            return False
    
    def diferenca(self, value1, value2):
        if (value1 != value2):
            return True
        else:
            return False
    
    def maior_q(self, value1, value2):
        if (value1 > value2):
            return True
        else:
            return False

    def maior_igual_q(self, value1, value2):
        if (value1 >= value2):
            return True
        else:
            return False
    
    def menor_q(self, value1, value2):
        if (value1 < value2):
            return True
        else:
            return False

    def menor_iqual_q(self, value1, value2):
        if (value1 <= value2):
            return True
        else:
            return False

    def orexpr(self, value1, value2):
        pass

    def andexpr(self, value1, value2):
        pass

    def whileexpr(self, value1, value2):
        pass

    def ifexpr(self, value1, value2):
        pass
        
# TESTANDO O CÓDIGO #
def main():
    parser: DMHParser = DMHParser()

    # print(parser.parse(text).pretty())

    while True:
        try:
            expr = input('> ')
            if (expr == ":q"):
                break

            print(parser.calcResult(expr))
            print(parser.calcResult(expr).pretty())
        except EOFError:
            print("Invalid Data Input")
        except Exception as err:
            #print("Error: {0}".format(err))
            print("Error:", err)


def test():
    parser: DMHParser = DMHParser()
    expressions: list = ["2 + 2;",
                         "3 * 23;",
                         "3 - 2 * 7;",
                         "2 // 20;",
                         "+2 - 4.0 / ----1.;",
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
        print("Expression: {0} = {1}".format(expr, parser.calcResult(expr)))

# Para testes unitários
if __name__ == '__main__':
    #test()
    main()