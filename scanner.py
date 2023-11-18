class TokenType:
    NUM = "NUM"
    ID = "ID"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    EOF = "EOF"

class scanner:
    def __init__(self,input_file):
        self.input = open(input_file,'r')
        self.lines = self.input.readlines()
        self.keyword = {'if', 'else', 'void', 'int', 'while', 'break','return'}
        self.symbols = {';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<'}
        self.whitespaces = {' ', '\n', '\r', '\t', '\v', '\f'}
        self.line_number = 0
        self.position = 0
        self.current_char = ''
        self.next_char = ''

    def get_next_char(self):
        next_char == None
        return

        
    def get_next_token(self):
        if self.current_char in self.whitespaces:
            self.get_next_char


    def run(self):
        while True:
            token = self.get_next_token
            if token == None:
                EOF_reached()
                break
            
            if self.position >= len(self.lines):
                break
            
                








###################################################
###################################################
###################################################
###################################################
###################################################



