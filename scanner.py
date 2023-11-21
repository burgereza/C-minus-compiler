SYMBOL = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=','==', '<', '/' ]
KEYWORDS = ["if", "else", "void", "int", "while", "break","return"]
WHITESPACE=[' ', '\t', '\n', '\r', '\v', '\f']



def get_type(token):
       if token.isdigit():
          return 'NUM'
       elif token.isalnum():
          return 'ID_OR_KEYWORD'
       elif token in SYMBOL:
          return 'SYMBOL'
       elif token == '/*':
          return 'COMMENT'
       elif token in WHITESPACE:
          return 'WHITESPACE'
       else :
          return 'UNKNOWN'



class scanner:
    def __init__(self,file_input):
      self.input = open(file_input,'r')
      self.lines = self.input.readlines()
      self.lines
      self.line_number = 0
      self.cursor = 0

   
   
    def get_next_token(self):
       token_string = ''
       token_type = ''
       char_type,current_char = self.update_char()
       token_string += current_char
       #print(str(char_type) + ' ------------ ' + current_char)
       #handle whitespace
       if char_type == 'WHITESPACE':
         #print('@@@@@@@ handle whitespace @@@@@@@')
         if current_char == '\n':
            self.line_number += 1
            self.cursor = 0
         else:
            self.cursor += 1

       #get number
       elif char_type == 'NUM':
          #print('@@@@@@@    get number    @@@@@@@')
          while True:
            self.cursor += 1
            char_type , current_char = self.update_char()
            if char_type == 'WHITESPACE' or char_type == 'SYMBOL':
               #end of number
               return 'NUM',token_string, ''
            elif char_type != 'NUM':
               #lexical error
               while True:
                  char_type , current_char = self.update_char()
                  if char_type == 'WHITESPACE' or char_type == 'SYMBOL':
                     break
                  token_string += current_char
                  self.cursor += 1  
               return 'NUM',token_string ,'INVALID INPUT'
            token_string += current_char
            #print(token_string)

       #get id or keyword
       elif char_type == 'ID_OR_KEYWORD':
          #print('@@@@@@@ get id or keyword @@@@@@@')
          while True:
            self.cursor += 1
            char_type , current_char = self.update_char()
            if char_type == 'WHITESPACE':
               #end of identifier
               if token_string in KEYWORDS:
                  return 'KEYWORD', token_string, ''
               return 'ID', token_string
            elif char_type == 'SYMBOL' or char_type == 'UNKNOWN':
               #lexical error
               return 'ID', token_string, 'INVALID INPUT'
            token_string += current_char
            #print(token_string)
          return
          
       
       #get symbol
       elif char_type == 'SYMBOL':
          #print('@@@@@@@    get SYMBOL    @@@@@@@')
          while True:
            self.cursor += 1
            char_type , current_char = self.update_char()
            if char_type == 'WHITESPACE' or char_type == 'ID_OR_KEYWORD' or char_type == 'NUM':
               #end of SYMBOL
               return 'SYMBOL',token_string
            elif char_type == 'UNKOWN':
               #lexical error
               while True:
                  char_type , current_char = self.update_char()
                  if char_type == 'WHITESPACE' or char_type == 'ID_OR_KEYWORD' or char_type == 'NUM':
                     break
                  token_string += current_char
                  self.cursor += 1
                  
               return 'LEXI',token_string
            
            
            token_string += current_char
            #print(token_string)
       
      
      #get comment
       elif char_type == 'COMMENT':
          return
           

       #print(token_string + '\n')
       return token_type , token_string
    

    def update_char(self):
       current_char = self.lines[self.line_number][self.cursor]
       char_type = get_type(current_char)
       return char_type, current_char

    def run(self):
       index = 0
       while True:
          token_type , token , Error = self.get_next_token()
          if token == None:
             #EOF reached
             self.print_outputs() 
             break
          #print(token+'_____'+str(self.line_number)+'_____'+ str(self.cursor)+'_____'+str(self.lines[self.line_number][(len(self.lines[self.line_number])-1)]))
          if index == 20:
             break
          index += 1

    def print_outputs(self):
       print('EOF')
       return