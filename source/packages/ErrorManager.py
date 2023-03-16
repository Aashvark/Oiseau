from sys import exit

class Error:
    def FileNotProvidedError():
        print(f"FileNotProvidedError: a file was not provided.")
        exit()

    def IncorrectFileTypeError(type):
        print(f"IncorrectFileTypeError: '{type}' could not be used as a oiseau file type.")
        exit()
    
    def FileNotFoundError(file):
        print(f"FileNotFoundError: '{file}' could not be found.")
        exit()
    
    def UnexpectedError():
        print(f"UnexpectedError: error wasn't expected")
        exit()

    def UnknownError(character):
        print(f"UnknownError: '{character}' could not be identified.")
        exit()
    
    def NotStartedError(type):
        print(f"NotStartedError: the '{type}' was not started.")
        exit()

    def UnexpectedStartError(type):
        print(f"UnexpectedStartError: the '{type}' was unexpectedly / randomly started.")
        exit()
    
    def StatementEndedEarlyError(funct):
        print(f"StatementEndedEarlyError: {'the ' + funct + ' statement' if ')' not in funct else funct} was ended too early.")
        exit()
    
    def StatementNotEndedError(funct):
        print(f"StatementNotEndedError: {'the ' + funct + ' statement' if ')' not in funct else funct} was not ended.")
        exit()
    
    def UnsupportedTypeError(funct, type, pos):
        print(f"UnsupportedTypeError: {'the ' + funct + ' statement' if ')' not in funct else funct} doesn't support the type '{type}' as a {pos}")
        exit()
    
    def NotCompletedError(funct, type):
        print(f"NotCompletedError: {'the ' + funct + ' statement' if ')' not in funct else funct} wasn't completed; missing '{type}'")
        exit()

    def NotUsedError(funct, type):
        print(f"NotUsedError: '{type}' wasn't used in {'the' + funct + 'statement' if ')' not in funct else funct}")
        exit()

    def ArgumentError(name, str):
        print(f"ArgumentError: {name} has been given {len(str)} positional argument{'s' if len(str) != 1 else ''}")
        exit()

    def ArgumentAssignmentError():
        print(f"ArgumentAssignmentError: you cannot reassign an argument")
        exit()
    
    def AssignmentError(name, value):
        print(f"AssignmentError: Cannot set variable '{name}' to '{value}'")
        exit()
    
    def DoesNotHaveFunctionError(type, fun):
        print(f"DoesNotHaveFunctionError: '{type}' does not have the function {fun}")
        exit()

    def FunctionNotFoundError(name):
        print(f"FunctionNotFoundError: function '{name}' could not be accessed")
        exit()

    def VariableNotFoundError(name):
        print(f"VariableNotFoundError: variable '{name}' could not be accessed")
        exit()