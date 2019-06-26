# -*- coding: utf-8 -*-

'''
    Classe responsável por realizar o parser tree(AST) da expressão/código 
    passada como entrada seguindo as regras definidas pela gramática da linguagem DMH 
'''

import sys, os
from lark import Lark, Tree
from DMHEvaluateTree import *

_GRAMMAR_PATH: str = os.path.dirname(os.path.abspath(__file__)) + "/../grammar/"
_GRAMMAR_FILENAME: str = "grammar.lark"
_DMHGRAMMAR: str = ""

try:
    with open(_GRAMMAR_PATH + _GRAMMAR_FILENAME, "r") as file:
        _DMHGRAMMAR = file.read()
except FileNotFoundError as err:
    print(err)
    sys.exit(1)
except IOError as err:
    print(err)
    sys.exit(1)
except Exception as err:
    print(err)
    sys.exit(1)


class DMHParser:
    def __init__(self):
        self._inputExpr: str = ""
        self._tree: Tree = None
        self._parser: Lark = Lark(_DMHGRAMMAR, start='start')

    @property
    def expression(self) -> str:
        return self._inputExpr

    @property
    def tree(self) -> Tree:
        return self._tree

    def checkExpression(self, inputExpr: str) -> bool:
        '''Checa se a expressão de entrada é válida seguindo as regras da gramática da linguagem'''
        
        self._inputExpr = inputExpr

        isValidExpr: bool = True
        try:
            self._parser.parse(inputExpr)
        except Exception:
            isValidExpr = False
        finally:
            return isValidExpr

    def parseTree(self, inputExpr: str = None) -> Tree:
        '''Cria e retorna a árvore(AST) da expressão de entrada'''

        if inputExpr != None: self._inputExpr = inputExpr
        self._tree = self._parser.parse(self._inputExpr)

        return self._tree


################################### TESTANDO A CLASSE DE FORMA UNITÁRIA ###################################
def main():
    parser: DMHParser = DMHParser()
    valueteTree: DMHEvaluateTree = DMHEvaluateTree()

    while True:
        try:
            expr = input('>>> ').strip()
            print(expr)
            if (expr == ":q"):
                break
            
            tree: Tree = parser.parseTree(expr)
            #print("Parse Tree:\n {0}".format(tree.pretty()))
            print("TREE >>> ", tree)
            print("CHILDs >> ", tree.children)
            print("DATA >>> ", tree.data)

            for child in tree.children:
                print("FOR-CHILD >>> ", child)
                valueteTree.start(child)

        except EOFError:
            print("Invalid Data Input")
        except Exception as err:
            print("{0}\n".format(err))


def testExpressions():
    parser: DMHParser = DMHParser()
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
        print("Expression: {0} = {1}".format(expr, parser.checkExpression(expr)))


# Para testes unitários
if __name__ == '__main__':
    #testExpressions()
    main()
