from packages.ErrorManager import SimpleError

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.ast    = []
        
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
                if t_val == "fun": self.parseFunction(stream)
                elif t_val == "if": self.parseIf(stream)
                elif t_val == "while": self.parseWhile(stream)
                elif t_val == "switch": self.parseSwitch(stream)
                elif t_val == "execute": self.parseExecute(stream)
                elif t_val == "write": self.parseWrite(stream)
                elif t_val == "clear": self.parseClear(stream)
                elif t_val == "delay": self.parseDelay(stream)
            elif t_type == "CALL": self.parseCall(stream)
                                
            self.index += 1
    
    def addAST(self, ast_):
        self.ast.append(ast_)
    
    def datatype(self, token):
        if token == '': return []
        return token
    
    def parseExplicitVariable(self, stream):
        name    = ""
        value   = []
        checked = 0
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]
            
            if t_type == "STATEMENT_END":
                if idx == 4: SimpleError("StatementEndedEarlyError", "variable was ended too early.")
                if value == []:
                    e = stream[0]["content"].upper()
                    if e == "BOOLEAN": value = {"type": e, "content": "false"}
                    elif e == "DECIMAL": value = {"type": e, "content": "0.0"}
                    elif e == "INTEGER": value = {"type": e, "content": "0"}
                    elif e == "STRING": value = {"type": e, "content": "\"\""}

                self.addAST({"module": 'var', "name": name, "content": value, "type": stream[0]["content"].upper(), "const": True if stream[0]["content"][0] == '!' else False, "mod": '='})
                checked = idx
                break
            
            if idx == len(stream) - 1: SimpleError("StatementNotEndedError", "variable was not ended.")
            elif idx == 1 and t_type != "COLON": SimpleError("InvalidTypeError", "variable wasn't completed; missing ':'")
            elif idx == 2:
                if t_type == "IDENTIFIER": 
                    name = t_value
                else: SimpleError("InvalidTypeError", "variable wasn't completed; missing '='")
            elif idx == 3 and t_type != "ASSIGN": SimpleError("InvalidTypeError", "variable wasn't completed; missing '='")
            elif idx >= 4:
                if t_type in self.global_types: value.append(self.datatype(data))
                else: SimpleError("InvalidTypeError", f"variable doesn't support {t_type}s")
        self.index += checked

    def parseVariable(self, stream):
        value   = []
        modif   = ''
        isShort = False
        checked = 0
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]
            
            if t_type == "STATEMENT_END":
                if not isShort and idx == 2: SimpleError("StatementEndedEarlyError", "variable was ended too early.")
                self.addAST({"module": 'var', "name": stream[0]["content"].removeprefix('!'), "content": {"type": "EMPTY", "content": "empty"} if value == [] else value, "type": "any", "const": True if stream[0]["content"][0] == '!' else False, "mod": modif})
                checked = idx
                break
            
            if idx == len(stream) - 1: SimpleError("StatementNotEndedError", "variable was not ended.")
            elif idx == 1:
                if t_type == "ASSIGN": modif = t_value
                elif t_type == "SHORT_MOD":
                    modif = t_value[0] + '='
                    isShort = True
                    value = [{'type': 'INTEGER', 'content': '1'}]
                else: SimpleError("InvalidTypeError", "variable wasn't completed.")
            elif idx >= 2:
                if t_type in self.global_types: value.append(self.datatype(data))
                else: SimpleError("InvalidTypeError", f"variable doesn't support {t_type}s")
        self.index += checked
    
    def parseFunction(self, stream):
        name    = ""
        args    = []
        value   = []
        ended = False
        checked = 0
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]
            
            if t_type == "STATEMENT_END" and ended:
                if idx < 6: SimpleError("StatementEndedEarlyError", "the function was ended too early.")
                ast = Parser(value).ast
                self.addAST({"module": 'funct', "name": name, "content": ast, "args": args})
                checked = idx
                break
            
            if idx == len(stream) - 1 or ended: SimpleError("StatementNotEndedError", "the function was not ended properly.")
            
            if idx == 1:
                if t_type == "IDENTIFIER": name = t_value
                else: SimpleError("UnnamedFunction", "function wasn't named.")
            elif idx == 2 and t_type != "ASSIGN": SimpleError("InvalidTypeError", "the function wasn't completed.")
            elif idx == 3:
                if t_type == "ARGUMENT": args = t_value
                else: SimpleError("InvalidTypeError", f"the function wasn't completed.")
            elif idx == 4 and t_type != "OPEN_CURLY_BRACKET": SimpleError("InvalidTypeError", f"the function wasn't started")
            elif idx >= 5 and not ended:
                if t_type == "CLOSE_CURLY_BRACKET": ended = True
                else: value.append(data)
        self.index += checked
    
    def parseIf(self, stream):
        passedCondition, hasElse = False, False
        condition, value, if_ = [], [], []
        checked, opened = 0, 0
        
        for idx, data in enumerate(stream):
            t_type   = data["type"]
            t_value  = data["content"]

            if t_type == "CLOSE_CURLY_BRACKET":
                if idx < 6: SimpleError("StatementEndedEarlyError", "the if statement was ended too early.")
                if_.append([condition, value])
                opened -= 1

                if stream[idx + 1]["content"] in ["elif", "else"] and not hasElse: continue
                elif stream[idx + 1]["content"] == ";" and opened == 0:
                    condition, value = [], []

                    for idy, if_s in enumerate(if_):
                        ast = Parser(if_s[1]).ast

                        if idy == len(if_) - 1 and hasElse: self.ast[-1]["else"] = ast
                        elif idy > 0: self.ast[-1]["elif"].append({"condition": if_s[0], "content": ast})
                        else: self.addAST({"module": 'if', "condition": if_s[0], "content": ast, "elif": [], "else": []})
                    checked = idx + 1
                    break
                else: SimpleError("StatementNotEndedError", "the if statement was not ended.")

            if idx >= 1:
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
        
        for idx, data in enumerate(stream):
            t_type   = data["type"]

            if t_type == "CLOSE_CURLY_BRACKET":
                if idx < 6: SimpleError("StatementEndedEarlyError", "the while statement was ended too early.")
                opened -= 1

                if stream[idx + 1]["content"] == ";" and opened == 0:
                    ast = Parser(value).ast
                    self.addAST({"module": 'while', "condition": condition, "content": ast})
                    checked = idx + 1
                    break
                else: SimpleError("StatementNotEndedError", "the while statement was not ended.")

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
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]

            if t_type == "STATEMENT_END" and opened == 0:
                if idx == 4: SimpleError("StatementEndedEarlyError", "switch was ended too early.")
                self.addAST({"module": 'switch', "input": input, "cases": self.breakCases(value[:-1])})
                checked = idx
                break
            
            if idx == len(stream) - 1: SimpleError("StatementNotEndedError", "switch was not ended.")
            elif idx == 1:
                if t_type in self.caseTypes: input = data
                else: SimpleError("InvalidTypeError", "switch was missing a input condition")
            elif idx == 2:
                if t_type != "OPEN_CURLY_BRACKET": SimpleError("InvalidTypeError", "switch wasn't opened")
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
                if t_val != "case": SimpleError("NotUsedError", "case wasn't used")
                cases.append(self.parseCase(stream))

            self.caseIndex += 1
        self.caseIndex = 0
        return cases
    
    def parseCase(self, stream): 
        name = ""
        content = []
        case = {"name": "", "content": []}
        opened, checked = 0, 0
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_value  = data["content"]

            if t_type == "CLOSE_CURLY_BRACKET":
                opened -= 1
                if opened == 0:
                    case["name"] = name
                    case["content"] = Parser(content).ast
                    checked = idx
                    break
                opened += 1

            if idx == len(stream) - 1: SimpleError("StatementNotEndedError", "the switch case was not ended.")
            elif idx == 1:
                if t_type in self.caseTypes: name = data
                else: SimpleError("InvalidTypeError", "switch case wasn't given a comparasion")
            elif idx == 2 and t_type != "COLON": SimpleError("InvalidTypeError", "switch case wasn't completed; missing ':'")
            elif idx == 3:
                if t_type != "OPEN_CURLY_BRACKET": SimpleError("InvalidTypeError", "switch case wasn't opened")
                opened += 1
            elif idx >= 4: 
                if t_type == "OPEN_CURLY_BRACKET": opened += 1
                elif t_type == "CLOSE_CURLY_BRACKET": opened -= 1
                content.append(data)
        self.caseIndex += checked
        return case
    
    def parseExecute(self, stream):
        value   = []
        checked = 0
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            
            if t_type == "STATEMENT_END":
                if idx < 2: SimpleError("StatementEndedEarlyError", "the execute statement was ended too early.")
                self.addAST({"module": 'execute', "content": value})
                checked = idx
                break
            
            if idx == len(stream) - 1: SimpleError("StatementNotEndedError", "the execute statement was not ended.")
            elif idx >= 1:
                if t_type in self.global_types: value.append(self.datatype(data))
                else: SimpleError("InvalidTypeError", f"the execute statement doesn't support {t_type}s")
        self.index += checked
    
    def parseWrite(self, stream):
        value   = []
        checked = 0
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            
            if t_type == "STATEMENT_END":
                if idx < 2: SimpleError("StatementEndedEarlyError", "the write statement was ended too early.")
                self.addAST({"module": 'write', "content": value})
                checked = idx
                break
            
            if idx == len(stream) - 1: SimpleError("StatementNotEndedError", "the write statement was not ended.")
            elif idx >= 1:
                if t_type in self.global_types: value.append(self.datatype(data))
                else: SimpleError("InvalidTypeError", f"the write statement doesn't support {t_type}s")
        self.index += checked
    
    def parseClear(self, stream):
        checked = 0
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            
            if t_type == "STATEMENT_END":
                self.addAST({"module": 'clear'})
                checked = idx
                break
            
            if idx >= 2: SimpleError("StatementNotEndedError", "the clear statement was not ended.")
        self.index += checked

    def parseDelay(self, stream):
        value = []
        checked = 0
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            t_val  = data["content"]
            
            if t_type == "STATEMENT_END":
                if idx < 2: SimpleError("StatementEndedEarlyError", "the delay statement was ended too early.")
                self.addAST({"module": 'delay', "content": value})
                checked = idx
                break
            
            if idx == len(stream) - 1: SimpleError("StatementNotEndedError", "the delay statement was not ended.")
            elif idx >= 1:
                if t_type in self.numeric: value.append(data)
                else: SimpleError("InvalidTypeError", f"the delay statement doesn't support {t_type}s")
        self.index += checked     

    def parseCall(self, stream):
        checked = 0
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            
            if t_type == "STATEMENT_END":
                if idx < 1: SimpleError("StatementEndedEarlyError", "the function call was ended too early.")
                self.addAST({"module": 'call', "content": stream[0]["content"].rsplit('(', 1)[0], "args": stream[0]["args"] if stream[0]["content"] != [''] else []})
                checked = idx
                break
            
            if idx == len(stream) - 1: SimpleError("StatementNotEndedError", "the function call was not ended.")
            
        self.index += checked
