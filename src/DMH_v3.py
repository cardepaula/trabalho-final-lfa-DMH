# -*- coding: utf-8 -*-

'''
    Classe responsável por realizar o parser tree(AST) e evaluation tree da expressão/código 
    passada como entrada seguindo as regras definidas pela gramática da linguagem DMH 
'''

import sys, math
from lark import Lark, Tree, Transformer, v_args

_DMHGRAMMAR: str = """
    start: expr ";"

    expr: assignment
        | ifexpr
        | whileexpr
        | block
        | orexpr
        | funct

    ifexpr: "if" expr "do" expr ["else" "do" expr] -> if_expr

    whileexpr: "while" expr "do" expr -> while_expr

    block: "{" start* "}"

    assignment: "var" NAME "=" aexpr -> assign_var
              | NAME "=" aexpr -> reassign_var
    
    funct: "defun" NAME "(" [params] ")" block -> def_function

    params: NAME ("," NAME)*

    functcall: NAME "(" [arglist] ")"

    arglist: expr ("," expr)*

    orexpr: andexpr ("||" andexpr)* -> or_expr

    andexpr: comp ("&&" comp)* -> and_expr

    comp: aexpr
        | aexpr OP_COMP aexpr -> comp_operation

    aexpr: term
         | aexpr OP_TERM term -> term_operation

    term: factor
        | term OP_FACTOR factor -> factor_operation

    factor: trig
          | trig "^" factor -> pow

    trig: base
        | TRIG base -> trig_operation

    base: OP_LEFT base -> left_operation
        | NUMBER -> number
        | NAME -> get_var
        | functcall -> call_function
        | "(" expr ")"

    OP_TERM: "+" | "-"
    OP_FACTOR: "*" | "/" | "//" | "%"
    OP_LEFT: "+" | "-"
    OP_COMP: "==" | "!=" | ">" | ">=" | "<" | "<="
    TRIG: "sen" | "cos" | "tang" | "arcsen" | "arccos" | "arctang"

    %import common.CNAME -> NAME
    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

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
        '''Faz o parse da árvore da expressão de entrada'''

        if inputExpr != None: self._inputExpr = inputExpr
        self._tree = self._parser.parse(self._inputExpr)

        return self._tree

    def calcResult(self, inputExpr: str = None) -> float:
        '''Faz o cálculo da expressão de entrada e retorna o valor da árvore de avaliação'''

        if inputExpr != None: self._inputExpr = inputExpr

        return None

class EvaluateTree():
    '''Classe que herda do Transformer responsável por visitar cada nó da árvore e 
       executando o método de acordo com o nome da regra definida na gramática'''

    def __init__(self):
        self.vars = {}
        self.vars_new = {}

    def teste(self, *args):
        return "Testing"

    # Métodos relativos a operações lógicas e matemáticas #
    from operator import add, sub, mul, truediv as div, floordiv, mod, pos, neg, pow, eq, ne, lt, le, gt, ge

    # Método de conversão para um float #
    def number(self, value):
        return float(value)

    # Métodos para o handler de variáveis (assinatura, reassinatura e recuperação) #
    def assign_var(self, name, value):
        if (name not in self.vars_new):
            self.vars_new[name] = value
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
        
# TESTANDO O CÓDIGO #
def main():
    parser: DMHParser = DMHParser()

    while True:
        try:
            expr = input('>>> ').strip()
            if (expr == ":q"):
                break
            
            tree: Tree = parser.parseTree(expr)
            print("Parse Tree:\n {0}".format(tree.pretty()))
            
            #for i in tree.iter_subtrees():
            #    print(i)
            
            #result: object = parser.calcResult(expr)
            #print("{0}\n".format(result))
            #print("Resultado: {0}\n".format(result))
        except EOFError:
            print("Invalid Data Input")
        except Exception as err:
            print("{0}\n".format(err))


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