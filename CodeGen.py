from SymbolTable import *

# class func:
#     def __init__(self):
#         self.return_value = 0
#         self.parameters = []
#         self.top_sp = 0
#         self.temps = []


class codeGen:
    def __init__(self):
        self.action = None
        self.token = None
        self.symbol_table = SymbolTable()
        self.semantic_stack = []
        self.scope_stack = []
        self.stack = []
        self.top_sp = 0
        self.pb_counter = 0
        self.program_block = []
        self.scope_stack = [1]
        self.reg = 500
        self.lentgh_byte = 4


        self.program_block.append(f"(ASSIGN, #4, 0, )")
        
    def get_addres(self,space = 1):
        address = str(self.reg)
        for _ in range(space):
            self.reg += 4
        return address

    def add_to_pb(self, part1, part2, part3='', part4=''):
        self.program_block[self.pb_counter] = f'({part1}, {part2}, {part3}, {part4})'
        self.pb_counter += 1

    def handle_action(self,action,token):
        self.action = action
        self.token = token
        print(self.semantic_stack)
        if self.action == 'push_ID':
            self.push_ID()
            self.semantic_stack.append(self.token)

        elif self.action == 'push_type':
            self.push_type()
            self.semantic_stack.append(self.token)

        elif self.action == 'start_of_function':
            self.start_of_function()
            self.semantic_stack.append('startfun')

        elif self.action == 'define_variable':
            self.define_variable() 

            name = self.semantic_stack.pop()
            temp_type = self.semantic_stack.pop()     
            temp_symbol = Symbol(lexeme= name,type=temp_type,address=self.reg ,scope=self.scope_stack[(-1)],
                                 type_var='var',no_arguments=0,line_pb=len(self.program_block)-1)
            self.symbol_table.add_symbol(temp_symbol)
            self.reg += self.lentgh_byte
        elif self.action == 'push_NUM':
            self.push_NUM()
            self.program_block.append(f'(ASSIGN, #{int(self.token)}, {self.reg}, )')
            self.reg += self.lentgh_byte
            self.semantic_stack.append(int(self.token))

        elif self.action == 'define_array':
            self.define_array()

            temp_num = self.semantic_stack.pop()
            temp_id = self.semantic_stack.pop()
            temp_type = self.semantic_stack.pop()

            temp_symbol = Symbol(lexeme= temp_id,type=temp_type,address=self.reg ,scope=self.scope_stack[(len(scope_stack) - 1)],
                                 type_var='arr',no_arguments=temp_num,line_pb=len(self.program_block)-1)
            self.reg *= temp_num
            self.symbol_table.add_symbol(temp_symbol)           

        elif self.action == 'define_function':
            self.define_function()
            arguments = []
            print('self.semantic_stack: ')
            print(self.semantic_stack)
            while self.semantic_stack[-1] != 'startfun':
                arguments.append(self.semantic_stack.pop())
            self.semantic_stack.pop()
            temp_num = self.semantic_stack.pop()
            temp_type = self.semantic_stack.pop()
            num_arg = len(arguments) // 3
            if temp_num != 'main':
                self.program_block.append("(JP, ?, , )")
                self.semantic_stack.append(len(self.program_block)-1)

            
            self.scope_stack.append(self.scope_stack[-1] + 1)
            temp_symbol= Symbol(lexeme=temp_num, type= temp_type, scope=self.scope_stack[len(self.scope_stack)-1] ,
                                type_var='funcation',no_arguments=num_arg,address=int(len(self.program_block)) )
            self.symbol_table.add_symbol(temp_symbol)

            self.scope_stack.append(self.scope_stack[-1] + 1)
            arguments.reverse()
            print('len(arguments): ' + str(len(arguments)))
            print(arguments)
            for i in range(0,len(arguments),3):
                ty=arguments[i] 
                name= arguments[i+1]
                array = arguments[i+2]

                if  array == 'arr':
                    temp_symbol= Symbol(lexeme=name, type= ty, scope=self.scope_stack[len(self.scope_stack)-1]
                        ,type_var='arr',no_arguments=0,address=int(len(self.program_block)) )
                    self.symbol_table.add_symbol(temp_symbol)
                else:
                    temp_symbol= Symbol(lexeme=name, type= ty, scope=self.scope_stack[len(self.scope_stack)-1]
                        ,type_var='var',no_arguments=0,address=self.reg )
                    self.symbol_table.add_symbol(temp_symbol)
                    self.reg += self.lentgh_byte
            self.symbol_table.print_symbol_table()
        elif self.action == 'end_of_scope':
            self.end_of_scope()
            self.symbol_table.delete_scope(self.scope_stack.pop())

        elif self.action == 'end_of_function':
            self.end_of_function()

        elif self.action == 'push_array_type':
            self.push_array_type()
            self.semantic_stack.append('arr')

        elif self.action == 'push_non_type':
            self.push_non_type()
            self.semantic_stack.append('nothing')

        elif self.action == 'pop':
            self.pop()
            self.semantic_stack.pop()

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

        elif self.action == 'start_function_call':
            self.start_function_call()

        elif self.action == 'function_call':
            self.function_call()

            











































    def push_ID(self):
        print('push_ID' + ' ' + self.token)
        
    def push_type(self):
        print('push_type' + ' ' + self.token)
    
    def start_of_function(self):
        print('start_of_function' + ' ' + self.token)
    
    def define_variable(self):
        print('define_variable' + ' ' + self.token)
    
    def push_NUM(self):
        print('push_NUM' + ' ' + self.token)
    
    def define_array(self):
        print('define_array' + ' ' + self.token)
    
    def define_function(self):
        print('define_function' + ' ' + self.token)
    
    def end_of_scope(self):
        print('end_of_scope' + ' ' + self.token)
    
    def end_of_function(self):
        print('end_of_function' + ' ' + self.token)
    
    def push_array_type(self):
        print('push_array_type' + ' ' + self.token)
    
    def push_non_type(self):
        print('push_non_type' + ' ' + self.token)
    
    def pop(self):
        print('pop' + ' ' + self.token)
    
    def if_stmt(self):
        print('if' + ' ' + self.token)
    
    def else_stmt(self):
        print('else' + ' ' + self.token)
    
    def end_if(self):
        print('end_if' + ' ' + self.token)
    
    def while_stmt(self):
        print('while_stmt' + ' ' + self.token)
    
    def while_condition(self):
        print('while_condition' + ' ' + self.token)
    
    def end_while(self):
        print('end_while' + ' ' + self.token)
    
    def return_stmt(self):
        print('return_stmt' + ' ' + self.token)
    
    def return_value(self):
        print('return_value' + ' ' + self.token)
    
    def assign(self):
        print('assign' + ' ' + self.token)
    
    def find_array_address(self):
        print('find_array_address' + ' ' + self.token)
    
    def relop(self):
        print('relop' + ' ' + self.token)
    
    def LT(self):
        print('LT' + ' ' + self.token)
    
    def EQ(self):
        print('EQ' + ' ' + self.token)
    
    def add_or_sub(self):
        print('add_or_sub' + ' ' + self.token)
    
    def add(self):
        print('add' + ' ' + self.token)
    
    def sub(self):
        print('sub' + ' ' + self.token)
    
    def mult(self):
        print('mult' + ' ' + self.token)
    
    def negate(self):
        print('negate' + ' ' + self.token)
    
    def function_call(self):
        print('function_call' + ' ' + self.token)
    
    def start_function_call(self):
        print('start_function_call' + ' ' + self.token)
    

