from os import listdir, getcwd
from sys import argv
from packages.Lexer import Lexer
from packages.Parser import Parser
from packages.Evaluator import Evaluator
from packages.ErrorManager import SimpleError

class LanguageManager:
    def __init__(self, filename, path):
        file   = open(filename, 'r').read()
        tokens = Lexer(file).tokens
        ast    = Parser(tokens).ast
        Evaluator(ast, path)

if __name__ == '__main__':
    if len(argv) == 1: SimpleError("FileError", "file wasn't given.")
    
    arg = argv[1].replace('\\', '/')
    if arg.rsplit('.', 1)[1] not in ['oi', 'ois', 'ose']: SimpleError("FileError", "incorrect file type used.")
    
    path = f"{getcwd()}/{arg.removeprefix('/')}".replace('/', '\\') if not arg.lower().startswith('c:/') else arg.replace('/', '\\')
    try: dirList = listdir(path.rsplit('\\', 1)[0])
    except FileNotFoundError:
        p = path.rsplit('\\', 1)[0]
        SimpleError("FileError", f"no such file or directory")
        
    if not path.rsplit('\\', 1)[1] in dirList: SimpleError("FileError", "file given doesn't exist.")

    try: lm = LanguageManager(argv[1], path.rsplit('\\', 1)[0] + '\\')
    except KeyboardInterrupt: SimpleError("UnexpectedError", "error wasn't expected")
