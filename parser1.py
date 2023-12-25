from anytree import Node
from anytree import RenderTree
import anytree
from scanner import scanner
grammar = {

    'Program': [['Declaration-list']],
    'Declaration-list' : [['Declaration', 'Declaration-list'],['EPSILON']], 
    'Declaration' : [['Declaration-initial',  'Declaration-prime']],
    'Declaration-initial' : [['Type-specifier', 'ID']],
    'Declaration-prime' : [['Fun-declaration-prime'], ['Var-declaration-prime']],
    'Var-declaration-prime' : [[';'],['[', 'NUM', ']', ';']],  
    'Fun-declaration-prime' : [ ['(', 'Params', ')', 'Compound-stmt']],
    'Type-specifier': [['int'], ['void']],
    'Params': [['int', 'ID' ,'Param-prime', 'Param-list'], ['void']],
    'Param-list': [[',', 'Param', 'Param-list'], ['EPSILON']],
    'Param': [ ['Declaration-initial', 'Param-prime']],
    'Param-prime': [['[', ']'],['EPSILON']] ,
    'Compound-stmt': [['{' ,'Declaration-list', 'Statement-list', '}']],
    'Statement-list' :[[ 'Statement', 'Statement-list'],['EPSILON']],  
    'Statement' : [['Expression-stmt'], ['Compound-stmt'], ['Selection-stmt'], ['Iteration-stmt' ],['Return-stmt']],
    'Expression-stmt' : [['Expression', ';'], ['break', ';'], [';']],
    'Selection-stmt' : [['if', '(', 'Expression' ,')', 'Statement', 'else', 'Statement']],
    'Iteration-stmt' :[[ 'while', '(', 'Expression', ')', 'Statement']], 
    'Return-stmt' :[['return', 'Return-stmt-prime']],
    'Return-stmt-prime':[[';'],['Expression', ';']],
    'Expression': [['Simple-expression-zegond'], ['ID', 'B']],
    'B':[[ '=', 'Expression'], ['[', 'Expression', ']', 'H'], ['Simple-expression-prime']],
    'H':[[ '=', 'Expression'], ['G', 'D', 'C']],
    'Simple-expression-zegond': [['Additive-expression-zegond', 'C']],
    'Simple-expression-prime' : [['Additive-expression-prime', 'C']],
    'C': [['Relop', 'Additive-expression'],['EPSILON']], 
    'Relop': [['<'],['==']], 
    'Additive-expression': [['Term D']],
    'Additive-expression-prime': [['Term-prime', 'D']],
    'Additive-expression-zegond': [['Term-zegond', 'D']],
    'D': [['Addop', 'Term', 'D'],['EPSILON']], 
    'Addop':[['+'],['-']], 
    'Term': [['SignedFactor', 'G']],
    'Term-prime': [['SignedFactorPrime', 'G']],
    'Term-zegond':[['SignedFactorZegond', 'G']],
    'G':[['*', 'Factor' ,'G'],['EPSILON']],
    'SignedFactor': [['+' , 'Factor'] , ['-' , 'Factor'], ['Factor']],
    'SignedFactorPrime' : [['Factor-Prime']],
    'SignedFactorZegond': [['+', 'Factor'] , ['-', 'Factor'] , ['FactoZegond']],
    'Factor':[['(', 'Expression', ')'], ['ID', 'Var-call-prime'], ['NUM']],
    'Var-call-prime':[['(', 'Args', ')'], ['Var-prime']],
    'Var-prime':[['[', 'Expression' ']'],['EPSILON']], 
    'Factor-prime':[['(' 'Args' ')'],['EPSILON']],  
    'Factor-zegond': [['(', 'Expression', ')'], ['NUM']],
    'Args': [['Arg-list'],['EPSILON']], 
    'Arg-list': [['Expression', 'Arg-list-prime']],
    'Arg-list-prime': [[',', 'Expression', 'Arg-list-prime'],['EPSILON']]

} 

predict = {
    'Program':[['int','viod','$']] ,
    'Declaration-list':[['int','void'],['ID',';','NUM','(','{','}','break','if','while','return','$']] ,
    'Declaration': [['int','void']] ,
    'Declaration-initial' : [['int','void']] ,
    'Declaration-prime' : [ ['('],[';','[']],
    'Var-declaration-prime' : [[';'],['[']],
    'Fun-declaration-prime' : [['(']],
    'Type-specifier': [['int'],['void']] ,
    'Params': [['int'],['void']] ,
    'Param-list': [[','],[')']],#16
    'Param': [['int','void']] ,
    'Param-prime': [['['],[')', ',']],#19
    'Compound-stmt': [['{']],#20
    'Statement-list' : [['ID',';','NUM','(','{','break','if','while','return','+','-'],['}']],#22
    'Statement' : [['ID',';','NUM','(','break','+','-'], ['{'], ['if'],['while'], ['return']],#27
    'Expression-stmt' : [['ID','NUM','(','+','-'],['break'],[';']],#30
    'Selection-stmt' : [['if']],#31
    'Iteration-stmt' :[['while']],#32
    'Return-stmt' :[['return']],
    'Return-stmt-prime': [[';'],['ID','NUM','(','+','-']],#35
    'Expression': [['NUM','(','+','-'],['ID']],#37
    'B':[['='],['['],[';',']','(',')',',','<','==','+','-','*']],#40
    'H':[['='],[';',']',')',',','<','==','+','-','*']],#42
    'Simple-expression-zegond': [['NUM','(','+','-']],
    'Simple-expression-prime' : [[';',']','(',')',',','<','==','+','-','*']],#44
    'C': [['<','=='],[';',']',')',',']], 
    'Relop': [['<'],['==']],#48
    'Additive-expression': [['ID','NUM','(','+','-']], 
    'Additive-expression-prime': [[';',']','(',')',',','<','==','+','-','*']],
    'Additive-expression-zegond': [['NUM','(','+','-']],#51
    'D': [['+','-'], [';',']',')',',','<','==']],
    'Addop': [['+'],['-']],#55
    'Term': [['ID','NUM','(','+','-']],
    'Term-prime': [[';',']','(',')',',','<','==','+','-','*']],
    'Term-zegond':[['NUM','(','+','-']],#58
    'G': [['*'],[';',']',')',',','<','==','+','-']], #60
    'SignedFactor': [['+'] , ['-'] , ['ID','NUM','(']],#63
    'SignedFactorPrime' : [[';',']','(',')',',','<','==','+','-','*']],
    'SignedFactorZegond' : [['+'] , ['-'] , ['NUM','(']],#67
    'Factor':[['('],['ID'],['NUM']],#70
    'Var-call-prime':[['('], ['[']],#72
    'Var-prime':[['['],[';',']',')',',','<','==','+','-','*']],#74
    'Factor-prime':[['('],[';',']',')',',','<','==','+','-','*']],#76
    'Factor-zegond':[['('],['NUM']],#78
    'Args': [['ID','NUM','('],[')']],#80 
    'Arg-list':[['ID','NUM','(']], #81
    'Arg-list-prime': [[','],[')']]#83
} 


first = {
    'Program':['int','viod','EPSILON'] ,
    'Declaration-list':['int','void','EPSILON'] ,
    'Declaration': ['int','void'] ,
    'Declaration-initial' : ['int','void'] ,
    'Declaration-prime' : [';','[','('],
    'Var-declaration-prime' : [';','['],
    'Fun-declaration-prime' : ['('],
    'Type-specifier': ['int','void'] ,
    'Params': ['int','void'] ,
    'Param-list': [',','EPSILON'],
    'Param': ['int','void'] ,
    'Param-prime': ['[','EPSILON'],
    'Compound-stmt': ['{'],
    'Statement-list' : ['ID',';','NUM','(','{','break','if','while','return','EPSILON'],
    'Statement' : ['ID',';','NUM','(','{','break','if','while', 'return'],
    'Expression-stmt' : ['ID',';','NUM','(','break'],
    'Selection-stmt' : ['if'],
    'Iteration-stmt' :['while'],
    'Return-stmt' :['return'],
    'Return-stmt-prime': ['ID',';','NUM','(','+','-'],
    'Expression': ['ID','NUM','(','+','-'],
    'B':['[','(','=','<','==','+','-','*','EPSILON'],
    'H':['=','<','==','+','-','*','EPSILON'],
    'Simple-expression-zegond': ['NUM','(','+','-'],
    'Simple-expression-prime' : ['(','==','+','-','*','EPSILON'],
    'C': ['<','==','EPSILON'], 
    'Relop': ['<','=='],
    'Additive-expression': ['ID','NUM','(','+','-'], 
    'Additive-expression-prime': ['(','+','-','*','EPSILON'],
    'Additive-expression-zegond': ['NUM','(','+','-'],
    'D': ['+','-', 'EPSILON'],
    'Addop': ['+','-'],
    'Term': ['ID','NUM','(','+','-'],
    'Term-prime': ['(','*','EPSILON'],
    'Term-zegond':['NUM','(','+','-'],
    'G': ['*','EPSILON'], 
    'SignedFactor': ['ID' , 'NUM' , '(', '+', '-'],
    'SignedFactorPrime' : ['(' , 'EPSILON'],
    'SignedFactorZegond' : ['NUM' , '(', '+', '-'],
    'Factor':['ID','NUM','('], 
    'Var-call-prime':['[','(','EPSILON'],
    'Var-prime':['['],
    'Factor-prime':['(','EPSILON'],
    'Factor-zegond':['NUM','('], 
    'Args': ['ID','NUM','(','+','-','EPSILON'], 
    'Arg-list':['ID','NUM','(','+','-'], 
    'Arg-list-prime': [',','EPSILON']
} 

follow = {
    'Program':['$'] ,
    'Declaration-list':['ID',';','NUM','(','{','}','break','if','while','return','+','-','$'] ,
    'Declaration': ['int','void','ID',';','NUM','(','{','}','break','if','while','return','+','-','$'] ,
    'Declaration-initial' : [';','[','(',')',','] ,
    'Declaration-prime' : ['ID',';','NUM','(','int','void','{','}','break','if','while','return','+','-','$'],
    'Var-declaration-prime' : ['ID',';','NUM','(','int','void','{','}','break','if','while','return','+','-','$'],
    'Fun-declaration-prime' : ['ID',';','NUM','(','int','void','{','}','break','if','while','return','+','-','$'],
    'Type-specifier': ['ID'] ,
    'Params': [')'] ,
    'Param-list': [')'],
    'Param': [')',','] ,
    'Param-prime': [')',','],
    'Compound-stmt': ['ID',';','NUM','(','int','void','{','}','break','if','else','while','return','+','-','$'],
    'Statement-list' : ['}'],
    'Statement' : ['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'Expression-stmt' : ['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'Selection-stmt' : ['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'Iteration-stmt' :['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'Return-stmt' :['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'Return-stmt-prime': ['ID',';','NUM','(','{','}','break','if','else','while','return','+','-'],
    'Expression': [';',']',')',','],
    'B':[';',']',')',','],
    'H':[';',']',')',','],
    'Simple-expression-zegond': [';',']',')',','],
    'Simple-expression-prime' : [';',']',')',','],
    'C': [';',']',')',','],
    'Relop': ['ID','NUM','(','+','-'],
    'Additive-expression': [';',']',')',','],
    'Additive-expression-prime': [';',']',')',',','<','=='],
    'Additive-expression-zegond': [';',']',')',',','<','=='],
    'D': [';',']',')',',','<','=='],
    'Addop': ['ID','NUM','(','+','-'],
    'Term': [';',']',')',',','<','==','+','-'],
    'Term-prime': [';',']',')',',','<','==','+','-'],
    'Term-zegond':[';',']',')',',','<','==','+','-'],
    'G': [';',']',')',',','<','==','+','-'],
    'SignedFactor': [';',']',')',',','<','==','+','-','*'],
    'SignedFactorPrime' : [';',']',')',',','<','==','+','-','*'],
    'SignedFactorZegond' : [';',']',')',',','<','==','+','-','*'],
    'Factor':[';',']',')',',','<','==','+','-','*'],
    'Var-call-prime':[';',']',')',',','<','==','+','-','*'],
    'Var-prime':[';',']',')',',','<','==','+','-','*'],
    'Factor-prime':[';',']',')',',','<','==','+','-','*'],
    'Factor-zegond':[';',']',')',',','<','==','+','-','*'],
    'Args': [')'], 
    'Arg-list':[')'], 
    'Arg-list-prime': [')']
} 



class LL1Parser:
    def __init__(self):
        self.syntax_errors = []
        self.root = Node('Program')
        self.scanner = scanner('input.txt')
        self.token_type = ''
        self.token = ''
        self.line_number = 0
        self.non_terminals = ['Program','Declaration-list','Declaration','Declaration-initial','Declaration-prime','Var-declaration-prime',
                              'Fun-declaration-prime',]
        
        
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
    
    def run_parser(self):
        self.get_next_token()
        self.parse(Node('Program'))

    def parse(self , non_terminal):
        for i in range(len(predict[non_terminal.name])):
            if self.token in predict[non_terminal.name][i] or self.token_type in predict[non_terminal.name][i]:
                for word in grammar[non_terminal.name][i]:
                    if self.eof_reached():
                        print(word + 'EOF')
                        return
                    if self.is_non_terminal(word):
                        print('non terminal: ' + word)
                        #get non terminal
                        node = Node(word, parent=non_terminal)
                        self.parse(node)
                    else: 
                        #get terminal
                        correct = False
                        if word in ['NUM', 'ID']:
                            correct = (self.token_type == word)
                        elif (word in self.scanner.KEYWORDS) \
                                or (self.scanner.get_type(word) == 'SYMBOL' or word == '=='):
                            correct = (self.token == word)

                        if correct:
                            Node(f'({self.token_type}, {self.token})', parent=non_terminal)
                            self.get_next_token()

                        elif word == 'EPSILON':
                            Node('epsilon', parent=non_terminal)
                        elif word == 'DOLLAR':
                            Node('$', parent=non_terminal)
                        else:
                            #Error
                            self.syntax_errors.append(f'#{self.line_number} : Syntax Error, Missing {word}')
                return
        
                        # correct = False
                        # if word in ['NUM', 'ID']:
                        #     correct = (self.token_type == word)
                        # elif (word in self.scanner.KEYWORDS) \
                        #         or (self.scanner.get_type(word) == 'SYMBOL' or word == '=='):
                        #     correct = (self.token == word)

                        # if correct:
                        #     Node(f'({self.token_type}, {self.token})', parent=non_terminal)
                        #     self.get_next_token()

                        # elif word == 'EPSILON':
                        #     Node('epsilon', parent=non_terminal)
                        # elif word == 'DOLLAR':
                        #     Node('$', parent=non_terminal)
                        # else:
                        #     #Error
                        #     self.syntax_errors.append(f'#{self.line_number} : Syntax Error, Missing {word}')
        


    def eof_reached(self):
        if self.token == '$':
            return True
        else:
            return False 
        
    def write_tree(self, file_name):
        with open(file_name, 'w') as tree_file:
            tree_file.write(anytree.RenderTree(self.root).by_attr(attrname="name"))

    def write_syntax_errors(self, file_name):
            with open(file_name, 'w') as syntax_file:
                if self.syntax_errors:
                    syntax_file.write('\n'.join(f'#{a} : {b}' for a, b in self.errors))
                else:
                    syntax_file.write('There is no syntax error.')




















#     def build_table(self):
#         for non_terminal, productions in self.grammar.items():
#             for production in productions:
#                 first_set = self.get_first_set(production)
#                 for symbol in first_set:
#                     if symbol is not 'EPSILON':
#                         self.table[(non_terminal, symbol)] = production

#                 if 'EPSILON' in first_set :#or ('EPSILON' in self.follow[non_terminal] and non_terminal != 'Program'):
#                     follow_set = self.follow[non_terminal]
#                     for symbol in follow_set:
#                         if symbol is not 'EPSILON':
#                             self.table[(non_terminal, symbol)] = 'EPSILON'

#     def get_first_set(self, production):
#         first_set = set()
#         for symbol in production:
#             first_set |= set(self.first[symbol])
#             if 'EPSILON' not in self.first[symbol]:
#                 break
#         return first_set

#     def run(self):
#         self.build_table()
#         print(self.table)


# myprser = LL1Parser()
# myprser.run()


# top_of_stack = ''
# current_token = scanner.get_next_token()
# while top_of_stack != '$':
#     if top_of_stack == current_token:
#         handle_terminal() # ==> stack.pop() , add token to the parse_tree
#     else:
#         error = True
#         production = top_of_stack
#         for action in grammar(production):
#             if current_token in action.firsts():
#                 handle_action() # ==> stack.pop() , stack.push(action)
#                 error == false
#         if error == True:
#             handle_error()
