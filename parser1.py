from anytree import Node
from anytree import RenderTree
import anytree
from scanner import scanner
grammar = {
    
    'Program': [['DeclarationList','$']],
    'DeclarationList' : [['Declaration', 'DeclarationList'],['EPSILON']], 
    'Declaration' : [['DeclarationInitial',  'DeclarationPrime']],
    'DeclarationInitial' : [['TypeSpecifier', 'ID']],
    'DeclarationPrime' : [['FunDeclarationPrime'], ['VarDeclarationPrime']],
    'VarDeclarationPrime' : [[';'],['[', 'NUM', ']', ';']],  
    'FunDeclarationPrime' : [ ['(', 'Params', ')', 'CompoundStmt']],
    'TypeSpecifier': [['int'], ['void']],
    'Params': [['int', 'ID' ,'ParamPrime', 'ParamList'], ['void']],
    'ParamList': [[',', 'Param', 'ParamList'], ['EPSILON']],
    'Param': [ ['DeclarationInitial', 'ParamPrime']],
    'ParamPrime': [['[', ']'],['EPSILON']] ,
    'CompoundStmt': [['{' ,'DeclarationList', 'StatementList', '}']],
    'StatementList' :[[ 'Statement', 'StatementList'],['EPSILON']],  
    'Statement' : [['ExpressionStmt'], ['CompoundStmt'], ['SelectionStmt'], ['IterationStmt' ],['ReturnStmt']],
    'ExpressionStmt' : [['Expression', ';'], ['break', ';'], [';']],
    'SelectionStmt' : [['if', '(', 'Expression' ,')', 'Statement', 'else', 'Statement']],
    'IterationStmt' :[[ 'while', '(', 'Expression', ')', 'Statement']], 
    'ReturnStmt' :[['return', 'ReturnStmtPrime']],
    'ReturnStmtPrime':[[';'],['Expression', ';']],
    'Expression': [['SimpleExpressionZegond'], ['ID', 'B']],
    'B':[[ '=', 'Expression'], ['[', 'Expression', ']', 'H'], ['SimpleExpressionPrime']],
    'H':[[ '=', 'Expression'], ['G', 'D', 'C']],
    'SimpleExpressionZegond': [['AdditiveExpressionZegond', 'C']],
    'SimpleExpressionPrime' : [['AdditiveExpressionPrime', 'C']],
    'C': [['Relop', 'AdditiveExpression'],['EPSILON']], 
    'Relop': [['<'],['==']], 
    'AdditiveExpression': [['Term', 'D']],
    'AdditiveExpressionPrime': [['TermPrime', 'D']],
    'AdditiveExpressionZegond': [['TermZegond', 'D']],
    'D': [['Addop', 'Term', 'D'],['EPSILON']], 
    'Addop':[['+'],['-']], 
    'Term': [['SignedFactor', 'G']],
    'TermPrime': [['SignedFactorPrime', 'G']],
    'TermZegond':[['SignedFactorZegond', 'G']],
    'G':[['*', 'SignedFactor' ,'G'],['EPSILON']],
    'SignedFactor': [['+' , 'Factor'] , ['-' , 'Factor'], ['Factor']],
    'SignedFactorPrime' : [['FactorPrime']],
    'SignedFactorZegond': [['+', 'Factor'] , ['-', 'Factor'] , ['FactorZegond']],
    'Factor':[['(', 'Expression', ')'], ['ID', 'VarCallPrime'], ['NUM']],
    'VarCallPrime':[['(', 'Args', ')'], ['VarPrime']],
    'VarPrime':[['[', 'Expression', ']'],['EPSILON']], 
    'FactorPrime':[['(', 'Args', ')'],['EPSILON']],  
    'FactorZegond': [['(', 'Expression', ')'], ['NUM']],
    'Args': [['ArgList'],['EPSILON']], 
    'ArgList': [['Expression', 'ArgListPrime']],
    'ArgListPrime': [[',', 'Expression', 'ArgListPrime'],['EPSILON']]

} 

predict = {
    'Program':[['int','void','$']] ,
    'DeclarationList':[['int','void'],['ID',';','NUM','(','{','}','break','if','while','return','$']] ,
    'Declaration': [['int','void']] ,
    'DeclarationInitial' : [['int','void']] ,
    'DeclarationPrime' : [ ['('],[';','[']],
    'VarDeclarationPrime' : [[';'],['[']],
    'FunDeclarationPrime' : [['(']],
    'TypeSpecifier': [['int'],['void']] ,
    'Params': [['int'],['void']] ,
    'ParamList': [[','],[')']],#16
    'Param': [['int','void']] ,
    'ParamPrime': [['['],[')', ',']],#19
    'CompoundStmt': [['{']],#20
    'StatementList' : [['ID',';','NUM','(','{','break','if','while','return','+','-'],['}']],#22
    'Statement' : [['ID',';','NUM','(','break','+','-'], ['{'], ['if'],['while'], ['return']],#27
    'ExpressionStmt' : [['ID','NUM','(','+','-'],['break'],[';']],#30
    'SelectionStmt' : [['if']],#31
    'IterationStmt' :[['while']],#32
    'ReturnStmt' :[['return']],
    'ReturnStmtPrime': [[';'],['ID','NUM','(','+','-']],#35
    'Expression': [['NUM','(','+','-'],['ID']],#37
    'B':[['='],['['],[';',']','(',')',',','<','==','+','-','*']],#40
    'H':[['='],[';',']',')',',','<','==','+','-','*']],#42
    'SimpleExpressionZegond': [['NUM','(','+','-']],
    'SimpleExpressionPrime' : [[';',']','(',')',',','<','==','+','-','*']],#44
    'C': [['<','=='],[';',']',')',',']], 
    'Relop': [['<'],['==']],#48
    'AdditiveExpression': [['ID','NUM','(','+','-']], 
    'AdditiveExpressionPrime': [[';',']','(',')',',','<','==','+','-','*']],
    'AdditiveExpressionZegond': [['NUM','(','+','-']],#51
    'D': [['+','-'], [';',']',')',',','<','==']],
    'Addop': [['+'],['-']],#55
    'Term': [['ID','NUM','(','+','-']],
    'TermPrime': [[';',']','(',')',',','<','==','+','-','*']],
    'TermZegond':[['NUM','(','+','-']],#58
    'G': [['*'],[';',']',')',',','<','==','+','-']], #60
    'SignedFactor': [['+'] , ['-'] , ['ID','NUM','(']],#63
    'SignedFactorPrime' : [[';',']','(',')',',','<','==','+','-','*']],
    'SignedFactorZegond' : [['+'] , ['-'] , ['NUM','(']],#67
    'Factor':[['('],['ID'],['NUM']],#70
    'VarCallPrime':[['('], [';','[',']',')',',','<','==','+','-','*']],#72
    'VarPrime':[['['],[';',']',')',',','<','==','+','-','*']],#74
    'FactorPrime':[['('],[';',']',')',',','<','==','+','-','*']],#76
    'FactorZegond':[['('],['NUM']],#78
    'Args': [['ID','NUM','('],[')']],#80 
    'ArgList':[['ID','NUM','(']], #81
    'ArgListPrime': [[','],[')']]#83
} 


first = {
    'Program':['int','void','EPSILON'] ,
    'DeclarationList':['int','void','EPSILON'] ,
    'Declaration': ['int','void'] ,
    'DeclarationInitial' : ['int','void'] ,
    'DeclarationPrime' : [';','[','('],
    'VarDeclarationPrime' : [';','['],
    'FunDeclarationPrime' : ['('],
    'TypeSpecifier': ['int','void'] ,
    'Params': ['int','void'] ,
    'ParamList': [',','EPSILON'],
    'Param': ['int','void'] ,
    'ParamPrime': ['[','EPSILON'],
    'CompoundStmt': ['{'],
    'StatementList' : ['ID',';','NUM','(','{','break','if','while','return','EPSILON'],
    'Statement' : ['ID',';','NUM','(','{','break','if','while', 'return'],
    'ExpressionStmt' : ['ID',';','NUM','(','break'],
    'SelectionStmt' : ['if'],
    'IterationStmt' :['while'],
    'ReturnStmt' :['return'],
    'ReturnStmtPrime': ['ID',';','NUM','(','+','-'],
    'Expression': ['ID','NUM','(','+','-'],
    'B':['[','(','=','<','==','+','-','*','EPSILON'],
    'H':['=','<','==','+','-','*','EPSILON'],
    'SimpleExpressionZegond': ['NUM','(','+','-'],
    'SimpleExpressionPrime' : ['(','==','+','-','*','EPSILON'],
    'C': ['<','==','EPSILON'], 
    'Relop': ['<','=='],
    'AdditiveExpression': ['ID','NUM','(','+','-'], 
    'AdditiveExpressionPrime': ['(','+','-','*','EPSILON'],
    'AdditiveExpressionZegond': ['NUM','(','+','-'],
    'D': ['+','-', 'EPSILON'],
    'Addop': ['+','-'],
    'Term': ['ID','NUM','(','+','-'],
    'TermPrime': ['(','*','EPSILON'],
    'TermZegond':['NUM','(','+','-'],
    'G': ['*','EPSILON'], 
    'SignedFactor': ['ID' , 'NUM' , '(', '+', '-'],
    'SignedFactorPrime' : ['(' , 'EPSILON'],
    'SignedFactorZegond' : ['NUM' , '(', '+', '-'],
    'Factor':['ID','NUM','('], 
    'VarCallPrime':['[','(','EPSILON'],
    'VarPrime':['[','EPSILON'],
    'FactorPrime':['(','EPSILON'],
    'FactorZegond':['NUM','('], 
    'Args': ['ID','NUM','(','+','-','EPSILON'], 
    'ArgList':['ID','NUM','(','+','-'], 
    'ArgListPrime': [',','EPSILON']
} 

follow = {
    'Program':['$'] ,
    'DeclarationList':['ID',';','NUM','(','{','}','break','if','while','return','+','-','$'] ,
    'Declaration': ['int','void','ID',';','NUM','(','{','}','break','if','while','return','+','-','$'] ,
    'DeclarationInitial' : [';','[','(',')',','] ,
    'DeclarationPrime' : ['ID',';','NUM','(','int','void','{','}','break','if','while','return','+','-','$'],
    'VarDeclarationPrime' : ['ID',';','NUM','(','int','void','{','}','break','if','while','return','+','-','$'],
    'FunDeclarationPrime' : ['ID',';','NUM','(','int','void','{','}','break','if','while','return','+','-','$'],
    'TypeSpecifier': ['ID'] ,
    'Params': [')'] ,
    'ParamList': [')'],
    'Param': [')',','] ,
    'ParamPrime': [')',','],
    'CompoundStmt': ['ID',';','NUM','(','int','void','{','}','break','if','else','while','return','+','-','$'],
    'StatementList' : ['}'],
    'Statement' : ['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'ExpressionStmt' : ['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'SelectionStmt' : ['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'IterationStmt' :['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'ReturnStmt' :['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'ReturnStmtPrime': ['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'Expression': [';',']',')',','],
    'B':[';',']',')',','],
    'H':[';',']',')',','],
    'SimpleExpressionZegond': [';',']',')',','],
    'SimpleExpressionPrime' : [';',']',')',','],
    'C': [';',']',')',','],
    'Relop': ['ID','NUM','(','+','-'],
    'AdditiveExpression': [';',']',')',','],
    'AdditiveExpressionPrime': [';',']',')',',','<','=='],
    'AdditiveExpressionZegond': [';',']',')',',','<','=='],
    'D': [';',']',')',',','<','=='],
    'Addop': ['ID','NUM','(','+','-'],
    'Term': [';',']',')',',','<','==','+','-'],
    'TermPrime': [';',']',')',',','<','==','+','-'],
    'TermZegond':[';',']',')',',','<','==','+','-'],
    'G': [';',']',')',',','<','==','+','-'],
    'SignedFactor': [';',']',')',',','<','==','+','-','*'],
    'SignedFactorPrime' : [';',']',')',',','<','==','+','-','*'],
    'SignedFactorZegond' : [';',']',')',',','<','==','+','-','*'],
    'Factor':[';',']',')',',','<','==','+','-','*'],
    'VarCallPrime':[';',']',')',',','<','==','+','-','*'],
    'VarPrime':[';',']',')',',','<','==','+','-','*'],
    'FactorPrime':[';',']',')',',','<','==','+','-','*'],
    'FactorZegond':[';',']',')',',','<','==','+','-','*'],
    'Args': [')'], 
    'ArgList':[')'], 
    'ArgListPrime': [')']
} 


def get_keys(data):
    return list(data.keys())

KEYWORDS = ["if", "else", "void", "int", "while", "break","return"]

class LL1Parser:
    def __init__(self):
        self.syntax_errors = []
        self.root = Node('Program')
        self.scanner = scanner('input.txt')
        self.token_type = ''
        self.token = ''
        self.line_number = 0
        self.non_terminals = get_keys(grammar)
        self.unexpected_eof_reached = False
        
    def is_non_terminal(self , word):
            if word in self.non_terminals:
                return True
            else:
                return False

    def get_next_token(self):
        while True:
            self.token_type , self.token , Error, self.line_number = self.scanner.get_next_token()
            if self.token_type != 'WHITESPACE' and self.token_type != 'COMMENT' and self.token_type != 'Error':
                break
        print('token= ' + self.token)
    
    def run_parser(self):
        self.get_next_token()
        print('1:',self.token,'---------------',self.token_type)
        self.parse(self.root)


    def parse(self , non_terminal:Node):
        for i in range(len(predict[non_terminal.name])):
            print('--------------node is: ' + non_terminal.name + ' i= ' + str(i) + ' -------------' )
            print('token: ' + self.token + '  ' + 'token type: ' + self.token_type)
            print(predict[non_terminal.name][i])
            if self.token in predict[non_terminal.name][i] or self.token_type in predict[non_terminal.name][i]:
                print('touched')
                for word in grammar[non_terminal.name][i]:
                    print('########### word is= ' + word + '###########')
                    if self.unexpected_eof_reached:
                        print('**********EOF**********')
                        return
                    if self.is_non_terminal(word):
                        print('non terminal: ' + word)
                        #get non terminal
                        node = Node(word, parent=non_terminal)
                        self.parse(node)
                    else: 
                        print('terminal is: ' + word )
                        
                        if word in ['NUM', 'ID'] and self.token_type == word:
                            Node(f'({self.token_type}, {self.token})', parent=non_terminal)
                            print('2:',self.token,'---------------',self.token_type)
                            self.get_next_token()
                        
                        elif (word in KEYWORDS or (word == '==' or self.scanner.get_token_type(word) == 'SYMBOL')) and self.token == word:
                            Node(f'({self.token_type}, {self.token})', parent=non_terminal)
                            self.get_next_token()
                
                        elif word == '$':
                            Node('$', parent=non_terminal)
                        elif word == 'EPSILON':
                            Node('epsilon', parent=non_terminal)
                        else:
                            #Error
                            self.syntax_errors.append(f'#{self.line_number + 1} : syntax error, missing {word}')


                        #get terminal
                        # correct = False
                        # if word in ['NUM', 'ID']:
                        #     correct = (self.token_type == word)
                        # elif (word in KEYWORDS) \
                        #         or (self.scanner.get_token_type(word) == 'SYMBOL' or word == '=='):
                        #     correct = (self.token == word)
                        # if correct:
                        #     Node(f'({self.token_type}, {self.token})', parent=non_terminal)
                        #     print('2:',self.token,'---------------',self.token_type)
                        #     self.get_next_token()
                        # elif word == 'EPSILON':
                        #     Node('epsilon', parent=non_terminal)
                        # elif word == '$':
                        #     Node('$', parent=non_terminal)
                        # else:
                        #     #Error
                        #     self.syntax_errors.append(f'#{self.line_number + 1} : syntax error, missing {word}')
                break
        else:  # is visited when no corresponding production was found
            print('problem is here')
            if self.token in follow[non_terminal.name]:
                if 'EPSILON' not in first[non_terminal.name]:  # missing T
                    self.syntax_errors.append(f'#{self.line_number + 1} : syntax error, missing {non_terminal.name}')
                non_terminal.parent = None  # Detach Node
                return  # exit
            else:  # illegal token
                if self.eof_reached():
                    self.syntax_errors.append(f'#{self.line_number + 1} : syntax error, Unexpected EOF')
                    self.unexpected_eof_reached = True
                    non_terminal.parent = None  # Detach Node
                    return
                # in samples, illegals are treated differently:
                illegal_lookahead = self.token
                if self.token_type in ['NUM', 'ID']:
                    illegal_lookahead = self.token_type
                #
                self.syntax_errors.append(f'#{self.line_number + 1} : syntax error, illegal {illegal_lookahead}')
                
                self.get_next_token()
                print('3:',self.token,'---------------',self.token_type)
                self.parse(non_terminal)

        


    def eof_reached(self):
        if self.token == '$':
            return True
        else:
            return False 
        
    def write_tree(self):
        with open('parse_tree.txt', 'w', encoding='utf-8') as f:
            for pre, fill, node in RenderTree(self.root):
                f.write("%s%s\n" % (pre, node.name))

    def write_syntax_errors(self):
        input = open('syntax_errors.txt','w')
        if len(self.syntax_errors)== 0:
            input.write('There is no syntax error.')
        else: 
            for i in self.syntax_errors:
                input.write(str(i+'\n'))

        input.close()
