class Scanner:
    def __init__(self, input_name):
        self.mat = [dict() for _ in range(16)]
        self.oth = [0] * 16
        self.mark = [False] * 16
        self.term = [False] * 16
        self.have_star = [False] * 16
        self.message = [''] * 16
        self.symbols_list = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"]
        self.valid_chars = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<', '/', ' ', '\n', '\t']
        self.keywords = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return",
                         "continue"]

        self.current_state = 0
        self.current_string = ""
        self.tk_counter = 1
        self.in_comment_all = False
        self.last_comment_line = -1
        self.lexical_errors = [list() for _ in range(10000)]
        self.in_comment_line = False
        self.tokens = [list() for _ in range(10000)]
        self.all_tokens = list()
        self.new_tokens = list()

        self.input_file = open(input_name, 'r')

    def close(self):
        self.input_file.close()

    def init_states(self):
        self.mat[0]["letter"] = 1
        self.mat[0]["digit"] = 3
        self.mat[0][";"] = 5
        self.mat[0][":"] = 5
        self.mat[0][","] = 5
        self.mat[0]["["] = 5
        self.mat[0]["]"] = 5
        self.mat[0]["("] = 5
        self.mat[0][")"] = 5
        self.mat[0]["{"] = 5
        self.mat[0]["}"] = 5
        self.mat[0]["+"] = 5
        self.mat[0]["-"] = 5
        self.mat[0]["<"] = 5
        self.mat[0]["="] = 6
        self.mat[0]["*"] = 8
        self.mat[0]["/"] = 10
        self.mat[0][" "] = 15
        self.mat[0]["\n"] = 15
        self.mat[0]["\t"] = 15
        self.mat[0]["\r"] = 15
        self.mat[0]["\f"] = 15
        self.mat[0]["\v"] = 15
        self.oth[0] = -1
        self.message[0] = "Invalid input"

        self.mat[1]["letter"] = 1
        self.mat[1]["digit"] = 1
        self.oth[1] = 2

        self.term[2] = True
        self.mark[2] = True
        self.have_star[2] = True

        self.mat[3]["digit"] = 3
        self.mat[3]["letter"] = -1
        self.oth[3] = 4
        self.message[3] = "Invalid number"

        self.term[4] = True
        self.mark[4] = True
        self.have_star[4] = True

        self.term[5] = True

        self.mat[6]["="] = 7
        self.oth[6] = 9

        self.term[7] = True

        self.mat[8]["/"] = -1
        self.oth[8] = 9
        self.message[8] = "Unmatched comment"

        self.term[9] = True
        self.mark[9] = True
        self.have_star[9] = True

        self.mat[10]["/"] = 11
        self.mat[10]["*"] = 13
        self.oth[10] = -1
        self.message[10] = "Invalid input"

        self.mat[11]["\n"] = 12
        self.oth[11] = 11

        self.term[12] = True

        self.mat[13]["*"] = 14
        self.oth[13] = 13

        self.mat[14]["/"] = 12
        self.mat[14]["*"] = 14
        self.oth[14] = 13

        self.term[15] = True

    def find_type(self, char):
        if ('a' <= char <= 'z') or ('A' <= char <= 'Z'):
            return "letter"

        if '0' <= char <= '9':
            return "digit"

        if char in self.valid_chars:
            return char

        return '!'

    def is_in_keyword(self, string):
        return string in self.keywords

    def process_next_char(self, c):
        if c == '\n':
            if not self.in_comment_all:
                self.current_state = 0  #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

            self.tk_counter = self.tk_counter + 1
            self.in_comment_line = False

        fin = False

        while not fin:
            fin = True

            in_comment = False
            if self.current_state == 11 or self.current_state == 13:
                in_comment = True

            self.current_string = self.current_string + c

            t = self.find_type(c)
            if not self.in_comment_all and not self.in_comment_line and t == '!':
                if self.current_string[0:-1] == "/":
                    if len(self.current_string[0:-1]) > 0:
                        self.lexical_errors[self.tk_counter].append(
                            "(" + self.current_string[0:-1] + ", " + "Invalid input" + ") ")
                    self.lexical_errors[self.tk_counter].append("(" + c + ", " + "Invalid input" + ") ")
                    self.current_state = 0
                    self.current_string = ""
                else:
                    self.lexical_errors[self.tk_counter].append(
                        "(" + self.current_string + ", " + "Invalid input" + ") ")
                    self.current_state = 0
                    self.current_string = ""
            elif t in self.mat[self.current_state]:
                if self.mat[self.current_state][t] == -1:
                    if c == ' ' or c == '\n' or c == '\t':
                        self.current_string = self.current_string[0: -1]
                    self.lexical_errors[self.tk_counter].append(
                        "(" + self.current_string + ", " + self.message[self.current_state] + ") ")

                self.current_state = self.mat[self.current_state][t]
            else:
                if self.oth[self.current_state] == -1 and self.current_state == 10:
                    fin = False
                    self.current_string = self.current_string[0: -1]
                    self.lexical_errors[self.tk_counter].append(
                        "(" + self.current_string + ", " + self.message[self.current_state] + ") ")
                elif self.oth[self.current_state] == -1:
                    if c == ' ' or c == '\n' or c == '\t':
                        self.current_string = self.current_string[0: -1]
                    self.lexical_errors[self.tk_counter].append(
                        "(" + self.current_string + ", " + self.message[self.current_state] + ") ")

                self.current_state = self.oth[self.current_state]
                if self.current_state == -1:
                    self.current_state = 0
                    self.current_string = ""

            if self.current_state == 11:
                self.in_comment_line = True
                if not in_comment:
                    self.last_comment_line = self.tk_counter

            if self.current_state == 13:
                self.in_comment_all = True
                if not in_comment:
                    self.last_comment_line = self.tk_counter

            if self.term[self.current_state]:
                if self.have_star[self.current_state]:
                    fin = False
                    self.current_string = self.current_string[0: -1]

                if self.current_state == 2:
                    flag = False
                    for s in self.symbols_list:
                        if s == self.current_string:
                            flag = True

                    if not self.is_in_keyword(self.current_string) and not flag:
                        self.symbols_list.append(self.current_string)

                    if self.is_in_keyword(self.current_string):
                        self.add_token("KEYWORD", self.current_string)
                    else:
                        self.add_token("ID", self.current_string)

                elif self.current_state == 4:
                    self.add_token("NUM", self.current_string)
                elif self.current_state == 5 or self.current_state == 7 or self.current_state == 9:
                    self.add_token("SYMBOL", self.current_string)

                elif self.current_state == 12:
                    self.in_comment_all = False
                    self.in_comment_line = False

                self.current_state = 0
                self.current_string = ""

    def get_next_token(self):
        if self.new_tokens:
            p1, p2 = self.new_tokens[0]
            if p1 in {'KEYWORD', 'SYMBOL'}:
                p1, p2 = p2, p1
            self.new_tokens.pop(0)
            return p1, p2

        while True:
            char = self.input_file.read(1)
            if char == '$' or char == '':
                return '$', 'END OF FILE'

            self.process_next_char(char)

            if self.new_tokens:
                p1, p2 = self.new_tokens[0]
                if p1 in {'KEYWORD', 'SYMBOL'}:
                    p1, p2 = p2, p1
                self.new_tokens.pop(0)
                return p1, p2

    def add_token(self, token_type, string):
        self.all_tokens.append((token_type, string))
        self.new_tokens.append(self.all_tokens[-1])
        self.tokens[self.tk_counter].append((token_type, string))

    def write_tokens(self, file_name):
        with open(file_name, 'w') as f:
            for line_id in range(10000):
                if not self.tokens[line_id]:
                    continue
                f.write(str(line_id) + '.\t')
                f.write(' '.join(f'({token_type}, {string})' for token_type, string in self.tokens[line_id]))
                f.write('\n')

    def write_lexical_errors(self, file_name):
        if self.current_state == 11 or self.current_state == 13:
            self.lexical_errors[self.last_comment_line].append(
                "(" + self.current_string[:7] + "..., " + "Unclosed comment) ")

        with open(file_name, 'w') as LE:
            flag = False
            for i in range(10000):
                if len(self.lexical_errors[i]) == 0:
                    continue

                flag = True
                LE.write(str(i) + ".\t")
                LE.write(' '.join(s[0: -1] for s in self.lexical_errors[i]))
                LE.write('\n')

            if not flag:
                LE.write("There is no lexical error.")

    def write_symbol_table(self, file_name):
        with open(file_name, 'w') as ST:
            st_counter = 0
            for s in self.symbols_list:
                st_counter += 1
                ST.write(str(st_counter) + ".\t" + s + '\n')






###################################################
###################################################
###################################################
###################################################
###################################################


import json
from collections import defaultdict

from anytree import RenderTree

from parse_tools import Parser

symbol_table = dict()  # only keys are used for now
lexical_errors = defaultdict(list)  # {line_no: [lexeme, error_type]}
semantic_errors = []
tokens = defaultdict(list)  # {line_no: [(type, lexeme),]}

first = dict()  # {T: [First(T)]}
follow = dict()  # {T: [Follow(T)]}
predict = dict()  # {No: [First(Prod(No))]}
productions = dict()  # {T: [prod numbers]}
grammar = dict()  # {No: Prod}


class TokenType:
    SYMBOL = 'SYMBOL'
    NUM = 'NUM'
    ID = 'ID'
    KEYWORD = 'KEYWORD'
    COMMENT = 'COMMENT'
    WHITESPACE = 'WHITESPACE'
    ID_OR_KEYWORD = 'ID_OR_KEYWORD'
    INVALID = 'Invalid input'
    DOLLAR = '$'
    EPSILON = 'EPSILON'


def get_symbol_table_from_id(id):
    for i in symbol_table['ids']:
        if i[0] == id:
            return i


def get_token_type(char):
    if char in [' ', '\t', '\n', '\r', '\v', '\f']:  # WHITESPACE
        return TokenType.WHITESPACE
    elif char in [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<']:  # SYMBOL
        return TokenType.SYMBOL
    elif char.isdigit():  # NUM
        return TokenType.NUM
    elif char.isalnum():  # ID / KEYWORD
        return TokenType.ID_OR_KEYWORD
    elif char == '/':  # COMMENT (potentially)
        return TokenType.COMMENT
    else:  # Invalid input
        return TokenType.INVALID


def init_symbol_table():
    symbol_table.update(
        {'keywords': ['if', 'else', 'void', 'int', 'while', 'break', 'switch',
                      'default', 'case', 'return', 'for'],
         'ids': []})


def save_lexical_errors():
    with open('lexical_errors.txt', 'w') as f:
        if lexical_errors:
            f.write('\n'.join([f'{line_no + 1}.\t' + ' '.join([f'({err[0]}, {err[1]})' for err in line_errors])
                               for line_no, line_errors in lexical_errors.items()]))
        else:
            f.write('There is no lexical error.')


def save_symbol_table():
    with open('symbol_table.txt', 'w') as f:
        f.write('\n'.join(
            [f'{idx + 1}.\t{symbol}' for idx, symbol in enumerate(symbol_table['keywords'] + symbol_table['ids'])]))


def save_tokens():
    with open('tokens.txt', 'w') as f:
        f.write('\n'.join([f'{line_no + 1}.\t' + ' '.join([f'({token[0]}, {token[1]})' for token in line_tokens])
                           for line_no, line_tokens in tokens.items()]))


def save_syntax_errors(parser: Parser):
    with open('syntax_errors.txt', 'w') as f:
        if not parser.syntax_errors:
            f.write('There is no syntax error.\n')
        else:
            f.write('\n'.join(error for error in parser.syntax_errors))







def save_semantic_errors():
    with open('semantic_errors.txt', 'w') as f:
        for idx in semantic_errors:
            f.write(f'{idx}\n')
    with open('output.txt', 'w') as f:
        f.write('The code has not been generated.')


def save_program(code_gen):
    with open('output.txt', 'w') as f:
        for idx in sorted(code_gen.PB.keys()):
            f.write(f'{idx}\t{code_gen.PB[idx]}\n')












from utils import *


def get_from_table(name):
    if name in symbol_table['keywords']:
        return TokenType.KEYWORD
    else:
        if name not in symbol_table['ids']:
            # symbol_table['ids'].append(name)
            pass
        return TokenType.ID


def get_short_comment(comment):
    return comment[:7] + '...' if len(comment) >= 7 else comment


class Scanner:
    def __init__(self, input_path):
        init_symbol_table()

        self.input_path = input_path
        self.lines = None
        self.read_input()

        self.line_number = 1
        self.cursor = 0

    def read_input(self):
        with open(self.input_path, 'r') as f:
            self.lines = ''.join([line for line in f.readlines()])

    def get_next_token(self):
        if self.eof_reached():
            return self.line_number, TokenType.DOLLAR, '$'

        char = self.get_current_char()
        token_type = get_token_type(char)

        if token_type == TokenType.WHITESPACE:
            if char == '\n':
                self.line_number += 1
            self.cursor += 1
            return self.get_next_token()

        elif token_type == TokenType.SYMBOL:
            if char == '=':
                if self.cursor < len(self.lines) - 1 \
                        and self.lines[self.cursor + 1] == '=':
                    self.cursor += 2
                    return self.line_number, TokenType.SYMBOL, '=='
            elif char == '*':
                if self.cursor < len(self.lines) - 1 \
                        and self.lines[self.cursor + 1] == '/':
                    self.cursor += 2
                    lexical_errors[self.line_number].append(('*/', 'Unmatched comment'))
                    return False
            self.cursor += 1
            return self.line_number, TokenType.SYMBOL, char

        elif token_type == TokenType.NUM:
            number, has_error = self.number_token()
            if not has_error:
                return self.line_number, TokenType.NUM, number
            lexical_errors[self.line_number].append((number, 'Invalid number'))

        elif token_type == TokenType.ID_OR_KEYWORD:
            name, has_error = self.find_id_or_keyword()
            if not has_error:
                return self.line_number, get_from_table(name), name
            lexical_errors[self.line_number].append((name, 'Invalid input'))

        elif token_type == TokenType.COMMENT:
            self.find_comment()

        elif token_type == TokenType.INVALID:
            lexical_errors[self.line_number].append((char, 'Invalid input'))
            self.cursor += 1

    def find_comment(self):
        beginning_line_number = self.line_number

        lexeme = self.get_current_char()
        if self.cursor + 1 == len(self.lines):
            lexical_errors[self.line_number].append((lexeme, 'Invalid input'))  # last char is /
            self.cursor += 1
            return None, True

        next_char = self.lines[self.cursor + 1]
        if next_char not in ['/', '*']:
            lexical_errors[self.line_number].append(
                (lexeme + (next_char if next_char != '\n' else ''), 'Invalid input'))  # /
            if next_char == '\n':  # Pure tof to fix the minor bug
                self.line_number += 1
            self.cursor += 2
            return None, True

        is_multiline = next_char == '*'

        while self.cursor + 1 < len(self.lines):
            self.cursor += 1
            temp_char = self.get_current_char()

            if temp_char == '\n' and not is_multiline:
                self.line_number += 1
                break
            if is_multiline:
                if self.cursor + 1 < len(self.lines):
                    if temp_char == '*' and self.lines[self.cursor + 1] == '/':
                        self.cursor += 2
                        return lexeme + '*/', False
                else:
                    lexeme += self.lines[-1]
                    self.cursor += 1
                    lexical_errors[beginning_line_number].append((get_short_comment(lexeme), 'Unclosed comment'))
                    return None, True

            if temp_char == '\n':
                self.line_number += 1
            lexeme += temp_char

        self.cursor += 1
        return lexeme, False

    def get_current_char(self):
        return self.lines[self.cursor]

    def find_id_or_keyword(self):
        name = self.get_current_char()
        while self.cursor + 1 < len(self.lines):
            self.cursor += 1
            temp_char = self.get_current_char()
            temp_type = get_token_type(temp_char)

            if temp_type == TokenType.NUM or temp_type == TokenType.ID_OR_KEYWORD:
                name += temp_char
            elif temp_type == TokenType.WHITESPACE or temp_type == TokenType.SYMBOL:
                return name, False
            else:
                name += temp_char
                self.cursor += 1
                return name, True

        self.cursor += 1
        return name, False

    def number_token(self):
        num = self.get_current_char()
        while self.cursor + 1 < len(self.lines):
            self.cursor += 1
            temp_char = self.get_current_char()
            temp_type = get_token_type(temp_char)

            if temp_type == TokenType.NUM:
                num += temp_char
            elif temp_type == TokenType.WHITESPACE or temp_type == TokenType.SYMBOL:
                return num, False
            else:
                num += temp_char
                self.cursor += 1
                return num, True

        self.cursor += 1
        return num, False

    def read_all_tokens(self):
        while True:
            if self.eof_reached():
                break
            token = self.get_next_token()
            if token:
                tokens[token[0]].append(token[1:])

    def eof_reached(self):
        return self.cursor >= len(self.lines)
