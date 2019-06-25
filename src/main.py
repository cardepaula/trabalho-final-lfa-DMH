import argparse
from models.DMHParser import DMHParser
from models.DMHEvaluateTree import DMHEvaluateTree

def main():
    parser: DMHParser = DMHParser()

    while True:
        try:
            expr = input('>>> ').strip()
            if (expr == ":q"):
                break
            
            tree = parser.parseTree(expr)
            print("Parse Tree:\n {0}".format(tree.pretty()))
            # DEPOIS DE CONSTRUIR A ÁRVORE CHAMA O EVALUATE TREE PARA PEGAR OS VALORES
        except EOFError:
            print("Invalid Data Input")
        except Exception as err:
            print("{0}\n".format(err))

    
    return 0


if __name__ == '__main__':
    main()


# parser = argparse.ArgumentParser()
#     parser.add_argument("--file", help="input file")
#     args = parser.parse_args() 
    
#     if args.file:
#       file = open(args.file, 'r')
#       for line in file:
#         paintCode.parser(line.strip())
#       input('\nPress any key to exit\n')
#     else:
#       rpl()