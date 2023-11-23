symbol = ["if", "else", "void", "int", "while", "break","return"]
symbol_table = []
token_table = []
lexical_error = []



def concat(A,B):
    return(str('('+ A + ', '+ B +')'))



def error(line_number,type,token):
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


def write_tokens():
     input = open('tokens.txt','w')
     for i in range(len(token_table)):
        if i == 0:
            input.write(str(token_table[i]['line_number'])+'.'+'\t'+concat(token_table[i]['type'],token_table[i]['token']))
        elif token_table[i]['line_number'] == token_table[i]['line_number']:
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
            elif lexical_error[i]['line_number'] == lexical_error[i]['line_number']:
                input.write(' '+concat(lexical_error[i]['type'],lexical_error[i]['token']))
            else:
                input.write('\n'+str(lexical_error[i]['line_number'])+".\t"+concat(lexical_error[i]['token'],lexical_error[i]['type']))

     input.close()
             
             
def write_symbol_table():
    count = 1
    input = open('symbol_table.txt','w')
    for i in symbol:
        input.write(str(count)+'.\t'+i+'\n')
        count += 1

    for i in symbol_table:
        input.write(str(count)+'.\t'+i+'\n')
        count += 1

    input.close()


lexical_error.append(
     {
            'type': 'id',
            'token': 'aaaaa',
            'line_number': 12 
     }
)

lexical_error.append(
     {
            'type': 'vvvvv',
            'token': 'keyword',
            'line_number': 14 
     }
)


write_lexical_errors()





