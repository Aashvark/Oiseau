from packages.ErrorManager import SimpleError

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.ast    = []
        
        self.global_types = ["BOOLEAN", "DECIMAL", "EMPTY", "INTEGER", "STRING", "IDENTIFIER", "OPERATOR"]
        
        self.index = 0
        self.buildAST()
    
    def buildAST(self):
        while self.index < len(self.tokens):
            stream = self.tokens[self.index:]
            t_type = self.tokens[self.index]["type"]
            t_val  = self.tokens[self.index]["content"]
            
            if t_type in ["COMMENT", "ATOM"]: pass
            elif t_type == "IDENTIFIER": self.parseVariable(stream)
            elif t_type == "COMMAND":
                if t_val == "fun": self.parseFunction(stream)
                elif t_val == "if": self.parseIf(stream)
                elif t_val == "while": self.parseWhile(stream)
                elif t_val == "execute": self.parseExecute(stream)
                elif t_val == "write": self.parseWrite(stream)
            elif t_type == "CALL": self.parseCall(stream)
                                
            self.index += 1
    
    def addAST(self, ast_):
        self.ast.append(ast_)
    
    def datatype(self, token):
        if token == '': return ''
        return {"type": token["type"], "content": token["content"]}
    
    def parseVariable(self, stream):
        value   = []
        checked = 0
        
        for idx, data in enumerate(stream):
            t_type  = data["type"]
            
            if t_type == "STATEMENT_END":
                if idx < 3: SimpleError("StatementEndedEarlyError", "variable was ended too early.")
                self.addAST({"module": 'var', "name": stream[0]["content"], "content": value})
                checked = idx
                break
            
            if idx == len(stream) - 1: SimpleError("StatementNotEndedError", "variable was not ended.")
            elif idx == 1 and t_type != "ASSIGN": SimpleError("InvalidTypeError", "variable wasn't completed.")
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
