import re
import pygame
import sys

pygame.init()

functions = {}
variables = {"width": 500, "height": 350, "windowname": "Lasun pygame window", "bgR": 0, "bgG": 0, "bgB": 0}
rects = {}

class Execute:
    def __init__(self, code):
        self.in_func = False
        self.in_args = False
        self.code = code
        self.funcname = ""
        self.new_arg = False
        self.in_code = False
        self.used_bkt = False
        self.in_show = False
        self.varname = ""
        self.in_call = False
        self.in_funcname = False
        self.in_comment = False

    def execute1(self):
        tokens = tokenize(self.code)
        tokenpos = 1
        funcargs = []

        while tokenpos <= len(tokens):
            token = tokens[tokenpos - 1]
            tokenpos += 1

            if not self.in_args and not self.in_code and not self.in_comment:
                if token[0] == "WORD":
                    if token[1] == "fct":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token[0] == "WORD":
                            self.funcname = token[1]
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "LPAREN":
                                self.in_args = True
                                self.in_func = True
                                self.new_arg = True
                                funcargs = []
                            elif token[0] == "import":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "STRING":
                                    if token[1].replace("\"","").endswith(".lasun"):
                                        with open(token[1].replace("\"", ""), "r") as fi:
                                            Execute(fi.read()).execute1()
                        else:
                            print(f"Error: Use a word to define function name. used type: {token[0]}")
                            sys.exit(1)
                    else:
                        print("Error: you can only 'import \"filename.lasun\"' and 'fct myfunc() {...}'")
                        sys.exit(1)
                elif token[0] == "EXCLAMATION":
                    self.in_comment = True
            elif self.in_args:
                if self.in_func:
                    if self.new_arg:
                        if token[0] == "WORD":
                            funcargs.append(token[1])
                            self.new_arg = False
                        elif token[0] == "RPAREN":
                            self.in_args = False
                            functions[self.funcname] = {"code": [], "params": []}
                            self.in_code = True
                            self.new_arg = False
                    elif not self.new_arg:
                        if token[0] == "COMMA":
                            self.new_args = True
                        elif token[0] == "RPAREN":
                            self.in_args = False
                            functions[self.funcname] = {"code": [], "params": funcargs}
                            self.in_code = True
                            self.new_arg = False
                        else:
                            print("Error: you can only use ',' to new arguments and ')' to stop adding arguments")
                            sys.exit(1)
            elif self.in_code:
                if self.in_func:
                    if self.used_bkt:
                        if token[0] == "RBRACKET":
                            self.in_code = False
                            self.in_func = False
                            self.used_bkt = False
                        else:
                            functions[self.funcname]["code"].append(token[1])
                    elif not self.used_bkt:
                        if token[0] == "LBRACKET":
                            self.used_bkt = True
                        else:
                            print("Error: Use '{' to start a function code")
                            sys.exit(1)
            elif self.in_comment:
                if token[0] == "SEMICOLON":
                    self.in_comment = False
        try:
            Execute(" ".join(functions["main"]["code"])).execute2()
        except:
            pass

    def execute2(self):
        showargs = []
        tokens = tokenize(self.code)
        tokenpos = 1
        funcargs = []
        returned = []
        R = [0]
        G = [0]
        B = [0]
        keys = pygame.key.get_pressed()

        while tokenpos <= len(tokens):
            token = tokens[tokenpos - 1]
            tokenpos += 1

            if not self.in_show and not self.in_call and not self.in_comment:
                if token[0] == "WORD":
                    if token[1] == "show":
                        self.in_show = True
                    elif token[1] == "int":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token[0] == "WORD":
                            self.varname = token[1]
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    variables[self.varname] = int(token[1])
                                elif token[0] == "WORD":
                                    variables[self.varname] = variables.get(token[1])
                                else:
                                    print("Error: to create int variables, use integer values")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to atribute variables values")
                                sys.exit(1)
                        else:
                            print(f"Error: Use normal word to set variables name. used type: {token[0]}")
                            sys.exit(1)
                    elif token[1] == "str":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token[0] == "WORD":
                            self.varname = token[1]
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "STRING":
                                    variables[self.varname] = token[1].replace("\"", "").replace("\\n", "\n")
                                elif token[0] == "WORD":
                                    variables[self.varname] = variables.get(token[1])
                                else:
                                    print("Error: to create str variables, use string values")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to atribute variables values")
                                sys.exit(1)
                        else:
                            print(f"Error: Use normal word to set variables name. used type: {token[0]}")
                            sys.exit(1)
                    elif token[1] == "float":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token[0] == "WORD":
                            self.varname = token[1]
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "FLOAT":
                                    variables[self.varname] = float(token[1])
                                elif token[0] == "WORD":
                                    variables[self.varname] = variables.get(token[1])
                                else:
                                    print("Error: to create float variables, use floating values")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to atribute variables values")
                                sys.exit(1)
                        else:
                            print(f"Error: Use normal word to set variables name. used type: {token[0]}")
                            sys.exit(1)
                    elif token[1] in functions.keys():
                        self.in_call = True
                        self.funcname = token[1]
                    elif token[1] in variables.keys():
                        varname1 = [token[1]]
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token[0] == "PLUS":
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    variables[varname1[0]] += int(token[1])
                                elif token[0] == "FLOAT":
                                    variables[varname1[0]] += float(token[1])
                                elif token[0] == "WORD":
                                    variables[varname1[0]] += variables.get(token[1])
                                elif token[0] == "STRING":
                                    variables[varname1[0]] += token[1].replace("\"", "").replace("\\n", "\n")
                                else:
                                    print(f"Error: can't use this type to sum: {token[0]}")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to assign the sum")
                                sys.exit(1)
                        elif token[0] == "MINUS":
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    variables[varname1[0]] -= int(token[1])
                                elif token[0] == "FLOAT":
                                    variables[varname1[0]] -= float(token[1])
                                elif token[0] == "WORD":
                                    variables[varname1[0]] -= variables.get(token[1])
                                else:
                                    print(f"Error: can't use this type to sub: {token[0]}")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to assign the sub")
                                sys.exit(1)
                        elif token[0] == "TIMES":
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    variables[varname1[0]] *= int(token[1])
                                elif token[0] == "FLOAT":
                                    variables[varname1[0]] *= float(token[1])
                                elif token[0] == "WORD":
                                    variables[varname1[0]] *= variables.get(token[1])
                                else:
                                    print(f"Error: can't use this type to multiply: {token[0]}")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to assign the mul")
                                sys.exit(1)
                        elif token[0] == "DIVIDE":
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    variables[varname1[0]] /= int(token[1])
                                elif token[0] == "FLOAT":
                                    variables[varname1[0]] /= float(token[1])
                                elif token[0] == "WORD":
                                    variables[varname1[0]] /= variables.get(token[1])
                                else:
                                    print(f"Error: can't use this type to div: {token[0]}")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to assign the div")
                                sys.exit(1)
                        elif token[0] == "EQUALS":
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    returned.append(variables[varname1[0]] == int(token[1]))
                                elif token[0] == "FLOAT":
                                    returned.append(variables[varname1[0]] == float(token[1]))
                                elif token[0] == "WORD":
                                    returned.append(variables[varname1[0]] == variables.get(token[1]))
                                elif token[0] == "STRING":
                                    returned.append(variables[varname1[0]] == token[1].replace("\"", "").replace("\\n", "\n"))
                                else:
                                    print(f"Error: can't use this type to '==': {token[0]}")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to assign the '=='")
                                sys.exit(1)
                        elif token[0] == "EQUALS":
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    returned.append(variables[varname1[0]] == int(token[1]))
                                elif token[0] == "FLOAT":
                                    returned.append(variables[varname1[0]] == float(token[1]))
                                elif token[0] == "WORD":
                                    returned.append(variables[varname1[0]] == variables.get(token[1]))
                                elif token[0] == "STRING":
                                    returned.append(variables[varname1[0]] == token[1].replace("\"", "").replace("\\n", "\n"))
                                else:
                                    print(f"Error: can't use this type to '==': {token[0]}")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to assign the '=='")
                                sys.exit(1)
                        elif token[0] == "EQUALS":
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    returned.append(variables[varname1[0]] == int(token[1]))
                                elif token[0] == "FLOAT":
                                    returned.append(variables[varname1[0]] == float(token[1]))
                                elif token[0] == "WORD":
                                    returned.append(variables[varname1[0]] == variables.get(token[1]))
                                elif token[0] == "STRING":
                                    returned.append(variables[varname1[0]] == token[1].replace("\"", "").replace("\\n", "\n"))
                                else:
                                    print(f"Error: can't use this type to '==': {token[0]}")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to assign the '=='")
                                sys.exit(1)
                        elif token[0] == "EQUALS":
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    returned.append(variables[varname1[0]] == int(token[1]))
                                elif token[0] == "FLOAT":
                                    returned.append(variables[varname1[0]] == float(token[1]))
                                elif token[0] == "WORD":
                                    returned.append(variables[varname1[0]] == variables.get(token[1]))
                                elif token[0] == "STRING":
                                    returned.append(variables[varname1[0]] == token[1].replace("\"", "").replace("\\n", "\n"))
                                else:
                                    print(f"Error: can't use this type to '==': {token[0]}")
                                    sys.exit(1)
                            elif token[0] == "GREATERTHAN":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    returned.append(variables[varname1[0]] >= int(token[1]))
                                elif token[0] == "FLOAT":
                                    returned.append(variables[varname1[0]] >= float(token[1]))
                                elif token[0] == "WORD":
                                    returned.append(variables[varname1[0]] >= variables.get(token[1]))
                                else:
                                    print(f"Error: can't use this type to '=>': {token[0]}")
                                    sys.exit(1)
                            elif token[0] == "LOWERTHAN":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    returned.append(variables[varname1[0]] <= int(token[1]))
                                elif token[0] == "FLOAT":
                                    returned.append(variables[varname1[0]] <= float(token[1]))
                                elif token[0] == "WORD":
                                    returned.append(variables[varname1[0]] <= variables.get(token[1]))
                                else:
                                    print(f"Error: can't use this type to '=<': {token[0]}")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to assign the '==' and '>' to assign the '=>' and '<' to '=<'")
                                sys.exit(1)
                        elif token[0] == "GREATERTHAN":
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "INT":
                                returned.append(variables[varname1[0]] > int(token[1]))
                            elif token[0] == "FLOAT":
                                returned.append(variables[varname1[0]] > float(token[1]))
                            elif token[0] == "WORD":
                                returned.append(variables[varname1[0]] > variables.get(token[1]))
                            else:
                                print(f"Error: can't use this type to '>': {token[0]}")
                                sys.exit(1)
                        elif token[0] == "LOWERTHAN":
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "INT":
                                returned.append(variables[varname1[0]] < int(token[1]))
                            elif token[0] == "FLOAT":
                                returned.append(variables[varname1[0]] < float(token[1]))
                            elif token[0] == "WORD":
                                returned.append(variables[varname1[0]] < variables.get(token[1]))
                            else:
                                print(f"Error: can't use this type to '<': {token[0]}")
                                sys.exit(1)
                        else:
                            print("Error: Can't do this operation!")
                            sys.exit(1)
                    elif token[1] == "returned":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token[0] == "LPAREN":
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "RPAREN":
                                print(returned)
                            else:
                                print("Error: can't add arguments to 'returned()'")
                                sys.exit(1)
                        else:
                            print("Error: use '(' to start calling 'returned()'")
                            sys.exit(1)
                    elif token[1] == "if":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token[0] == "WORD":
                            if returned.pop():
                                Execute(" ".join(functions[token[1]]["code"])).execute2()
                        else:
                            print("Error: use an function name (using an word) to execute if")
                    elif token[1] == "KEY":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1

                        key_mapping = {
                            "A": pygame.K_a,
                            "B": pygame.K_b,
                            "C": pygame.K_c,
                            "D": pygame.K_d,
                            "E": pygame.K_e,
                            "F": pygame.K_f,
                            "G": pygame.K_g,
                            "H": pygame.K_h,
                            "I": pygame.K_i,
                            "J": pygame.K_j,
                            "K": pygame.K_k,
                            "L": pygame.K_l,
                            "M": pygame.K_m,
                            "N": pygame.K_n,
                            "O": pygame.K_o,
                            "P": pygame.K_p,
                            "Q": pygame.K_q,
                            "R": pygame.K_r,
                            "S": pygame.K_s,
                            "T": pygame.K_t,
                            "U": pygame.K_u,
                            "V": pygame.K_v,
                            "W": pygame.K_w,
                            "X": pygame.K_x,
                            "Y": pygame.K_y,
                            "Z": pygame.K_z,
                            "0": pygame.K_0,
                            "1": pygame.K_1,
                            "2": pygame.K_2,
                            "3": pygame.K_3,
                            "4": pygame.K_4,
                            "5": pygame.K_5,
                            "6": pygame.K_6,
                            "7": pygame.K_7,
                            "8": pygame.K_8,
                            "9": pygame.K_9,
                            "SPACE": pygame.K_SPACE,
                            "ESC": pygame.K_ESCAPE,
                            "LEFT": pygame.K_LEFT,
                            "RIGHT": pygame.K_RIGHT,
                            "UP": pygame.K_UP,
                            "DOWN": pygame.K_DOWN,
                            "RETURN": pygame.K_RETURN,
                            "TAB": pygame.K_TAB,
                            "BACKSPACE": pygame.K_BACKSPACE,
                            "LSHIFT": pygame.K_LSHIFT,
                            "RSHIFT": pygame.K_RSHIFT,
                            "LCTRL": pygame.K_LCTRL,
                            "RCTRL": pygame.K_RCTRL,
                            "LALT": pygame.K_LALT,
                            "RALT": pygame.K_RALT,
                            "F1": pygame.K_F1,
                            "F2": pygame.K_F2,
                            "F3": pygame.K_F3,
                            "F4": pygame.K_F4,
                            "F5": pygame.K_F5,
                            "F6": pygame.K_F6,
                            "F7": pygame.K_F7,
                            "F8": pygame.K_F8,
                            "F9": pygame.K_F9,
                            "F10": pygame.K_F10,
                            "F11": pygame.K_F11,
                            "F12": pygame.K_F12
                        }

                        if token[0] == "WORD" and token[1] in key_mapping:
                            key = key_mapping[token[1]]
                            if keys[key]:
                                returned.append(True)
                            else:
                                returned.append(False)
                    elif token[1] == "Vector2":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token[0] == "WORD":
                            self.varname = token[1]
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    n1 = int(token[1])
                                    token = tokens[tokenpos - 1]
                                    tokenpos += 1
                                    if token[0] == "INT":
                                        variables[self.varname] = (n1, int(token[1]))
                                    elif token[0] == "WORD":
                                        variables[self.varname] = (n1, variables.get(token[1]))
                                    else:
                                        print("Error: to create Vector2 variables, use integer values or variable names values(part2)")
                                        sys.exit(1)
                                elif token[0] == "WORD":
                                    n1 = variables.get(token[1])
                                    token = tokens[tokenpos - 1]
                                    tokenpos += 1
                                    if token[0] == "INT":
                                        variables[self.varname] = (n1, int(token[1]))
                                    elif token[0] == "WORD":
                                        variables[self.varname] = (n1, variables.get(token[1]))
                                    else:
                                        print("Error: to create Vector2 variables, use integer values or variable names values (part2)")
                                        sys.exit(1)
                                else:
                                    print("Error: to create Vector2 variables, use integer values or variable names values (part1)")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to atribute variables values")
                                sys.exit(1)
                        else:
                            print(f"Error: Use normal word to set variables name. used type: {token[0]}")
                            sys.exit(1)
                    elif token[1] == "Rgb":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token[0] == "WORD":
                            self.varname = token[1]
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "INT":
                                    n1 = int(token[1])
                                    token = tokens[tokenpos - 1]
                                    tokenpos += 1
                                    if token[0] == "INT":
                                        n2 = int(token[1])
                                        token = tokens[tokenpos - 1]
                                        tokenpos += 1
                                        if token[0] == "INT":
                                            variables[self.varname] = (n1, n2, int(token[1]))
                                        else:
                                            print("Error: to create Rgb variables, use integer values (part3)")
                                            sys.exit(1)
                                    else:
                                        print("Error: to create Rgb variables, use integer values (part2)")
                                        sys.exit(1)
                                else:
                                    print("Error: to create Rgb variables, use integer values (part1)")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to atribute variables values")
                                sys.exit(1)
                        else:
                            print(f"Error: Use normal word to set variables name. used type: {token[0]}")
                            sys.exit(1)
                    elif token[1] == "Rect":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token[0] == "WORD":
                            self.varname = token[1]
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "EQUALS":
                                token = tokens[tokenpos - 1]
                                tokenpos += 1
                                if token[0] == "WORD":
                                    var1 = variables.get(token[1])
                                    token = tokens[tokenpos - 1]
                                    tokenpos += 1
                                    if token[0] == "WORD":
                                        rects[self.varname] = pygame.Rect(var1, variables.get(token[1]))
                                    else:
                                        print("Error: to create Rect variables, use variable names values (part2)")
                                        sys.exit(1)
                                else:
                                    print("Error: to create Rect variables, use variable names values (part1)")
                                    sys.exit(1)
                            else:
                                print("Error: use '=' to atribute variables values")
                                sys.exit(1)
                        else:
                            print(f"Error: Use normal word to set variables name. used type: {token[0]}")
                            sys.exit(1)
                    elif token[1] == "DrawRect":
                        token = tokens[tokenpos - 1]
                        tokenpos += 1
                        if token[0] == "WORD":
                            colorvarname = variables.get(token[1])
                            token = tokens[tokenpos - 1]
                            tokenpos += 1
                            if token[0] == "WORD":
                                pygame.draw.rect(screen, colorvarname, rects.get(token[1]))
                            else:
                                print("Error: use normal words and use rect variables name to draw your rect")
                                sys.exit(1)
                        else:
                            print("Error: use normal words and use variables name to set rect color.")
                            sys.exit(1)
                    else:
                        print(f"Error: Unknown keyword: {token[1]}")
                        sys.exit(1)
                elif token[0] == "EXCLAMATION":
                    self.in_comment = True
                elif token[0] == "NEWLINE":
                    pass
                else:
                    print(f"Error: unknown token type: ({token[0]}, {token[1]})")
                    sys.exit(1)
            elif self.in_show:
                if not self.in_args:
                    if token[0] == "LPAREN":
                        self.in_args = True
                        self.new_arg = True
                        showargs.clear()
                    else:
                        print("Error: use '(' to start printing things.")
                elif self.in_args:
                    if self.new_arg:
                        if token[0] == "STRING":
                            showargs.append(token[1].replace("\"", "").replace("\\n", "\n"))
                            self.new_arg = False
                        elif token[0] == "INT":
                            showargs.append(int(token[1]))
                            self.new_arg = False
                        elif token[0] == "FLOAT":
                            showargs.append(float(token[1]))
                            self.new_arg = False
                        elif token[0] == "WORD":
                            showargs.append(variables.get(token[1]))
                            self.new_arg = False
                        elif token[0] == "RPAREN":
                            self.in_show = False
                            self.in_args = False
                            self.new_arg = False
                        elif token[0] == "COMMA":
                            pass
                        else:
                            print("Error: you can only use strings, integers, floats and variables")
                            sys.exit(1)
                    elif not self.new_arg:
                        if token[0] == "COMMA":
                            self.new_arg = True
                        elif token[0] == "RPAREN":
                            self.in_show = False
                            self.in_args = False
                            for msg in showargs:
                                print(msg, end="")
                            print()
                        else:
                            print("Error: you can only use ',' to add more arguments and ')' to stop the arguments")
                            sys.exit(1)
            elif self.in_call:
                if self.in_args:
                    if self.new_arg:
                        if token[0] == "STRING":
                            funcargs.append(token[1].replace("\"", "").replace("\\n", "\n"))
                            self.new_arg = False
                        elif token[0] == "WORD":
                            funcargs.append(variables.get(token[1]))
                            self.new_arg = False
                        elif token[0] == "INT":
                            funcargs.append(int(token[1]))
                            self.new_arg = False
                        elif token[0] == "FLOAT":
                            funcargs.append(float(token[1]))
                            self.new_arg = False
                        elif token[0] == "RPAREN":
                            Execute(" ".join(functions.get(self.funcname)["code"])).execute2()
                            self.new_arg = False
                            self.in_args = False
                            self.in_call = False
                        else:
                            print("Error: you can only use strings, integers, floats and variables")
                            sys.exit(1)
                    elif not self.new_arg:
                        if token[0] == "COMMA":
                            self.new_arg = True
                        elif token[0] == "RPAREN":
                            for i, arg in enumerate(funcargs):
                                variables[functions[self.funcname]["params"][i]] = arg
                            Execute(" ".join(functions.get(self.funcname)["code"])).execute2()
                            self.new_arg = False
                            self.in_args = False
                            self.in_call = False
                        else:
                            print("Error: you can only use ',' to add more arguments and ')' to stop the arguments")
                            sys.exit(1)
                elif not self.in_args:
                    if token[0] == "LPAREN":
                        self.in_args = True
                        self.new_arg = True
                    else:
                        print("Error: use '(' to start arguments or to start function calling")
                        sys.exit(1)
            elif self.in_comment:
                if token[0] == "SEMICOLON":
                    self.in_comment = False

def tokenize(expr):
    patterns = [
        (r'STRING', r'"([^"\\]*(\\.[^"\\]*)*)"'),
        (r'FLOAT', r'\d+\.\d+'),
        (r'INT', r'\d+'),
        (r'PLUS', r'\+'),
        (r'MINUS', r'\-'),
        (r'TIMES', r'\*'),
        (r'DIVIDE', r'/'),
        (r'LPAREN', r'\('),
        (r'RPAREN', r'\)'),
        (r'LBRACKET', r'{'),
        (r'RBRACKET', r'}'),
        (r'COMMA', r','),
        (r'WORD', r'\w+'),
        (r'EQUALS', r'='),
        (r'LOWERTHAN', r'<'),
        (r'GREATERTHAN', r'>'),
        (r'EXCLAMATION', r'!'),
        (r'SEMICOLON', r';'),
        (r'NEWLINE', r'\n'),
        (r'WS', r'\s+'),
    ]
    
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns)
    
    tokens = []
    for match in re.finditer(token_regex, expr):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type != 'WS':
            tokens.append((token_type, token_value))

    return tokens

if __name__ == "__main__":
    version = "beta 1.0"
    if len(sys.argv) < 2:
        print(f"Lasun programming language version: {version}")
        print(f"Usage: {sys.argv[0]} <file>")
    else:
        if sys.argv[1].endswith(".lasun"):
            with open(sys.argv[1], "r") as f:
                Execute(f.read()).execute1()
                screen = pygame.display.set_mode((variables["width"], variables["height"]))
                pygame.display.set_caption(variables["windowname"])

                bgcolor = (variables["bgR"], variables["bgG"], variables["bgB"])
                print("Background color (bg):", bgcolor)

                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                            sys.exit()
                            
                    screen.fill(bgcolor)

                    Execute(" ".join(functions["run"]["code"])).execute2()
                    pygame.display.flip()
        else:
            print("Error: Use .lasun file extension")
            sys.exit(1)
