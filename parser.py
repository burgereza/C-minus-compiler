grammer = {

    'Program': [['Declaration-list']],
    'Declaration-list' : [['Declaration', 'Declaration-list'],[None]], 
    'Declaration' : [['Declaration-initial',  'Declaration-prime']],
    'Declaration-initial' : [['Type-specifier', 'ID']],
    'Declaration-prime' : [['Fun-declaration-prime'], ['Var-declaration-prime']],
    'Var-declaration-prime' : [[';'],['[', 'NUM', ']', ';']],  
    'Fun-declaration-prime' : [ ['(', 'Params', ')', 'Compound-stmt']],
    'Type-specifier': [['int'], ['void']],
    'Params': [['int', 'ID' ,'Param-prime', 'Param-list'], ['void']],
    'Param-list': [[',', 'Param', 'Param-list'], [None]],
    'Param': [ ['Declaration-initial', 'Param-prime']],
    'Param-prime': [['[', ']'],[None]] ,
    'Compound-stmt': [['{' ,'Declaration-list', 'Statement-list', '}']],
    'Statement-list' :[[ 'Statement', 'Statement-list'],[None]],  
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
    'C': [['Relop', 'Additive-expression'],[None]], 
    'Relop': [['<'],['==']], 
    'Additive-expression': [['Term D']],
    'Additive-expression-prime': [['Term-prime', 'D']],
    'Additive-expression-zegond': [['Term-zegond', 'D']],
    'D': [['Addop', 'Term', 'D'],[None]], 
    'Addop':[['+'],['-']], 
    'Term': [['Factor', 'G']],
    'Term-prime': [['Factor-prime', 'G']],
    'Term-zegond':[['Factor-zegond', 'G']],
    'G':[['*', 'Factor' ,'G'],[None]],  
    'Factor':[['(', 'Expression', ')'], ['ID', 'Var-call-prime'], ['NUM']],
    'Var-call-prime':[['(', 'Args', ')'], ['Var-prime']],
    'Var-prime':[['[', 'Expression' ']'],[None]], 
    'Factor-prime':[['(' 'Args' ')'],[None]],  
    'Factor-zegond': [['(', 'Expression', ')'], ['NUM']],
    'Args': [['Arg-list'],[None]], 
    'Arg-list': [['Expression', 'Arg-list-prime']],
    'Arg-list-prime': [[',', 'Expression', 'Arg-list-prime'],[None]]

} 

first = {
    'Program':['int','viod',None] ,
    'Declaration-list':['int','void',None] ,
    'Declaration': ['int','void'] ,
    'Declaration-initial' : ['int','void'] ,
    'Declaration-prime' : [';','[','('],
    'Var-declaration-prime' : [';','['],
    'Fun-declaration-prime' : ['('],
    'Type-specifier': ['int','void'] ,
    'Params': ['int','void'] ,
    'Param-list': [',',None],
    'Param': ['int','void'] ,
    'Param-prime': ['[',None],
    'Compound-stmt': ['{'],
    'Statement-list' : ['ID',';','NUM','(','{','break','if','while','return',None],
    'Statement' : ['ID',';','NUM','(','{','break','if','while', 'return'],
    'Expression-stmt' : ['ID',';','NUM','(','break'],
    'Selection-stmt' : ['if'],
    'Iteration-stmt' :['while'],
    'Return-stmt' :['return'],
    'Return-stmt-prime': ['ID',';','NUM','('],
    'Expression': ['ID','NUM','('],
    'B':['[','(','=','<','==','+','-','*',None],
    'H':['=','<','==','+','-','*',None],
    'Simple-expression-zegond': ['NUM','('],
    'Simple-expression-prime' : ['(','==','+','-','*',None],
    'C': ['<','==',None], 
    'Relop': ['<','=='],
    'Additive-expression': ['ID','NUM','('], 
    'Additive-expression-prime': ['(','==','+','-','*',None],
    'Additive-expression-zegond': ['NUM','('],
    'D': ['+','-', None],
    'Addop': ['+','-'],
    'Term': ['ID','NUM','('],
    'Term-prime': ['(','*',None],
    'Term-zegond':['NUM','('],
    'G': ['*',None], 
    'Factor':['ID','NUM','('], 
    'Var-call-prime':['[','(',None],
    'Var-prime':['['],
    'Factor-prime':['(',None],
    'Factor-zegond':['NUM','('], 
    'Args': ['ID','NUM','(',None], 
    'Arg-list':['ID','NUM','('], 
    'Arg-list-prime': [',',None]
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



class LL1Parser:
    def __init__(self, grammar, first, follow):
        self.grammar = grammar
        self.first = first
        self.follow = follow
        self.table = {}

    def build_table(self):
        for non_terminal, productions in self.grammar.items():
            for production in productions:
                first_set = self.get_first_set(production)
                for symbol in first_set:
                    if symbol is not None:
                        self.table[(non_terminal, symbol)] = production

                if None in first_set or (None in self.follow[non_terminal] and non_terminal != 'Program'):
                    follow_set = self.follow[non_terminal]
                    for symbol in follow_set:
                        if symbol is not None:
                            self.table[(non_terminal, symbol)] = production

    def get_first_set(self, production):
        first_set = set()
        for symbol in production:
            first_set |= set(self.first[symbol])
            if None not in self.first[symbol]:
                break
        return first_set