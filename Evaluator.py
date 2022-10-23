from packages.ErrorManager import SimpleError
from os import system

class Object:
    def __init__(self, type_, raw, value) -> None:
        self.type = type_
        self.raw = raw
        self.value = value

class Boolean(Object):
    def __init__(self, value) -> None: super().__init__("BOOLEAN", "True" if value == "true" else "False", value)

class Decimal(Object):
    def __init__(self, value) -> None: super().__init__("DECIMAL", str(value), value)

class Empty(Object):
    def __init__(self) -> None: super().__init__("EMPTY", "empty", "empty")

class Integer(Object):
    def __init__(self, value) -> None: super().__init__("INTEGER", str(value), value)

class String(Object):
    def __init__(self, value) -> None:
        v = value[1:-1] if value.startswith('"') else value
        super().__init__("STRING", value, v)

class Evaluator:
    def __init__(self, ast) -> None:
        self.ast = ast
        
        self.operators = ['+', "-", "*", "/"]

        self.functions  = [] 
        self.variables = []
        self.build(ast)
    
    def build(self, data):
        if isinstance(data, list):
            for node in data: self.execute(node)
        elif isinstance(data, dict): self.execute(data)
    
    def execute(self, loc):
        if loc["module"] == "funct": self.function(loc["name"], loc["content"], loc["args"])
        elif loc["module"] == "if": self.if_(loc["condition"], loc["content"], loc["elif"], loc["else"])
        elif loc["module"] == "while": self.while_(loc["condition"], loc["content"])
        elif loc["module"] == "var": self.variable(loc["name"], self.objectify(loc["content"]))
        elif loc["module"] == "execute": self.execut(loc["content"])
        elif loc["module"] == "write": self.write(self.objectify(loc["content"]))
        elif loc["module"] == "call": self.call(loc["content"], loc["args"])
    
    def objectify(self, loc):
        if isinstance(loc, list):
            ob = [self.objectify(o) if o["type"] != "OPERATOR" else o for o in loc]
            for op in ob:
                print(op)
                if op.get("type") == "OPERATOR":
                    return self.condition(ob)
            return ob if len(ob) > 1 else ob[0]
        elif loc["type"] == "BOOLEAN": return Boolean(loc["content"])
        elif loc["type"] == "DECIMAL": return Decimal(loc["content"])
        elif loc["type"] == "EMPTY": return Empty()
        elif loc["type"] == "INTEGER": return Integer(loc["content"])
        elif loc["type"] == "STRING": return String(loc["content"])
        elif loc["type"] == "IDENTIFIER": return self.getVariable(loc["content"])["content"]
    
    def function(self, name, content, args):
        for funct in self.functions:
            if funct["name"] == name: return funct["content"] == content
        self.functions.append({"name": name, "content": content, "args": args})
    
    def if_(self, condition, content, elif_, else_):
        if eval(self.condition(condition)): return self.build(content)
        for c in elif_:
            if eval(self.condition(c["condition"])): return self.build(c["content"])
        return self.build(else_)

    def while_(self, condition, content):
        while eval(self.condition(condition)):
            self.build(content)
    
    def condition(self, condition):
        return ' '.join([(self.objectify(c).raw if c["type"] != "OPERATOR" else c["content"])if not isinstance(c, Object) else c.raw for c in condition]).replace('~', '=')
    
    def variable(self, name, content):
        for var in self.variables:
            if var["name"] == name: 
                var["content"] = content
                return
        self.variables.append({"name": name, "content": content})
    
    def isVariable(self, name):
        for var in self.variables:
            if var["name"] == name: return True
        return False

    def getVariable(self, name):
        for var in self.variables:
            if var["name"] == name: return var
        SimpleError("VariableError", f"{name} isn't a variable")
    
    def execut(self, content):
        comm = [(self.objectify(c).value if isinstance(self.objectify(c), Object) else self.objectify(c)) if c["content"] not in ["echo"] else c["content"] for c in content]
        system(' '.join(comm))
    
    def write(self, ob): 
        if isinstance(ob, Object):
            print(ob.value)
            return 
        
        for o in ob: print(o.value)
    
    def call(self, name, args): 
        for funct in self.functions:
            if name == funct["name"]:
                if len(args) == len(funct["args"]):
                    return self.build(self.replaceArgs(funct, args))
                elif len(args) > len(funct["args"]): SimpleError("ArgumentError", f"{name}() has been given {len(args) - len(funct['args'])} extra positional argument{'s' if len(args) - len(funct['args']) > 1 else ''}")
                SimpleError("ArgumentError", f"{name}() is missing {len(funct['args']) - len(args)} positional argument{'s' if len(args) - len(funct['args']) > 1 else ''}")
        SimpleError("FunctionError", f"{name}() doesn't exist")
    
    def replaceArgs(self, f, args):
        val = f
        if args != []:
            for c in val["content"]:
                for idx, data in enumerate(args):
                    f_args = val["args"][idx]
                    c["content"] = [data if f_args == dat else dat for dat in c["content"]]
        return val["content"]