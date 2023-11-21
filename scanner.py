SYMBOL = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=','==', '<', '/' ]
KEYWORD = ["if", "else", "void", "int", "while", "break","return"]
WHITESPACE=[' ', '\t', '\n', '\r', '\v', '\f']


class TokenType:
    NUM = 'NUM'
    ID = 'ID'
    KEYWORD = 'KEYWORD'
    SYMBOL = 'SYMBOL'
    COMMENT = 'COMMENT'
    WHITESPACE = 'WHITESPACE'



class scanner:
    def __init__(self,file_input):
      self.input = open(file_input,'r')
      self.lines = self.input.readlines()
      self.lines
      self.line_number = 0
      self.cursor = 0

    def get_type(self,token):
       if token in KEYWORD:
          return TokenType.KEYWORD
       elif token.isdigit():
          return TokenType.NUM
       elif token.isalnum():
          return TokenType.ID
       elif token in SYMBOL:
          return TokenType.SYMBOL
       elif token == '/*':
          return TokenType.COMMENT
       else:
          return TokenType.WHITESPACE


    def get_next_token(self):
       token_string = ''
       token_type = ''
       current_char = self.lines[self.cursor]
       char_type = self.get_type(current_char)
       
       if char_type == TokenType.NUM:
          #get number
          return
       
       
       elif char_type == TokenType.ID:
          #get id or keyword
          return
       
       
       elif char_type == TokenType.SYMBOL:
          #get symbol
          return
       
       
       elif char_type == TokenType.COMMENT:
          #get comment
          return
       

       elif char_type == TokenType.WHITESPACE:
          #handle whitespace
          return
       

       #print(token_string + '\n')
       return token_type , token_string
    


    def run(self):
       while True:
          token , token_type = self.get_next_token()
          if token == None:
             self.print_outputs() 
             break


    def print_outputs(self):
       #FILL-HERE
       return