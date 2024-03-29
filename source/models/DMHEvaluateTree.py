# -*- coding: utf-8 -*-

'''
    Classe responsável por realizar o evaluation da árvore (AST) da expressão/código 
    passada como entrada seguindo as regras definidas pela gramática da linguagem DMH
'''

import math
from lark import Tree, Token

class DMHEvaluateTree:
    def __init__(self, tree: Tree = None):
        self._vars: dict = {}
        self._functs: dict = {}
        self._tree: Tree = tree

    @property
    def tree(self) -> Tree:
        return self._tree

    @tree.setter
    def tree(self, value: Tree) -> None:
        self._tree = value

    def evaluate(self) -> None:
        '''Realiza o evaluate tree da parse da árvore do objeto EvaluateTree criado'''
        self.__start(self._tree)

    # Início da gramática #

    # expr ";" (expr ";")*
    def __start(self, t: Tree) -> None:
        for child in t.children:
            self.__expr(child)

    # Seleção das expressões definidas na gramática #
 
    # assignment | ifexpr | whileexpr | funct | aexpr | print
    def __expr(self, t: Tree) -> object:
        first_child: Tree = t.children[0]

        if first_child.data == 'assign_var':
            self.__assign_var(first_child)
        elif first_child.data == 'reassign_var':
            self.__reassign_var(first_child)
        elif first_child.data == 'if_expr':
            return self.__if_expr(first_child)
        elif first_child.data == 'while_expr':
            return self.__while_expr(first_child)
        elif first_child.data == 'def_function':
            return self.__def_function(first_child)
        elif first_child.data == 'block':
            return self.__block(first_child)
        elif first_child.data == 'aexpr':
            return self.__aexpr(first_child)
        elif first_child.data == 'print_screen':
            return self.__print_screen(first_child)
        else:
            raise Exception("It's not a valid expression.")

    # Assinatura, reassinatura e recuperação de variável #

    # "var" NAME "=" aexpr
    def __assign_var(self, t: Tree) -> None:
        name: str = t.children[0].value
        aexpr: Tree = t.children[1]
        self._vars[name] = self.__aexpr(aexpr)

    # NAME "=" aexpr
    def __reassign_var(self, t: Tree) -> None:
        name: str = t.children[0].value
        aexpr: Tree = t.children[1]

        if (name not in self._vars):
            raise Exception("Error: Variable '{0}' is not defined".format(name))

        self._vars[name] = self.__aexpr(aexpr)

    # NAME == ('_'|'a'..'z'|'A'..'Z') ('_'|'a'..'z'|'A'..'Z'|0..9)*
    def __get_var(self, t: Tree) -> float:
        name: float = t.children[0].value

        if (name in self._vars):
            return self._vars[name]
        
        raise Exception("Error: Variable {0} does not exist".format(name))

    # Estruturas de seleção(if) e repetição(while) #

    # "if" comp "do" block ["else" "do" block]
    def __if_expr(self, t: Tree) -> None:
        op_comp: bool = self.__comp_operation(t.children[0])

        if (op_comp):
            self.__block(t.children[1])
        elif len(t.children) == 3:
            self.__block(t.children[2])

    # "while" comp "do" block
    def __while_expr(self, t: Tree) -> None:
        while (self.__comp_operation(t.children[0])):
            self.__block(t.children[1])

    # aexpr OP_COMP aexpr
    def __comp_operation(self, t: Tree) -> bool:
        aexpr_letf: float = self.__aexpr(t.children[0])
        op_comp: str = t.children[1].value
        aexpr_right: float = self.__aexpr(t.children[2])

        if op_comp == "==":
            return aexpr_letf == aexpr_right
        elif op_comp == "!=":
            return aexpr_letf != aexpr_right
        elif op_comp == ">=":
            return aexpr_letf >= aexpr_right
        elif op_comp == "<=":
            return aexpr_letf <= aexpr_right
        elif op_comp == ">":
            return aexpr_letf > aexpr_right
        elif op_comp == "<":
            return aexpr_letf < aexpr_right

    # Definições e chamadas de funções #

    # "defun" NAME "(" ")" "do" functblock
    def __def_function(self, t: Tree) -> None:
        funct_name: str = t.children[0].value

        if (funct_name in self._functs):
            raise Exception("Error: Function '{0}' is already defined".format(funct_name))

        self._functs[funct_name] = t.children[1]

    # NAME "(" ")"
    def __functcall(self, t: Tree) -> float:
        funct_name: Token = t.children[0].value

        if (funct_name not in self._functs):
            raise Exception("Error: Function '{0}' is not defined".format(funct_name))

        funct_block: Tree = self._functs[funct_name]
        return self.__functblock(funct_block)

    # "{" start* functreturn "}"
    def __functblock(self, t: Tree) -> float:
        for child in t.children:
            if (child.data == "start"):
                self.__start(child)
            elif (child.data == "functreturn"):
                return self.__functreturn(child)

    # "returns" aexpr ";"
    def __functreturn(self, t: Tree) -> float:
        aexpr: float = self.__aexpr(t.children[0])
        return aexpr

    # Definição de blocos de escopo do código #
    # "{" start "}"
    def __block(self, t: Tree) -> object:
        first_child: Tree = t.children[0]
        return self.__start(first_child)

    # Printar informações na tela
    # "show" "(" aexpr ")"
    def __print_screen(self, t: Tree) -> None:
        aexpr: float = self.__aexpr(t.children[0])
        print(aexpr)

    # Lidar com números e cálculos matemáticos em geral #

    # term | aexpr ('+' | '-') term
    def __aexpr(self, t: Tree) -> float:
        first_child: Tree = t.children[0]

        if (first_child.data == "term" and len(t.children) == 1):
            return self.__term(first_child)
        elif (first_child.data == "aexpr" and len(t.children) == 3):
            return self.__term_operation(t)
        else:
            raise Exception("Invalid math expression.")

    # factor | term (* | / | // | %) factor
    def __term(self, t: Tree) -> float:
        first_child: Tree = t.children[0]

        if (first_child.data == "factor" and len(t.children) == 1):
            return self.__factor(first_child)
        elif (first_child.data == "term" and len(t.children) == 3):
            return self.__factor_operation(t)
        else:
            raise Exception("Invalid math expression.")

    # aexpr (+ | -) term
    def __term_operation(self, t: Tree) -> float:
        aexpr: float = self.__aexpr(t.children[0])
        op_term: str = t.children[1].value
        term: float = self.__term(t.children[2])

        if op_term == '+':
            return aexpr + term
        elif op_term == '-':
            return aexpr - term
        else:
            raise Exception("Invalid term operator. Expect (+ or -) given {0}".format(op_term))

    # trig | factor ^ trig
    def __factor(self, t: Tree) -> float:
        first_child: Tree = t.children[0]

        if first_child.data == "trig" and len(t.children) == 1:
            return self.__trig(first_child)
        elif first_child.data == "factor" and len(t.children) == 3:
            return self.__pow_operation(t)
        else:
            raise Exception("Invalid math expression.")

    # term (* | / | // | %) factor
    def __factor_operation(self, t: Tree):
        term: float = self.__term(t.children[0])
        op_factor: str = t.children[1].value
        factor: float = self.__factor(t.children[2])

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

    # factor ^ trig
    def __pow_operation(self, t: Tree) -> float:
        factor: float = self.__factor(t.children[0])
        op_pow: str = t.children[1].value
        trig: float = self.__trig(t.children[2])

        if (op_pow != '^'):
            raise Exception("Invalid pow operator. Expect (^) given {0}".format(op_pow))

        return factor ** trig

    # ('sen' | 'cos' | 'tang' | 'arcsen' | 'arccos' | 'arctang') base
    def __trig(self, t: Tree) -> float:
        first_child: Tree = t.children[0]

        if (isinstance(first_child, Token) and first_child.type == 'TRIG'):
            return self.__trig_operation(t)
        elif (first_child.data == 'base' and len(t.children) == 1):
            return self.__base(first_child)
        else:
            raise Exception("Invalid math expression")
    
    # ('sen' | 'cos' | 'tang' | 'arcsen' | 'arccos' | 'arctang') base
    def __trig_operation(self, t: Tree) -> float:
        op_trig: str = t.children[0].value
        base: float = self.__base(t.children[1])

        if op_trig == 'sen':
            return DMHEvaluateTree.__sen(base)
        elif op_trig == 'cos':
            return DMHEvaluateTree.__cos(base)
        elif op_trig == 'tang':
            return DMHEvaluateTree.__tang(base)
        elif op_trig == 'arcsen':
            return DMHEvaluateTree.__arcsen(base)
        elif op_trig == 'arccos':
            return DMHEvaluateTree.__arccos(base)
        elif op_trig == 'arctang':
            return DMHEvaluateTree.__arctang(base)
        else:
            raise Exception('''Invalid trigonometric operator. 
                            Expect (sen, cos, tang, arcsen, arccos or arctang) given {0}'''.format(op_trig))

    @staticmethod
    def __sen(deg_value: float) -> float:
        radian = math.radians(deg_value)
        return round(math.sin(radian), 10)

    @staticmethod
    def __cos(deg_value: float) -> float:
        radian = math.radians(deg_value)
        return round(math.cos(radian), 10)

    @staticmethod
    def __tang(deg_value: float) -> float:
        radian = math.radians(deg_value)
        return round(math.tan(radian), 10)

    @staticmethod
    def __arcsen(deg_value: float) -> float:
        radian = math.radians(deg_value)
        return round(math.asin(radian), 10)

    @staticmethod
    def __arccos(deg_value: float) -> float:
        radian = math.radians(deg_value)
        return round(math.acos(radian), 10)

    @staticmethod
    def __arctang(deg_value: float) -> float:
        radian = math.radians(deg_value)
        return round(math.atan(radian), 10)

    # Operações básicas da linguagem
    def __base(self, t: Tree) -> float:
        first_child: Tree = t.children[0]

        if (isinstance(first_child, Token) and first_child.type == 'TRIG'):
            return self.__trig_operation(t)
        elif first_child.data == 'leftoperation':
            return self.__left_operation(first_child)
        elif first_child.data == 'number':
            return self.__number(first_child)
        elif first_child.data == 'getvar':
            return self.__get_var(first_child)
        elif first_child.data == 'functcall':
            return self.__functcall(first_child)
        elif first_child.data == 'aexpr':
            return self.__aexpr(first_child)

    # (+ | -) <base>
    def __left_operation(self, t: Tree) -> float:
        op_left: str = t.children[0].value
        base: float = self.__base(t.children[1])

        if (op_left == '-'):
            return -1 * base
        return base

    # <number>
    @staticmethod
    def __number(t: Tree) -> float:
        token: Token = t.children[0]
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
                         "sen(63) * 12 - 321 // 213;",
                         "-sen(60);",
                         "var x = 9;"]

    for expr in expressions:
        tree = parser.parseTree(expr)
        valueteTree.tree = tree
        valueteTree.evaluate()
        #print("Expression: {0} = {1}".format(expr, aux))


if __name__ == '__main__':
    testExpressions()
