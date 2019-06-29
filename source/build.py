import argparse, os, sys
from models.DMHParser import DMHParser
from models.DMHEvaluateTree import DMHEvaluateTree

_TESTING_FILES_PATH: str = os.path.dirname(os.path.abspath(__file__)) + "/../testes/"

def main():
    parser: DMHParser = DMHParser()
    valueteTreeContext: DMHEvaluateTree = DMHEvaluateTree()
    
    argparse_cli = argparse.ArgumentParser()
    argparse_cli.add_argument("--file", help="input file")
    args = argparse_cli.parse_args()

    if (args.file != None):
        try:
            if (args.file.split('.')[1] != "dmh"):
                raise IOError("[Error] The file extension should be .dmh")

            with open(_TESTING_FILES_PATH + args.file, "r") as file:
                inputExprFile = file.read()

                if (len(inputExprFile.strip()) == 0):
                    return

                tree = parser.parseTree(inputExprFile)
                valueteTreeContext.tree = tree
                print("Execution output:\n")
                valueteTreeContext.evaluate()

        except FileNotFoundError as err:
            print(err)
        except IOError as err:
            print(err)
        else:
            sys.exit("\nFinished program execution.")
    else:
        terminalUserInput(parser, valueteTreeContext)

    return 0

def terminalUserInput(parser: DMHParser, valueteTreeContext: DMHEvaluateTree):
    print("\nTerminal interaction. Insert ':q' to exit")
    
    while True:
        try:
            inputExpr = input('>>> ').strip()
            if (inputExpr == ":q"):
                break
            
            tree = parser.parseTree(inputExpr)
            #print("Parse Tree:\n {0}".format(tree.pretty()))
            valueteTreeContext.tree = tree
            valueteTreeContext.evaluate()
        except EOFError:
            print("Invalid Data Input\n")
        except Exception as err:
            print("{0}\n".format(err))


if __name__ == '__main__':
    main()
