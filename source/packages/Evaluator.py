import math as m
import decimal
from inspect import currentframe
from decimal import Decimal as dec
from decimal import getcontext, ROUND_UP, DivisionByZero
import os
from os import system
from packages.ErrorManager import Error
from time import sleep
from re import match

getcontext().prec = 28
getcontext().rounding = ROUND_UP
getcontext().traps[DivisionByZero] = False

class stlib:
    def __init__(self, path, args) -> None:
        self.name = self.__class__.__name__
        self.path = path
        self.args = Storage([String(arg) for arg in args])
    
    def readf(self, str):
        if (isinstance(str, list) and len(str) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (str.type != "STRING"): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "STRING", "argument")

        try: return String(open(self.path + str.value, 'r').read())
        except FileNotFoundError: Error.FileNotFoundError(str.value)
    
    def writef(self, str):
        if (isinstance(str, list) and len(str) != 2): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif ([str[0].type, str[1].type] != ["STRING", "STRING"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "STRING", "argument")
        
        try:
            with open(self.path + str[0].value, 'w+') as f: f.write(str[1].value)
        except FileNotFoundError: Error.FileNotFoundError(str[0].value)
    
    def createf(self, str):
        if (isinstance(str, list) and len(str) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (str.type != "STRING"): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "STRING", "argument")
        try:
            with open(self.path + str.value, 'x') as f: return
        except FileExistsError: return
    
    def input(self, str):
        if (isinstance(str, list) and len(str) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (str.type != "STRING"): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "STRING", "argument")
        return String(input(str[0].value))

class math:
    def __init__(self, path):
        self.path = path
        self.name = self.__class__.__name__
        self.pi = Decimal(m.pi)
    
    def sqrt(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        sqrt = m.sqrt(num.value)
        if (isinstance(sqrt, int) or sqrt == round(sqrt)): return Integer(sqrt)
        return Decimal(sqrt)
    
    def sind(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.sin(m.radians(num.value)))

    def cosd(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.cos(m.radians(num.value)))

    def tand(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.tan(m.radians(num.value)))
    
    def sinr(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.sin(num.value))

    def cosr(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.cos(num.value))

    def tanr(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.tan(num.value))
    
    def asind(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.asin(m.radians(num.value)))

    def acosd(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.acos(m.radians(num.value)))

    def atand(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.atan(m.radians(num.value)))
    
    def asinr(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.asin(num.value))

    def acosr(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.acos(num.value))

    def atanr(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.atan(num.value))
    
    def degrees(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.degrees(num.value))
    
    def radians(self, num):
        if (isinstance(num, list) and len(num) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        elif (num.type not in ["INTEGER", "DECIMAL"]): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERS and DECIMALS", "argument")
        return Decimal(m.radians(num.value))

class Object:
    def __init__(self, type_, raw, value) -> None:
        self.type = type_
        self.raw = raw
        self.value = value

class Boolean(Object):
    def __init__(self, value) -> None: super().__init__("BOOLEAN", "True" if value == "true" else "False", value)

class Decimal(Object):
    def __init__(self, value) -> None: super().__init__("DECIMAL", f"decimal.Decimal(str({value}))", float(value))
    
    def sqrt(self, num):
        if (isinstance(num, list) and len(num) != 0): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        sqrt = m.sqrt(self.value)
        if (isinstance(sqrt, int) or sqrt == round(sqrt)): return Integer(sqrt)
        return Decimal(sqrt)
    
    def round(self, num):
        if (isinstance(num, list) and len(num) > 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        r = round(self.value, num.value) if num != [] else round(self.value)
        if isinstance(r, int): return Integer(r)
        return Decimal(r)

    def ceil(self, num):
        if (isinstance(num, list) and len(num) != 0): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        r = m.ceil(self.value)
        return Integer(r)
    
    def floor(self, num):
        if (isinstance(num, list) and len(num) != 0): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", str)
        r = m.floor(self.value)
        return Integer(r)

class Empty(Object):
    def __init__(self) -> None: super().__init__("EMPTY", "empty", "empty")

class Integer(Object):
    def __init__(self, value) -> None: super().__init__("INTEGER", f"decimal.Decimal(str({value}))" if str(value) not in "-infinity" else value, int(value) if str(value) not in "-infinity" else value)

    def sqrt(self, num):
        if (isinstance(num, list) and len(num) != 0): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", num)
        sqrt = m.sqrt(self.value)
        if (isinstance(sqrt, int) or sqrt == round(sqrt)): return Integer(sqrt)
        return Decimal(sqrt)

class Storage(Object):
    def __init__(self, value) -> None: super().__init__("STORAGE", "", value)

    def get(self, index):
        if (isinstance(index, list) and len(index) != 1): Error.ArgumentError(f"{self.name}.{currentframe().f_code.co_name}()", index)
        elif (index.type != "INTEGER"): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "INTEGERs", "argument")
        return self.value[index.value]

class Dictionary(Object):
    def __init__(self, key, value) -> None:
        v = f"{key.raw}: {value.raw}"
        super().__init__("DICT", v[1:-1] if v[0] == "\"" else v, value)
        self.key = key

class String(Object):
    def __init__(self, value) -> None:
        v = value.replace('\\\\', '\\').replace('\\\"', '\"').replace('\\n', '\n').replace('\\t', '\t').replace("\\s", " ")
        super().__init__("STRING", v, v[1:-1] if value.startswith('"') else v)
    
    def split(self, str):
        if (isinstance(str, list) and len(str) != 1): Error.ArgumentError(f"{self.type}.{currentframe().f_code.co_name}()", str)
        elif (str.type != "STRING"): Error.UnsupportedTypeError(f"{self.name}.{currentframe().f_code.co_name}()", "STRING", "argument")
        return Storage([String(v) for v in self.value.split(str.value)])

class Function(Object):
    def __init__(self, name, v, args, parent) -> None:
        super().__init__("FUNCTION", "", v)
        self.name = name
        self.args = args
        self.parent = parent

class Variable(Object):
    def __init__(self, name, type_, v:Object, isConst, parent) -> None:
        super().__init__(v.type if type_ == "any" else type_, v if v.raw == "" else v.raw, v.value)
        self.name = name
        self.isExplicit = False if type_ == "any" else True
        self.isConst = isConst
        self.parent = parent
    
    def set(self, value, mod, type_): 
        if (not self.isExplicit or self.type == value.type) and not self.isConst: 
            self.type = type_
            return self.modify(value, mod)
        Error.AssignmentError(self.name, value.value)

    def modify(self, value, mod):
        v = value.value
        if self.type in ["INTEGER", "DECIMAL"]:
            if mod == "+=": self.value += v
            elif mod == "-=": self.value -= v
            elif mod == "*=": self.value *= v
            elif mod == "/=": self.value /= v
            elif mod == "^=": self.value = self.value ** v
            elif mod == "#=": self.value = self.value ** (1/v)
            else: self.value = v
            
            if self.value == round(self.value): self.value = eval(f"decimal.Decimal(str({round(self.value)}))")
            else: self.value = eval(f"decimal.Decimal(str({self.value}))")
            return
        if isinstance(v, Object): Error.ArgumentAssignmentError()
        self.value = v

class Evaluator:
    def __init__(self, ast, path, args) -> None:
        self.ast = ast

        self.modules = [
            "stlib",
            "math"
        ]

        self.stlib = stlib(path, args)
        self.math = math(path)
        
        self.operators = ['+', "-", "*", "/"]

        self.functions  = [] 
        self.variables = []
        self.build(ast)
    
    def build(self, data):
        if isinstance(data, list):
            for node in data: self.execute(node)
        elif isinstance(data, dict): self.execute(data)
    
    def execute(self, loc):
        if loc["module"] == "funct": self.function(loc["name"], loc["content"], loc["args"], loc["parent"])
        elif loc["module"] == "if": self.if_(loc["condition"], loc["content"], loc["elif"], loc["else"])
        elif loc["module"] == "while": self.while_(loc["condition"], loc["content"])
        elif loc["module"] == "switch": self.switch(loc["input"], loc["content"])
        elif loc["module"] == "var": self.variable(loc["name"], self.objectify(loc["content"]), loc["type"], loc["mod"], loc["const"], loc["parent"])
        elif loc["module"] == "execute": self.execut(loc["content"])
        elif loc["module"] == "write": self.write(self.objectify(loc["content"]))
        elif loc["module"] == "clear": _ = system('cls' if os.name == 'nt' else 'clear')
        elif loc["module"] == "delay": sleep(self.objectify(loc["content"]).value)
        elif loc["module"] == "call": self.direct_call(loc["funct"], loc["parent"])
    
    def objectify(self, loc):
        if isinstance(loc, list):
            ob = [self.objectify(o) if (isinstance(o, dict) and o.get('key')) or (isinstance(o, dict) and o["type"] != "OPERATOR") or isinstance(o, str) else o for o in loc]
            for op in ob:
                if isinstance(op, dict) and op.get("type") == "OPERATOR":
                    if [o["content"] for o in loc] == ['0', '/', '0']: return Integer("infinity")
                    return self.objectify(eval(''.join([o.value if isinstance(o, Object) else o for o in self.condition(ob)])))
            return (ob if len(ob) != 1 else ob[0])
        elif isinstance(loc, Object): return loc
        elif isinstance(loc, dec):
            if '.' in str(loc): return Decimal(float(loc))
            return Integer(int(loc) if str(loc) not in "-infinity" else loc)
        elif isinstance(loc, str): 
            if '"' in loc: return String(loc)
            elif match(r"(\-)?[0-9_]+\.[0-9_]+", loc): return Decimal(float(loc))
            elif match(r"(\-)?([0-9_]+|infinity)", loc): return Integer(int(loc) if loc not in "-infinity" else loc)
            return self.getVariable(loc.rsplit('.', 1)[-1], loc.rsplit('.', 1)[0])
        elif isinstance(loc, int): return Integer(loc)
        elif loc.get('key'): return Dictionary(self.objectify(loc['key']), self.objectify(loc['value']))
        elif loc.get("funct"): return self.objectify(self.getFunction(loc["funct"], loc["content"]))
        elif loc["type"] == "BOOLEAN": return Boolean(loc["content"])
        elif loc["type"] == "DECIMAL": return Decimal(float(loc["content"]))
        elif loc["type"] == "EMPTY": return Empty()
        elif loc["type"] == "INTEGER": return Integer(int(loc["content"]) if str(loc["content"]) not in "-infinity" else loc["content"])
        elif loc["type"] == "STORAGE": return Storage(self.objectify(loc["content"]))
        elif loc["type"] == "STRING": return String(loc["content"])
        elif loc["type"] == "IDENTIFIER": return self.getVariable(loc["content"].rsplit('.', 1)[-1], loc["content"].rsplit('.', 1)[0])
        elif loc["type"] == "CALL": return self.getFunction(loc["funct"], loc["content"])
    
    def function(self, name, content, args, parent):
        for funct in self.functions:
            if funct.name == name: 
                funct.value = content
                return
        if name == "init":
            if parent == "": return self.build(content)
        self.functions.append(Function(name, content, args, parent))
    
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
            if case.get("name") == None: return self.build(case["content"])
            if self.objectify(input).value == self.objectify(case["name"]).value: return self.build(case["content"])
        return
    
    def condition(self, condition):
        if not isinstance(condition, list) or len(condition) <= 1: return self.objectify(condition).raw
        return ' '.join([(((self.objectify(c).raw if c["type"] not in ["COMPARATOR", "OPERATOR"] else c["content"]) if isinstance(c, dict) else self.objectify(c).raw) if not isinstance(c, str) else c) if not isinstance(c, Object) else c.raw for c in condition])
    
    def variable(self, name, content, type_, mod, const, parent):
        c = content if isinstance(content, Storage) or isinstance(content, list) and len(content) != 1 else content[0] 
        for var in self.variables:
            if var.name == name:
                return var.set(c, mod, c.type)
        if type_ != "any" and c.type != type_: Error.AssignmentError(name, c.value)
        self.variables.append(Variable(name, type_, c, const, parent))

    def getVariable(self, name, parent):
        for var in self.variables:
            if var.name == name and var.parent == ("" if parent == name else parent):
                if var.type == "FUNCTION": return var.value
                return var
        if parent in self.modules and getattr(getattr(self, parent), name, None) != None: return getattr(getattr(self, parent), name)
        Error.VariableNotFoundError(name)
    
    def getFunction(self, funs, parent):
        value = self.objectify(parent)
        for fun in funs:
            name = fun["name"]
            args = fun["args"]
            value = self.grabFunction(name, args, value, parent)
        return value
    
    def grabFunction(self, name, args, v, parent):
        try:
            val = v if not isinstance(v, Variable) else self.objectify(v.value)
            if isinstance(val, list) and isinstance(v, Variable): val = Storage(val)

            if parent in self.modules and getattr(getattr(self, parent), name, None) != None: return getattr(getattr(self, parent), name)(self.objectify(args))
            if parent not in self.modules and getattr(val, name, None) != None: return getattr(val, name)(self.objectify(args))
        except AttributeError: Error.DoesNotHaveFunctionError(v.type, f"{name}()")
        Error.FunctionNotFoundError(f"{(parent + '.') if parent != '' else ''}{name}()")
    
    def write(self, ob):
        if isinstance(ob, list) or ob.type == "STORAGE": return print(f"{[o.value if o.type != 'DICT' else o.raw for o in ob.value]}".replace('[', '<').replace(']', '>').replace('\'', '\"'))
        elif ob.type == "DICT": return print(f"{ob.value.value}")
        elif isinstance(ob, Object): return print(ob.value)
        elif isinstance(ob, float) or isinstance(ob, dec): return print(ob)

        for o in ob: print(o.value)
    
    def direct_call(self, fun, parent):
        for funct in self.functions:
            name = fun[0]["name"]
            args = fun[0]["args"]
            if name == funct.name and funct.parent == parent:
                if len(args) == len(funct.args): return self.build(self.replaceArgs(funct, args))
                elif len(args) > len(funct.args): Error.ArgumentError(f"{(parent + '.') if parent != '' else ''}{name}()", args)
                Error.ArgumentError(f"{(parent + '.') if parent != '' else ''}{name}()", args)
        Error.FunctionNotFoundError(f"{(parent + '.') if parent != '' else ''}{name}()")

    def call(self, name, fun, parent):
        for funct in self.functions:
            for f in fun: 
                name = f["name"]
                args = f["args"]
                if name == funct.name and funct.parent == parent:
                    if len(args) == len(funct.args): return self.build(self.replaceArgs(funct, args))
                    elif len(args) > len(funct.args): Error.ArgumentError(f"{(parent + '.') if parent != '' else ''}{name}()", args)
                    Error.ArgumentError(f"{(parent + '.') if parent != '' else ''}{name}()", args)
        Error.FunctionNotFoundError(f"{(parent + '.') if parent != '' else ''}{name}()")
    
    def replaceArgs(self, f, args):
        val = f
        if args != []:
            for c in val.value:
                for idx, data in enumerate(args):
                    f_args = val.args[idx]
                    c["content"] = [data if f_args == dat else dat for dat in c["content"]]
        return val.value