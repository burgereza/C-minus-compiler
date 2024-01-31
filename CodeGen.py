

class codeGen:
    def __init__(self):
        self.action = None
        self.token = None
        self.token_type = None
        self.symbol_table = []
        self.semantic_stack = []
        self.scope_stack = []
        self.stack = []
        
    def handle_action(self,action,token,token_type):
        self.action = action
        self.token = token
        self.token_type = token_type

        if self.action == 'push_ID':
            self.push_ID()      
        elif self.action == 'push_type':
            self.push_type()     
        elif self.action == 'start_of_function':
            self.start_of_function()     
        elif self.action == 'define_variable':
            self.define_variable()      
        elif self.action == 'push_NUM':
            self.push_NUM()      
        elif self.action == 'define_array':
            self.define_array()      
        elif self.action == 'define_function':
            self.define_function()      
        elif self.action == 'end_of_scope':
            self.end_of_scope()      
        elif self.action == 'end_of_function':
            self.end_of_function()      
        elif self.action == 'push_array_type':
            self.push_array_type()  
        elif self.action == 'push_non_type':
            self.push_non_type()
        elif self.action == 'pop':
            self.pop()
        elif self.action == 'if':
            self.if_stmt()
        elif self.action == 'else':
            self.else_stmt()
        elif self.action == 'end_if':
            self.end_if()
        elif self.action == 'while':
            self.while_stmt()
        elif self.action == 'while_condition':
            self.while_condition()     
        elif self.action == 'end_while':
            self.end_while()     
        elif self.action == 'return':
            self.return_stmt()    
        elif self.action == 'return_value':
            self.return_value()    
        elif self.action == 'assign':
            self.assign()     
        elif self.action == 'find_array_address':
            self.find_array_address()     
        elif self.action == 'relop':
            self.relop()    
        elif self.action == 'LT':
            self.LT() 
        elif self.action == 'EQ':
            self.EQ()      
        elif self.action == 'add_or_sub':
            self.add_or_sub()     
        elif self.action == 'add':
            self.add()     
        elif self.action == 'sub':
            self.sub()     
        elif self.action == 'mult':
            self.mult()     
        elif self.action == 'negate':
            self.negate()     
        elif self.action == 'function_call':
            self.function_call()
            


    def push_ID(self):
        print('push_ID' + ' ' + self.token + ' ' + self.token_type)
        self.semantic_stack.append(self.token)
        
    def push_type(self):
        print('push_type' + ' ' + self.token + ' ' + self.token_type)
        self.semantic_stack.append(self.token)
    
    def start_of_function(self):
        print('start_of_function' + ' ' + self.token + ' ' + self.token_type)
    
    def define_variable(self):
        print('define_variable' + ' ' + self.token + ' ' + self.token_type)
    
    def push_NUM(self):
        print('push_NUM' + ' ' + self.token + ' ' + self.token_type)
    
    def define_array(self):
        print('define_array' + ' ' + self.token + ' ' + self.token_type)
    
    def define_function(self):
        print('define_function' + ' ' + self.token + ' ' + self.token_type)
    
    def end_of_scope(self):
        print('end_of_scope' + ' ' + self.token + ' ' + self.token_type)
    
    def end_of_function(self):
        print('end_of_function' + ' ' + self.token + ' ' + self.token_type)
    
    def push_array_type(self):
        print('push_array_type' + ' ' + self.token + ' ' + self.token_type)
    
    def push_non_type(self):
        print('push_non_type' + ' ' + self.token + ' ' + self.token_type)
    
    def pop(self):
        print('pop' + ' ' + self.token + ' ' + self.token_type)
    
    def if_stmt(self):
        print('if' + ' ' + self.token + ' ' + self.token_type)
    
    def else_stmt(self):
        print('else' + ' ' + self.token + ' ' + self.token_type)
    
    def end_if(self):
        print('end_if' + ' ' + self.token + ' ' + self.token_type)
    
    def while_stmt(self):
        print('while_stmt' + ' ' + self.token + ' ' + self.token_type)
    
    def while_condition(self):
        print('while_condition' + ' ' + self.token + ' ' + self.token_type)
    
    def end_while(self):
        print('end_while' + ' ' + self.token + ' ' + self.token_type)
    
    def return_stmt(self):
        print('return_stmt' + ' ' + self.token + ' ' + self.token_type)
    
    def return_value(self):
        print('return_value' + ' ' + self.token + ' ' + self.token_type)
    
    def assign(self):
        print('assign' + ' ' + self.token + ' ' + self.token_type)
    
    def find_array_address(self):
        print('find_array_address' + ' ' + self.token + ' ' + self.token_type)
    
    def relop(self):
        print('relop' + ' ' + self.token + ' ' + self.token_type)
    
    def LT(self):
        print('LT' + ' ' + self.token + ' ' + self.token_type)
    
    def EQ(self):
        print('EQ' + ' ' + self.token + ' ' + self.token_type)
    
    def add_or_sub(self):
        print('add_or_sub' + ' ' + self.token + ' ' + self.token_type)
    
    def add(self):
        print('add' + ' ' + self.token + ' ' + self.token_type)
    
    def sub(self):
        print('sub' + ' ' + self.token + ' ' + self.token_type)
    
    def mult(self):
        print('mult' + ' ' + self.token + ' ' + self.token_type)
    
    def negate(self):
        print('negate' + ' ' + self.token + ' ' + self.token_type)
    
    def function_call(self):
        print('function_call' + ' ' + self.token + ' ' + self.token_type)
    

