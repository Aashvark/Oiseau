from re import match
from packages.ErrorManager import Error

class Lexer:
    def __init__(self, file):
        self.file  = file
        self.tokens = []
        
        self.tokenize()
    
    def tokenize(self):
        tickets = self.ticketize(self.file.replace('~', '=').replace(' ', 'α').replace('\n', 'β').replace('\\\"', "γ").replace('\\\\', "δ").replace('\\t', "ε").replace('\\n', 'ζ'))
        
        for ticket in tickets:
            base = ticket.split('.')[0]
            funs = ticket.split('.')[1:]
            for idx, fun in enumerate(funs):
                if '(' not in fun: base += '.' + funs.pop(idx) 
            args = [ticket[:-1].rsplit('(', 1)[-1].replace(',', '')]

            if match(r"\%(.|\n)*?\%|\$(.|\n)*?\$", ticket) or ticket in ['\n']: continue
            elif match(r"(inject|fun|if|elif|else|while|switch|case|endcase|clear|delay|write)\b", ticket): self.addToken("COMMAND", ticket)
            elif match(r"(true|false)\b", ticket): self.addToken("BOOLEAN", ticket, funs)
            elif match(r"(as)\b", ticket): self.addToken("RENAME", ticket)
            elif match(r"(empty)\b", ticket): self.addToken("EMPTY", 'empty', funs)
            elif match(r"(\-)?[0-9_]+\.[0-9_]+", ticket): self.addToken("DECIMAL", base.replace('_', ''), funs)
            elif match(r"(\-)?([0-9_]+|infinity)", ticket): self.addToken("INTEGER", base.replace('_', ''), funs)
            elif match(r"<(.*?)>", ticket):
                args = [ticket[:-1].rsplit('<', 1)[-1].replace(',', '')]
                lex = Lexer('' if args == [''] else ','.join(args)).tokens
                for idx, arg in enumerate(lex):
                    if arg["type"] == "COLON":
                        lex[idx - 1] = {"key": lex.pop(idx - 1), "value": lex.pop(idx)}
                self.addToken("STORAGE", lex, funs)
            elif match(r"\"(.*?)\"", ticket): self.addToken("STRING", base, funs)
            elif match(r"(\!)?(boolean|decimal|integer|string)\b", ticket): self.addToken("DATATYPE", ticket)
            elif match(r"\((.*?)\)", ticket): self.addToken("ARGUMENT", Lexer('' if args == [''] else ','.join(args)).tokens)
            elif match(r"([A-Za-z]+[A-Za-z0-9]*?(\.)*?)*?(\((.*?)\))", ticket): 
                if '(' in base:
                    funs.insert(0, f"{base.split('(', 1)[0]}({base[:-1].split('(')[1]})")
                    self.addToken("CALL", '', funs)
                else: self.addToken("CALL", base, funs)
            elif match(r"(\!)?[A-Za-z]+[A-Za-z0-9\-\_]*", ticket): self.addToken("IDENTIFIER", ticket, funs)
            elif ticket.replace('~', '=') in ['=', '+=', '-=', '/=', '*=', '^=', '#=']: self.addToken("ASSIGN", ticket.replace('~', '='))
            elif ticket.replace('~', '=') in ['==', '!=', '>=', '<=', '>', '<']: self.addToken("COMPARATOR", ticket.replace('~', '='))
            elif ticket in ['+', '-', '*', '/']: self.addToken("OPERATOR", ticket)
            elif ticket in ["++", "--"]: self.addToken("SHORT_MOD", ticket)
            elif ticket == "{": self.addToken("OPEN_CURLY_BRACKET", ticket)
            elif ticket == "}": self.addToken("CLOSE_CURLY_BRACKET", ticket)
            elif ticket == ':': self.addToken("COLON", ticket)
            elif ticket == ';': self.addToken("STATEMENT_END", ticket)
            elif ticket != ' ': Error.UnknownError(ticket)
    
    def ticketize(self, file):
        tStr = []
        isolate = ['%', '"', ':', ';', "=", "(", ",", ")", "{", "}", "<", ">", "+", "*", "!", "-", "/", "α", "β", "γ", "δ", "ε", "ζ"]
        capture = ['%', '"', "(", ")", "<", ">"]
        capturing = False

        for idx, data in enumerate(file):            
            d = data.replace("α", ' ').replace("β", '\n').replace("γ", "\\\"").replace("δ", "\\\\").replace("ε", '\\t').replace("ζ", '\\n')
            if file[idx - 1] in isolate or data in isolate:
                if data in capture: capturing = not capturing
                tStr.append(d)
                continue
            if tStr != []: tStr[-1] += d
            else: tStr.append(d)
        
        holdType = ""
        tickets, holding = [], []
        
        for idx, data in enumerate(tStr):
            if holdType in ["COMMENT", "STRING"] and data not in ["$", "%", "\""]: holding.append(data)
            elif data == "\"" and holdType in ["ARGUMENT", "STORAGE"]: holding.append(data)
            elif data == "%":
                if holdType == "": holdType = "COMMENT"
                elif holdType == "COMMENT":
                    tickets.append(f"%{''.join(holding)}%")
                    holdType = ""
                    holding = []
                else: Error.NotStartedError("COMMENT")
            elif data == "$":
                if holdType == "": holdType = "COMMENT"
                elif holdType == "COMMENT":
                    tickets.append(f"%{''.join(holding)}%")
                    holdType = ""
                    holding = []
                else: Error.NotStartedError("COMMENT")
            elif data == "\"":
                if holdType == "": holdType = "STRING"
                elif holdType == "STRING":
                    tickets.append(f"\"{''.join(holding)}\"")
                    holdType = ""
                    holding = []
                else: Error.NotStartedError("STRING")
            elif data == "(":
                if holdType == "": holdType = "ARGUMENT"
                else: Error.UnexpectedStartError("ARGUMENT")
            elif data == ")":
                if holdType == "ARGUMENT":
                    if match(r"\.[A-Za-z0-9\-\_\"\<]+[A-Za-z0-9\-\_]*", tickets[-1]):
                        tickets[-2] += tickets[-1] + f"({''.join(holding)})"
                        tickets = tickets[:-1]
                    elif match(r"[A-Za-z0-9\-\_\"\<]+[A-Za-z0-9\-\_]*", tickets[-1]): 
                        tickets[-1] += f"({''.join(holding)})"
                    else: tickets.append(f"({''.join(holding)})")

                    holdType = ""
                    holding = []
                else: Error.NotStartedError("ARGUMENT")
            elif data == "<":
                if holdType == "": holdType = "STORAGE"
                else: Error.UnexpectedStartError("STORAGE")
            elif data == ">":
                if holdType == "STORAGE":
                    tickets.append(f"<{''.join(holding)}>")
                    holdType = ""
                    holding = []
                else: Error.NotStartedError("STORAGE")
            elif data == "=" and tickets[-1] in ["=", "!", "?", ">", "<", "+", "-", "/", "*", '^', '#']: tickets[-1] += data
            elif data in ["+", "-"] and tickets[-1] == data: tickets[-1] += data
            elif tickets != [] and tickets[-1] == "!":
                if holdType == "": tickets[-1] += data
                else: holding[-1] += data
            else:
                if holdType == "": tickets.append(data)
                else: holding.append(data)
        return tickets
    
    def addToken(self, type_, content, funs = None):
        self.tokens.append({"type": type_, "content": content})
        if funs != None and funs not in [[''], []]:
            if self.tokens[-1].get("funct") == None: self.tokens[-1].update({"funct": []})
            for fun in funs:
                name = fun[:-1].split('(', 1)[0]
                arg = fun[:-1].split('(', 1)[-1]
                self.tokens[-1]["funct"].append({"name": name, "args": Lexer(','.join([arg.replace(',', '')])).tokens})
            
