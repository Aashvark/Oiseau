from packages.ErrorManager import Error
from packages.Lexer import Lexer

class Parser:
    def __init__(self, tokens, path) -> None:
        self.tokens = tokens
        self.ast    = []
        self.path = path

        self.parent = ""
        
        self.global_types = ["BOOLEAN", "DECIMAL", "EMPTY", "INTEGER", "STORAGE", "STRING", "IDENTIFIER", "OPERATOR", "CALL"]
        self.caseTypes = ["BOOLEAN", "CALL", "DECIMAL", "EMPTY", "IDENTIFIER", "INTEGER", "STORAGE", "STRING", "OPERATOR"]
        self.numeric = ["DECIMAL", "INTEGER", "OPERATOR"]

        self.index = 0
        self.caseIndex = 0
        self.buildAST()
    
    def buildAST(self):
        while self.index < len(self.tokens):
            stream = self.tokens[self.index:]
            t_type = self.tokens[self.index]["type"]
            t_val  = self.tokens[self.index]["content"]

            if t_type == "DATATYPE": self.parseExplicitVariable(stream)
            elif t_type == "IDENTIFIER": self.parseVariable(stream)
            elif t_type == "COMMAND":
                if t_val == "inject": self.parseInject(stream)
                elif t_val == "fun": self.parseFunction(stream)
                elif t_val == "if": self.parseIf(stream)
                elif t_val == "while": self.parseWhile(stream)
                elif t_val == "switch": self.parseSwitch(stream)
                elif t_val == "write": self.parseWrite(stream)
                elif t_val == "clear": self.parseClear(stream)
                elif t_val == "delay": self.parseDelay(stream)
            elif t_type == "CALL": self.parseCall(stream)
            self.index += 1
    
    def addAST(self, ast_, front:bool = False):
        if front: 
            self.ast.insert(0, ast_)
            return
        self.ast.append(ast_)
    
    def datatype(self, token):
        if token == '': return []
        return token
    
    def parseInject(self, stream):
        value   = []
        name    = ""
        checked = 0
        funct = stream[0]["content"]
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]
            
            if t_type == "STATEMENT_END":
                if idx < 1 or idx == 3 and name == "": Error.StatementEndedEarlyError(funct)
                v = value['content'].replace('\\', '/').replace('"', '')
                data = Parser(Lexer(open(f"{self.path}/{v.removeprefix('/')}".replace('/', '\\') if not value['content'].lower().startswith('c:/') else value['content'].replace('/', '\\'), "r").read()).tokens, self.path).ast
                for dat in data:
                    if dat["module"] in ["var", "funct"]:
                        dat["parent"] = name if name != "" else v.rsplit('/', 1)[-1].split('.')[0] if dat["parent"] == "" else v.rsplit('/', 1)[-1].split('.')[0] + dat["parent"]
                self.ast.extend(data)
                checked = idx
                break
            
            if idx == 4: Error.StatementNotEndedError(funct)
            elif idx == 1:
                if t_type in self.global_types: value = self.datatype(data)
                else: Error.UnsupportedTypeError(funct, t_type)
            elif idx == 2 and t_type != "RENAME": Error.NotCompletedError(funct, "as")
            elif idx == 3:
                if t_type == "IDENTIFIER": name = t_value
                else: Error.UnsupportedTypeError(funct, "IDENTIFIER", "name")

        self.index += checked
    
    def parseExplicitVariable(self, stream):
        name, value, checked = "", [], 0
        funct = "variable"

        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]
            
            if t_type == "STATEMENT_END":
                if idx == 4: Error.StatementEndedEarlyError(funct)
                if value == []:
                    e = stream[0]["content"].upper()
                    if e == "BOOLEAN": value = {"type": e, "content": "false"}
                    elif e == "DECIMAL": value = {"type": e, "content": "0.0"}
                    elif e == "INTEGER": value = {"type": e, "content": "0"}
                    elif e == "STRING": value = {"type": e, "content": "\"\""}

                self.addAST({"module": 'var', "name": name, "content": value, "type": stream[0]["content"].upper(), "const": True if stream[0]["content"][0] == '!' else False, "mod": '=', "parent": self.parent})
                checked = idx
                break
            
            if idx == len(stream) - 1: Error.StatementNotEndedError(funct)
            elif idx == 1 and t_type != "COLON": Error.NotCompletedError(funct, ":")
            elif idx == 2:
                if t_type == "IDENTIFIER": name = t_value
                else: Error.UnsupportedTypeError(funct, "IDENTIFIER", "name")
            elif idx == 3 and t_type != "ASSIGN": Error.NotCompletedError(funct, "ASSIGN")
            elif idx >= 4:
                if t_type in self.global_types: value.append(self.datatype(data))
                else: Error.UnsupportedTypeError(funct, t_type, "value")
        self.index += checked

    def parseVariable(self, stream):
        value   = []
        modif   = ''
        isShort = False
        checked = 0
        funct = "variable"
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]
            
            if t_type == "STATEMENT_END":
                if not isShort and idx == 2: Error.StatementEndedEarlyError(funct)
                self.addAST({"module": 'var', "name": stream[0]["content"].removeprefix('!'), "content": {"type": "EMPTY", "content": "empty"} if value == [] else value, "type": "any", "const": True if stream[0]["content"][0] == '!' else False, "mod": modif, "parent": self.parent})
                checked = idx
                break
            
            if idx == len(stream) - 1: Error.StatementEndedEarlyError(funct)
            elif idx == 1:
                if t_type == "ASSIGN": modif = t_value
                elif t_type == "SHORT_MOD":
                    modif = t_value[0] + '='
                    isShort = True
                    value = [{'type': 'INTEGER', 'content': '1'}]
                else: Error.NotCompletedError(funct)
            elif idx >= 2:
                if t_type in self.global_types: value.append(self.datatype(data))
                else: Error.UnsupportedTypeError(funct, t_type, "value")
        self.index += checked
    
    def parseFunction(self, stream):
        name    = ""
        args, value = [], []
        opened, checked = 0, 0
        funct = "function"
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]
            
            if t_type == "STATEMENT_END" and opened == 0:
                if idx < 6: Error.StatementNotEndedError(funct)
                self.addAST({"module": 'funct', "name": name, "content": Parser(value, self.path).ast, "args": args, "parent": self.parent}, True)
                checked = idx
                break
            
            if idx == len(stream) - 1: Error.StatementNotEndedError(funct)
            elif idx == 1:
                if t_type == "IDENTIFIER": name = t_value
                else: Error.UnsupportedTypeError(funct, "IDENTIFIER", "name")
            elif idx == 2 and t_type != "ASSIGN": Error.NotCompletedError(function, "ASSIGN")
            elif idx == 3:
                if t_type == "ARGUMENT": args = t_value
                else: Error.UnsupportedTypeError(funct, t_type, "ARGUMENT")
            elif idx == 4:
                if t_type != "OPEN_CURLY_BRACKET": Error.NotStartedError(funct)
                opened += 1
            elif idx >= 5:
                if t_type == "OPEN_CURLY_BRACKET": opened += 1
                elif t_type == "CLOSE_CURLY_BRACKET": opened -= 1
                value.append(data)
        self.index += checked
    
    def parseIf(self, stream):
        passedCondition, hasElse = False, False
        condition, value, if_ = [], [], []
        checked, opened = 0, 0
        funct = stream[0]["content"]
        
        for idx, data in enumerate(stream):
            t_type   = data["type"]
            t_value  = data["content"]

            if t_type == "CLOSE_CURLY_BRACKET":
                if idx < 6: Error.StatementEndedEarlyError(funct)
                if_.append([condition, value])
                opened -= 1

                if stream[idx + 1]["content"] in ["elif", "else"] and not hasElse: continue
                elif stream[idx + 1]["content"] == ";" and opened == 0:
                    condition, value = [], []

                    for idy, if_s in enumerate(if_):
                        ast = Parser(if_s[1], self.path).ast

                        if idy == len(if_) - 1 and hasElse: self.ast[-1]["else"] = ast
                        elif idy > 0: self.ast[-1]["elif"].append({"condition": if_s[0], "content": ast})
                        else: self.addAST({"module": 'if', "condition": if_s[0], "content": ast, "elif": [], "else": []})
                    checked = idx + 1
                    break
                else: Error.StatementNotEndedError(funct)

            if idx > 0:
                if not passedCondition: 
                    if t_type in ["BOOLEAN", "DECIMAL", "EMPTY", "INTEGER", "STRING", "IDENTIFIER", "OPERATOR", "COMPARATOR"]: condition.append(self.datatype(data))
                    elif t_type == "OPEN_CURLY_BRACKET": 
                        passedCondition = True
                        opened += 1
                else:
                    if t_value == "elif":
                        if_.append([condition, value])
                    elif t_value == "else": hasElse = True                    
                    else: 
                        value.append(data)
                        continue

                    passedCondition = False
                    condition, value = [], []
        self.index += checked
    
    def parseWhile(self, stream):
        passedCondition = False
        condition, value = [], []
        checked, opened = 0, 0
        funct = stream[0]["content"]
        
        for idx, data in enumerate(stream):
            t_type   = data["type"]

            if t_type == "CLOSE_CURLY_BRACKET":
                if idx < 6: Error.StatementEndedEarlyError(funct)
                opened -= 1

                if stream[idx + 1]["content"] == ";" and opened == 0:
                    ast = Parser(value, self.path).ast
                    self.addAST({"module": 'while', "condition": condition, "content": ast})
                    checked = idx + 1
                    break
                else: Error.StatementNotEndedError(funct)

            if idx >= 1:
                if not passedCondition: 
                    if t_type in ["BOOLEAN", "DECIMAL", "EMPTY", "INTEGER", "STRING", "IDENTIFIER", "OPERATOR", "COMPARATOR"]: condition.append(self.datatype(data))
                    elif t_type == "OPEN_CURLY_BRACKET": 
                        passedCondition = True
                        opened += 1
                else: value.append(data)
        self.index += checked
    
    def parseSwitch(self, stream):
        input    = ""
        value = []
        checked, opened = 0, 0
        funct = stream[0]["content"]
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]

            if t_type == "STATEMENT_END" and opened == 0:
                if idx == 4: Error.StatementEndedEarlyError(funct)
                self.addAST({"module": 'switch', "input": input, "content": self.breakCases(value[:-1])})
                checked = idx
                break
            
            if idx == len(stream) - 1: Error.StatementNotEndedError(funct)
            elif idx == 1:
                if t_type in self.caseTypes: input = data
                else: Error.UnsupportedTypeError(funct, t_type, "condition")
            elif idx == 2:
                if t_type != "OPEN_CURLY_BRACKET": Error.NotStartedError(funct)
                opened += 1
            elif idx >= 3: 
                if t_type == "OPEN_CURLY_BRACKET": opened += 1
                elif t_type == "CLOSE_CURLY_BRACKET": opened -= 1
                value.append(data)
        self.index += checked
    
    def breakCases(self, tokens):
        cases = []

        while self.caseIndex < len(tokens):
            stream = tokens[self.caseIndex:]
            t_type = tokens[self.caseIndex]["type"]
            t_val  = tokens[self.caseIndex]["content"]

            if t_type == "COMMAND":
                if t_val == "case": cases.append(self.parseCase(stream))
                elif t_val == "endcase": cases.append(self.parseEndCase(stream))
                else: Error.NotUsedError("switch", "case")
            
            self.caseIndex += 1
        self.caseIndex = 0
        return cases
    
    def parseCase(self, stream): 
        name = ""
        content = []
        case = {"name": "", "content": []}
        opened, checked = 0, 0
        funct = "switch case"

        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]

            if t_type == "CLOSE_CURLY_BRACKET":
                opened -= 1
                if opened == 0:
                    case["name"] = name
                    case["content"] = Parser(content, self.path).ast
                    checked = idx
                    break
                opened += 1

            if idx == len(stream) - 1: Error.StatementNotEndedError(funct)
            elif idx == 1:
                if t_type in self.caseTypes: name = data
                else: Error.UnsupportedTypeError(funct, t_type, "condition")
            elif idx == 2 and t_type != "COLON": Error.NotCompletedError(funct, ":")
            elif idx == 3:
                if t_type != "OPEN_CURLY_BRACKET": Error.NotStartedError(funct)
                opened += 1
            elif idx >= 4: 
                if t_type == "OPEN_CURLY_BRACKET": opened += 1
                elif t_type == "CLOSE_CURLY_BRACKET": opened -= 1
                content.append(data)
        self.caseIndex += checked
        return case
    
    def parseEndCase(self, stream): 
        content = []
        case = {"content": []}
        opened, checked = 0, 0
        funct = "switch case"

        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]

            if t_type == "CLOSE_CURLY_BRACKET":
                opened -= 1
                if opened == 0:
                    case["content"] = Parser(content, self.path).ast
                    checked = idx
                    break
                opened += 1

            if idx == len(stream) - 1: Error.StatementNotEndedError(funct)
            if idx == 1 and t_type != "COLON": Error.NotCompletedError(funct, ":")
            elif idx == 2:
                if t_type != "OPEN_CURLY_BRACKET": Error.NotStartedError(funct)
                opened += 1
            elif idx >= 3: 
                if t_type == "OPEN_CURLY_BRACKET": opened += 1
                elif t_type == "CLOSE_CURLY_BRACKET": opened -= 1
                content.append(data)
        self.caseIndex += checked
        return case
    
    def parseWrite(self, stream):
        value   = []
        checked = 0
        funct = stream[0]["content"]
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            
            if t_type == "STATEMENT_END":
                if idx < 2: Error.StatementEndedEarlyError(funct)
                self.addAST({"module": 'write', "content": value})
                checked = idx
                break
            
            if idx == len(stream) - 1: Error.StatementNotEndedError(funct)
            elif idx >= 1:
                if t_type in self.global_types: value.append(self.datatype(data))
                else: Error.UnsupportedTypeError(funct, t_type, "value")
        self.index += checked
    
    def parseClear(self, stream):
        checked = 0
        funct = stream[0]["content"]
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            
            if t_type == "STATEMENT_END":
                self.addAST({"module": 'clear', "content": []})
                checked = idx
                break
            
            if idx >= 2: Error.StatementNotEndedError(funct)
        self.index += checked

    def parseDelay(self, stream):
        value = []
        checked = 0
        funct = stream[0]["content"]
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_val  = data["content"]
            
            if t_type == "STATEMENT_END":
                if idx < 2: Error.StatementEndedEarlyError(funct)
                self.addAST({"module": 'delay', "content": value})
                checked = idx
                break
            
            if idx == len(stream) - 1: Error.StatementNotEndedError(funct)
            elif idx >= 1:
                if t_type in self.numeric: value.append(data)
                else: Error.UnsupportedTypeError(funct, t_type, "value")
        self.index += checked     

    def parseCall(self, stream):
        checked = 0
        funct = "function call"

        for idx, data in enumerate(stream):
            t_type  = data["type"]
            
            if t_type == "STATEMENT_END":
                if idx < 1: Error.StatementEndedEarlyError()
                self.addAST({"module": 'call', "content": "", "funct": stream[0]["funct"], "parent": stream[0]["content"]})
                checked = idx
                break
            
            if idx == len(stream) - 1: Error.StatementNotEndedError(funct)
            
        self.index += checked