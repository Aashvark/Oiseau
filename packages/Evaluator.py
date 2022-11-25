import decimal
import os
from packages.ErrorManager import SimpleError
from decimal import Decimal as dec
from decimal import getcontext, ROUND_UP, DivisionByZero
from time import sleep
from os import system

getcontext().rounding = ROUND_UP
getcontext().prec = 16
getcontext().traps[DivisionByZero] = False

class builtin():
    def __init__(self, path) -> None:
        self.path = path
    
    def read(self, file):
        return String(open(self.path + file[0].value, 'r').read())
    
    def input(self, str):
        return String(input(str[0].value))

class Object:
    def __init__(self, type_, raw, value) -> None:
        self.type = type_
        self.raw = raw
        self.value = value

class Boolean(Object):
    def __init__(self, value) -> None: super().__init__("BOOLEAN", "True" if value == "true" else "False", value)

class Decimal(Object):
    def __init__(self, value) -> None: super().__init__("DECIMAL", f"decimal.Decimal(str({value}))", float(value))

class Empty(Object):
    def __init__(self) -> None: super().__init__("EMPTY", "empty", "empty")

class Integer(Object):
    def __init__(self, value) -> None: super().__init__("INTEGER", f"decimal.Decimal({value})" if str(value) not in "-infinity" else value, int(value) if str(value) not in "-infinity" else value)

class Storage(Object):
    def __init__(self, value) -> None: super().__init__("STORAGE", "", value)  

class String(Object):
    def __init__(self, value) -> None:
        v = value.replace('\\\\', '\\').replace('\\\"', '\"').replace('\\n', '\n').replace('\\t', '\t').replace("\\s", " ")
        super().__init__("STRING", v, v[1:-1] if value.startswith('"') else v)
    
    def upper(self, args): return self.value.upper()

class Function(Object):
    def __init__(self, name, v, args, loc) -> None:
        super().__init__("FUNCTION", "", v)
        self.name = name
        self.args = args
        self.location = loc

class Variable(Object):
    def __init__(self, name, type_, v:Object, isConst) -> None:
        super().__init__(v.type if type_ == "any" else type_, v if v.raw == "" else v.raw, v.value)
        self.name = name
        self.isExplicit = False if type_ == "any" else True
        self.isConst = isConst
    
    def set(self, value, mod): 
        if (not self.isExplicit or self.type == value.type) and not self.isConst: return self.modify(value, mod)
        SimpleError("VariableError", f"Cannot set variable '{self.name}' to '{value.value}'")

    def modify(self, value, mod):
        if self.type == "INTEGER":
            v = value.value
            if mod == "+=": self.value += v
            elif mod == "-=": self.value -= v
            elif mod == "*=": self.value *= v
            elif mod == "/=": self.value /= v
            elif mod == "^=": self.value = self.value ** v
            elif mod == "#=": self.value = self.value ** (1/v)
            else: self.value = value
            return
        self.value = value

class Evaluator:
    def __init__(self, ast, path) -> None:
        self.ast = ast
        self.builtin = builtin(path)
        
        self.operators = ['+', "-", "*", "/"]

        self.functions  = [
            Function("read", "", ["file"], "internal"),
            Function("readln", "", ["file"], "internal"),
            Function("input", "", ["str"], "internal")
        ] 
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
        elif loc["module"] == "switch": self.switch(loc["input"], loc["cases"])
        elif loc["module"] == "var": self.variable(loc["name"], self.objectify(loc["content"]), loc["type"], loc["mod"], loc["const"])
        elif loc["module"] == "execute": self.execut(loc["content"])
        elif loc["module"] == "write": self.write(self.objectify(loc["content"]))
        elif loc["module"] == "clear": _ = system('cls' if os.name == 'nt' else 'clear')
        elif loc["module"] == "delay": 
            sleep(self.objectify(loc["content"]).value)
        elif loc["module"] == "call": self.call(loc["content"], loc["args"])
    
    def objectify(self, loc):
        if isinstance(loc, list):
            ob = [self.objectify(o) if o["type"] != "OPERATOR" else o for o in loc]
            for op in ob:
                if isinstance(op, dict) and op.get("type") == "OPERATOR":
                    if [o["content"] for o in loc] == ['0', '/', '0']: return Integer("infinity")
                    return self.objectify(eval(''.join([o.value if isinstance(o, Object) else o for o in self.condition(ob)])))
            return ob if len(ob) > 1 else ob[0]
        elif isinstance(loc, dec):
            if '.' in str(loc): return Decimal(float(loc))
            return Integer(int(loc) if str(loc) not in "-infinity" else loc)
        elif loc["type"] == "BOOLEAN": return Boolean(loc["content"])
        elif loc["type"] == "DECIMAL": return Decimal(float(loc["content"]))
        elif loc["type"] == "EMPTY": return Empty()
        elif loc["type"] == "INTEGER": return Integer(int(loc["content"]) if str(loc["content"]) not in "-infinity" else loc["content"])
        elif loc["type"] == "STORAGE": return Storage(self.objectify(loc["content"]))
        elif loc["type"] == "STRING": return String(loc["content"])
        elif loc["type"] == "IDENTIFIER":
            var = self.getVariable(loc["content"])
            return (var) if not isinstance(var, Function) else var
        elif loc["type"] == "CALL": return self.getFunction(loc["content"], loc["args"])
    
    def function(self, name, content, args):
        for funct in self.functions:
            if funct.name == name: 
                funct.value = content
                return
        self.functions.append(Function(name, content, args, "external"))
    
    def if_(self, condition, content, elif_, else_):
        if eval(self.condition(condition)): return self.build(content)
        for c in elif_:
            if eval(self.condition(c["condition"])): return self.build(c["content"])
        return self.build(else_)

    def while_(self, condition, content):
        while eval(self.condition(condition)):
            self.build(content)
    
    def switch(self, input, cases):
        for case in cases:
            if self.objectify(input).value == self.objectify(case["name"]).value: return self.build(case["content"])
        return
    
    def condition(self, condition):
        if not isinstance(condition, list) or len(condition) <= 1: return self.objectify(condition).raw
        return ' '.join([(((self.objectify(c).raw if c["type"] not in ["COMPARATOR", "OPERATOR"] else c["content"]) if isinstance(c, dict) else self.objectify(c).raw) if not isinstance(c, str) else c) if not isinstance(c, Object) else c.raw for c in condition])
    
    def variable(self, name, content, type_, mod, const):
        for var in self.variables:
            if var.name == name: return var.set(content, mod)
        if type_ != "any" and content.type != type_: SimpleError("VariableError", f"Cannot set variable '{name}' to '{content.value}'")
        self.variables.append(Variable(name, type_, content, const))
    
    def isVariable(self, name):
        for var in self.variables:
            if var.name == name: return True
        return False

    def getVariable(self, name):
        for var in self.variables:
            if var.name == name:
                if var.type == "FUNCTION": return var.value
                return var
        SimpleError("VariableError", f"{name} isn't a variable")
    
    def getFunction(self, name, args):
        for function in self.functions:
            if function.name == name: return self.call(function.name, [self.objectify(arg) for arg in args])
        SimpleError("FunctionError", f"{name} isn't a defined function")
    
    def execut(self, content):
        comm = [(self.objectify(c).value if isinstance(self.objectify(c), Object) else self.objectify(c)) if c["content"] not in ["echo"] else c["content"] for c in content]
        system(' '.join(comm))
    
    def write(self, ob):
        if ob.type == "STORAGE": return print(f"{[o.value for o in ob.value]}".replace('[', '<').replace(']', '>').replace('\'', '\"'))
        elif isinstance(ob, Object): return print(ob.value)
        elif isinstance(ob, float) or isinstance(ob, dec): return print(ob)

        for o in ob: print(o.value)
    
    def call(self, name, args):
        for funct in self.functions:
            if name == funct.name:
                if len(args) == len(funct.args):
                    if funct.location == "internal": return getattr(self.builtin, name)(args)
                    return self.build(self.replaceArgs(funct, args))
                elif len(args) > len(funct.args): SimpleError("ArgumentError", f"{name}() has been given {len(args) - len(funct.args)} extra positional argument{'s' if len(args) - len(funct.args) > 1 else ''}")
                SimpleError("ArgumentError", f"{name}() is missing {len(funct.args) - len(args)} positional argument{'s' if len(args) - len(funct.args) > 1 else ''}")
        SimpleError("FunctionError", f"{name}() doesn't exist")
    
    def replaceArgs(self, f, args):
        val = f
        if args != []:
            for c in val.value:
                for idx, data in enumerate(args):
                    f_args = val.args[idx]
                    c["content"] = [data if f_args == dat else dat for dat in c["content"]]
        return val.value
