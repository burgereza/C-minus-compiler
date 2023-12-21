from anytree import Node

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
    'Term': [['Factor', 'G']],
    'Term-prime': [['Factor-prime', 'G']],
    'Term-zegond':[['Factor-zegond', 'G']],
    'G':[['*', 'Factor' ,'G'],['EPSILON']],  
    'Factor':[['(', 'Expression', ')'], ['ID', 'Var-call-prime'], ['NUM']],
    'Var-call-prime':[['(', 'Args', ')'], ['Var-prime']],
    'Var-prime':[['[', 'Expression' ']'],['EPSILON']], 
    'Factor-prime':[['(' 'Args' ')'],['EPSILON']],  
    'Factor-zegond': [['(', 'Expression', ')'], ['NUM']],
    'Args': [['Arg-list'],['EPSILON']], 
    'Arg-list': [['Expression', 'Arg-list-prime']],
    'Arg-list-prime': [[',', 'Expression', 'Arg-list-prime'],['EPSILON']]

} 

predict_sets = {
    'Program':['int','viod','$'] ,
    'Declaration-list':[['int','void'],['ID',';','NUM','(','{','}','break','if','while','return','$']] ,
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
    'Return-stmt-prime': ['ID',';','NUM','('],
    'Expression': ['ID','NUM','('],
    'B':['[','(','=','<','==','+','-','*','EPSILON'],
    'H':['=','<','==','+','-','*','EPSILON'],
    'Simple-expression-zegond': ['NUM','('],
    'Simple-expression-prime' : ['(','==','+','-','*','EPSILON'],
    'C': ['<','==','EPSILON'], 
    'Relop': ['<','=='],
    'Additive-expression': ['ID','NUM','('], 
    'Additive-expression-prime': ['(','==','+','-','*','EPSILON'],
    'Additive-expression-zegond': ['NUM','('],
    'D': ['+','-', 'EPSILON'],
    'Addop': ['+','-'],
    'Term': ['ID','NUM','('],
    'Term-prime': ['(','*','EPSILON'],
    'Term-zegond':['NUM','('],
    'G': ['*','EPSILON'], 
    'Factor':['ID','NUM','('], 
    'Var-call-prime':['[','(','EPSILON'],
    'Var-prime':['['],
    'Factor-prime':['(','EPSILON'],
    'Factor-zegond':['NUM','('], 
    'Args': ['ID','NUM','(','EPSILON'], 
    'Arg-list':['ID','NUM','('], 
    'Arg-list-prime': [',','EPSILON']
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
    'Return-stmt-prime': ['ID',';','NUM','('],
    'Expression': ['ID','NUM','('],
    'B':['[','(','=','<','==','+','-','*','EPSILON'],
    'H':['=','<','==','+','-','*','EPSILON'],
    'Simple-expression-zegond': ['NUM','('],
    'Simple-expression-prime' : ['(','==','+','-','*','EPSILON'],
    'C': ['<','==','EPSILON'], 
    'Relop': ['<','=='],
    'Additive-expression': ['ID','NUM','('], 
    'Additive-expression-prime': ['(','==','+','-','*','EPSILON'],
    'Additive-expression-zegond': ['NUM','('],
    'D': ['+','-', 'EPSILON'],
    'Addop': ['+','-'],
    'Term': ['ID','NUM','('],
    'Term-prime': ['(','*','EPSILON'],
    'Term-zegond':['NUM','('],
    'G': ['*','EPSILON'], 
    'Factor':['ID','NUM','('], 
    'Var-call-prime':['[','(','EPSILON'],
    'Var-prime':['['],
    'Factor-prime':['(','EPSILON'],
    'Factor-zegond':['NUM','('], 
    'Args': ['ID','NUM','(','EPSILON'], 
    'Arg-list':['ID','NUM','('], 
    'Arg-list-prime': [',','EPSILON']
} 

follow = {
    'Program':['$'] ,
    'Declaration-list':['ID',';','NUM','(','{','}','break','if','while','return','$'] ,
    'Declaration': ['int','void','ID',';','NUM','(','{','}','break','if','while','return','$'] ,
    'Declaration-initial' : [';','[','(',')',','] ,
    'Declaration-prime' : ['ID',';','NUM','(','int','void','{','}','break','if','while','return','$'],
    'Var-declaration-prime' : ['ID',';','NUM','(','int','void','{','}','break','if','while','return','$'],
    'Fun-declaration-prime' : ['ID',';','NUM','(','int','void','{','}','break','if','while','return','$'],
    'Type-specifier': ['ID'] ,
    'Params': ['('] ,
    'Param-list': ['('],
    'Param': ['(',','] ,
    'Param-prime': ['(',','],
    'Compound-stmt': ['ID',';','NUM','(','int','void','{','}','break','if','else','while','return','$'],
    'Statement-list' : ['}'],
    'Statement' : ['ID',';','NUM','(','{','}','break','if','else','while','return'],
    'Expression-stmt' : ['ID',';','NUM','(','{','}','break','if','else','while','return'],
    'Selection-stmt' : ['ID',';','NUM','(','{','}','break','if','else','while','return'],
    'Iteration-stmt' :['ID',';','NUM','(','{','}','break','if','else','while','return'],
    'Return-stmt' :['ID',';','NUM','(','{','}','break','if','else','while','return'],
    'Return-stmt-prime': ['ID',';','NUM','(','{','}','break','if','else','while','return'],
    'Expression': [';',']',')',','],
    'B':[';',']',')',','],
    'H':[';',']',')',','],
    'Simple-expression-zegond': [';',']',')',','],
    'Simple-expression-prime' : [';',']',')',','],
    'C': [';',']',')',','],
    'Relop': ['ID','NUM','(',],
    'Additive-expression': [';',']',')',','],
    'Additive-expression-prime': [';',']',')',',','<','=='],
    'Additive-expression-zegond': [';',']',')',',','<','=='],
    'D': [';',']',')',',','<','=='],
    'Addop': ['ID','NUM','(',],
    'Term': [';',']',')',',','<','==','+','-'],
    'Term-prime': [';',']',')',',','<','==','+','-'],
    'Term-zegond':[';',']',')',',','<','==','+','-'],
    'G': [';',']',')',',','<','==','+','-'],
    'Factor':[';',']',')',',','<','==','+','-','*'],
    'Var-call-prime':[';',']',')',',','<','==','+','-','*'],
    'Var-prime':[';',']',')',',','<','==','+','-','*'],
    'Factor-prime':[';',']',')',',','<','==','+','-','*'],
    'Factor-zegond':[';',']',')',',','<','==','+','-','*'],
    'Args': [')'], 
    'Arg-list':[')'], 
    'Arg-list-prime': [')']
} 

predict = {
    '1': []
}




class LL1Parser:
    def __init__(self):
        self.syntax_errors = []
        self.root = Node('Program')
        self.scanner = scanner('input.txt')
        self.token_type = ''
        self.token = ''
        self.line_number = 0
        
        
    def get_next_token(self):
        self.token_type , self.token , Error, self.line_number = self.scanner.get_next_token()

    def parse(self , non_terminal):
        for i in range(predict[non_terminal:Node]):
            if self.token in predict[non_terminal:Node][i] or self.token_type in predict[non_terminal:Node][i]:
                for word in grammar[rule_number]:
                    if self.unexpected_eof_reached:
                        return
                    if is_non_terminal(word):
                        node = Node(word, parent=parent)
                        self.call_procedure(node)
                    else:
                        correct = False
                        if expected_token in ['NUM', 'ID']:
                            correct = self.lookahead[1] == expected_token
                        elif (expected_token in utils.symbol_table['keywords']) \
                                or (utils.get_token_type(expected_token) == utils.TokenType.SYMBOL or expected_token == '=='):
                            correct = self.lookahead[2] == expected_token

                        if correct:
                            Node(f'({self.lookahead[1]}, {self.lookahead[2]})', parent=parent)
                            self.lookahead = self.get_next_token()
                        elif expected_token == utils.TokenType.EPSILON:
                            Node('epsilon', parent=parent)
                        elif expected_token == utils.TokenType.DOLLAR:
                            Node('$', parent=parent)
                        else:
                            self.syntax_errors.append(f'#{self.lookahead[0]} : Syntax Error, Missing {expected_token}')
                        #self.call_match(word, parent)
                # #action found
                # for part in grammar[non_terminal:][i]:
                #     if is_non_terminal(non_terminal):
                #         #non_terminal
                #         self.parse()
                #     else:
                #         #terminal
                #         node = Node(non_terminal)
                return
        #Error


    def eof_reached(self):
        return self.lookahead[1] == utils.TokenType.DOLLAR
        





















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
