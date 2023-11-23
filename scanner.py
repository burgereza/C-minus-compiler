SYMBOL = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=','==', '<', '/' ]
KEYWORDS = ["if", "else", "void", "int", "while", "break","return"]
WHITESPACE=[' ', '\t', '\n', '\r', '\v', '\f']
symbol_table = []
token_table = []
lexical_error = []


def concat(A, B):
    return(str('('+ str(A) + ', '+ str(B) +')'))
        

def add_symbol(chars):
    if chars not in symbol_table and chars not in KEYWORDS:
        symbol_table.append(chars)

def error(line_number, type,token):
        error_info = {
            'type': type,
            'token': token,
            'line_number':  line_number 
        }
        lexical_error.append(error_info)


def tokens(line_number,type,token):
        token_info = {
            'type': type,
            'token': token,
            'line_number':  line_number 
        }
        token_table.append(token_info)

def check (type,token,massage,line_number):
    if type == 'ID' or type == 'KEYWORD':
        add_symbol(token)
    if type == 'ID' or type == 'KEYWORD' or type == 'NUM' or type == 'SYMBOL':
        tokens(line_number,type,token)
    if type == 'Error':
        error(line_number,massage,token)

def write_tokens():
    input = open('tokens.txt','w')
    for i in range(len(token_table)):
        if i == 0:
            input.write(str(token_table[i]['line_number'])+'.'+'\t'+concat(token_table[i]['type'],token_table[i]['token']))
        elif token_table[i]['line_number'] == token_table[i-1]['line_number']:
            input.write(' '+concat(token_table[i]['type'],token_table[i]['token']))
        else:
            input.write('\n'+str(token_table[i]['line_number'])+'.'+'\t'+concat(token_table[i]['type'],token_table[i]['token']))

    input.close()

def write_lexical_errors():
    input = open('lexical_errors.txt','w')
    if len(lexical_error)== 0:
        input.write('There is no lexical error.')
    else: 
        for i in range(len(lexical_error)):
            if i == 0:
                input.write(str(lexical_error[i]['line_number'])+'.'+'\t'+concat(lexical_error[i]['token'],lexical_error[i]['type']))
            elif lexical_error[i]['line_number'] == lexical_error[i-1]['line_number']:
                input.write(' '+concat(lexical_error[i]['token'],lexical_error[i]['type']))
            else:
                input.write('\n'+str(lexical_error[i]['line_number'])+".\t"+concat(lexical_error[i]['token'],lexical_error[i]['type']))

    input.close()
            
            
def write_symbol_table():
    count = 1
    input = open('symbol_table.txt','w')
    for i in KEYWORDS:
        input.write(str(count)+'.\t'+i+'\n')
        count += 1

    for i in symbol_table:
        input.write(str(count)+'.\t'+i+'\n')
        count += 1

    input.close()


def get_type(token):
       if token.isdigit():
          return 'NUM'
       elif token.isalnum():
          return 'ID_OR_KEYWORD'
       elif token == '/':
          return 'COMMENT'
       elif token in SYMBOL:
          return 'SYMBOL'
       elif token in WHITESPACE:
          return 'WHITESPACE'
       else :
          return 'UNKNOWN'



class scanner:
    def __init__(self,file_input):
      self.input = open(file_input,'r')
      self.lines = self.input.readlines()
      self.lines.append("EOF")
      self.lines[len(self.lines)-2] += '\n'
      print(self.lines)
      self.line_number = 0
      self.cursor = 0
      self.end = True
      

   
   
    def get_next_token(self):
       token_string = ''
       token_type = ''
       char_type,current_char = self.update_char()
       token_string += current_char
       #print(str(char_type) + ' ------------ ' + current_char)

       #get whitespace
       if char_type == 'WHITESPACE':
          print('@@@@@@@  get whitespace  @@@@@@@')
          if current_char == '\n': #or self.cursor < len(self.lines[self.line_number]):
             #print("cursor = " + str(self.cursor) + ' --------- ' + "line number = " + str(self.line_number) , ord(current_char))
             self.line_number += 1
             self.cursor = 0
          else:
             #print("cursor = " + str(self.cursor) + ' --------- ' + "line number = " + str(self.line_number) , ord(current_char))
             if self.cursor < len(self.lines[self.line_number]):
               self.cursor += 1
             else: self.line_number += 1
          return ' ',' ',' '

       #get number
       elif char_type == 'NUM':
          print('@@@@@@@    get number    @@@@@@@')
          while True:
            self.cursor += 1
            char_type , current_char = self.update_char()
            if char_type == 'WHITESPACE' or char_type == 'SYMBOL' or char_type == 'COMMENT':
               #end of number
               return 'NUM',token_string, ''
            elif char_type != 'NUM':
               print("char = " + current_char + " ###  char_type = " + char_type)
               #lexical error
               flag = True
               if char_type == 'UNKNOWN':
                  token_string += current_char
                  self.cursor += 1
                  flag = False
               if flag:
                  token_string += current_char 
                  return 'Error',token_string ,'Invalid number'
               else:
                  token_string += current_char
                  return 'Error',token_string ,'Invalid input'
            token_string += current_char
            #print(token_string)

       #get id or keyword
       elif char_type == 'ID_OR_KEYWORD':
          print('@@@@@@@ get id or keyword @@@@@@@')
          while True:
            self.cursor += 1
            char_type , current_char = self.update_char()
            if char_type == 'WHITESPACE' or char_type == 'SYMBOL':
               #end of identifier
               if token_string in KEYWORDS:
                  return 'KEYWORD', token_string, ''
               return 'ID', token_string , ''
            elif char_type == 'UNKNOWN':
               #lexical error
               token_string += current_char
               self.cursor += 1
               return 'Error', token_string, 'Invalid input'
            token_string += current_char
            #print(token_string)
          
       
       #get comment
       elif char_type == 'COMMENT':
          print('@@@@@@@    get COMMENT    @@@@@@@')
          self.cursor += 1
          char_type , current_char = self.update_char()
          if current_char != '*':
             print("*********")
             print(current_char)
             return 'SYMBOL', '/', ''
          else:
             unc_comm_cursor , unc_comm_line = self.cursor , self.line_number
             #comment started
             while True:
                self.cursor += 1
                char_type , current_char = self.update_char()
                if current_char == None:
                   #Error
                   self.cursor = unc_comm_cursor + 2
                   self.line_number = unc_comm_line + 2
                   return 'Error', token_string, 'Unclosed comment'
                if current_char == '*':
                   self.cursor += 1
                   char_type , current_char = self.update_char()
                   if current_char == '/':
                      self.cursor += 1
                      return 'COMMENT', '/*' + token_string + '*/', ''
                   else:
                      current_char = '*'
                      self.cursor += 1
                #token_string += current_char
          return

       #get symbol
       elif char_type == 'SYMBOL':
         print('@@@@@@@    get SYMBOL    @@@@@@@')
         self.cursor += 1
         print("cursor = " + str(self.cursor))
         char_type , current_char = self.update_char()
         if token_string == '=':
            if current_char == '=':
               token_string += current_char
               self.cursor += 1
               return 'SYMBOL', token_string, ''
            return 'SYMBOL', token_string, ''
         elif token_string == '*' and current_char == '/':
            self.cursor += 1
            return 'Error','*/' ,'Unmatched comment'
         elif char_type == 'UNKNOWN':
            #lexical error
            token_string += current_char
            self.cursor += 1
            return 'Error',token_string ,'Invalid input'
         else:
            return 'SYMBOL', token_string, 'bfdb'
            #print(token_string)
         
      #get unkown
       elif char_type == 'UNKNOWN':
          self.cursor += 1
          return 'Error',token_string ,'Invalid input'
       #print(token_string + '\n')
       #return token_type , token_string
    

    def update_char(self):
      current_char = self.lines[self.line_number][self.cursor]
      char_type = get_type(current_char)
      return char_type, current_char
       

    def run(self):
       #index = 0
       while self.line_number < len(self.lines)-1 :#and self.cursor == len(self.lines[len(self.lines)-1])-1:
          token_type , token , Error = self.get_next_token()
          #continue
          print(str(self.line_number) + '     ' + str(len(self.lines)))
          check(token_type,token,Error,(self.line_number+1))
          #print(token+'_____'+str(self.line_number)+'_____'+ str(self.cursor)+'_____'+str(self.lines[self.line_number][(len(self.lines[self.line_number])-1)]))
          #if index == 20:
          #     break
          #  index += 1
       print('----------------------')
       write_lexical_errors()
       write_symbol_table()
       write_tokens() 

    def print_outputs(self):
       print('EOF')
       return
    
