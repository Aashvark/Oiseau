from os import listdir, getcwd, system
from sys import argv
from packages.Lexer import Lexer
from packages.Parser import Parser
from packages.Evaluator import Evaluator
from packages.ErrorManager import Error

class LanguageManager:
    def __init__(self, filename, path, args):
        file   = open(filename, 'r').read()
        tokens = Lexer(file).tokens
        ast    = Parser(tokens, path).ast
        Evaluator(ast, path, args)

if __name__ == '__main__':
    if len(argv) == 1: Error.FileNotProvidedError()
    
    arg = argv[1].replace('\\', '/')
    if arg.rsplit('.', 1)[-1] not in ['oi', 'ois', 'ose']: Error.IncorrectFileTypeError(arg.rsplit('.', 1)[-1])
    
    path = f"{getcwd()}/{arg.removeprefix('/')}".replace('/', '\\') if not arg.lower().startswith('c:/') else arg.replace('/', '\\')
    try: dirList = listdir(path.rsplit('\\', 1)[0])
    except FileNotFoundError: Error.FileNotFoundError(path.rsplit('\\', 1)[-1])
        
    if not path.rsplit('\\', 1)[-1] in dirList: Error.FileNotFoundError(path.rsplit('\\', 1)[-1])

    try: LanguageManager(argv[1], path.rsplit('\\', 1)[0] + '\\', argv[1:])
    except KeyboardInterrupt: Error.UnexpectedError()
