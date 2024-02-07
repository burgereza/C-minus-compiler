from SymbolTable import *

class function:
    def __init__(self,name,parameters):
        self.name = name
        self.parameters = parameters

    def add_param(self,addr):
        self.parameters.append(addr)

class funcss:
    def __init__(self):
        funcs = []

    def find_func(self, func_name):
        for funm in self.funcs:
            if fun.name == func_name:
                return fun
        return None
    
class codeGen:
    def __init__(self):
        self.action = None
        self.token = None
        self.function_table = funcss()
        self.symbol_table = SymbolTable()
        self.semantic_stack = []
        self.scope_stack = []
        self.stack = []
        self.top_sp = 0
        self.pb_counter = 0
        self.program_block = []
        self.scope_stack = [1]
        self.reg = 508
        self.lentgh_byte = 4
        self.args_count = 0
        self.temp_return = 0
        self.main_seen = False

        self.program_block.append(f"(ASSIGN, #4, 0, )")
        self.program_block.append("(JP, ?, , )")
        self.pb_counter = 2
        
    def get_addres(self,space = 1):
        address = str(self.reg)
        for _ in range(space):
            self.reg += 4
        return address

    # def add_to_pb(self, part1, part2, part3='', part4=''):
    #     self.program_block[self.pb_counter] = f'({part1}, {part2}, {part3}, {part4})'
    #     self.pb_counter += 1

    def handle_action(self,action,token):
        self.action = action
        self.token = token
        #print(self.semantic_stack)

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
            address = self.get_addres(space=1)   
            temp_symbol = Symbol(name= name,type=temp_type,address=address ,scope=self.scope_stack[(-1)],
                                 type_var='var',no_arguments=0,line_pb=len(self.program_block)-1)
            self.symbol_table.add_symbol(temp_symbol)
            self.program_block.append(f'(ASSIGN, #0, {address}, )')
            self.pb_counter += 1
            print('\n\n----------- define variable -----------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'push_NUM':
            self.push_NUM()
            #print('push num touched with num: ' + self.token)
            #self.symbol_table.print_symbol_table()
            self.program_block.append(f'(ASSIGN, #{int(self.token)}, {self.reg}, )')
            self.pb_counter += 1
            address = self.get_addres(space=1)
            #print("str(self.token): " + str(self.token))
            temp_symbol = Symbol(name= str(self.token) , type='int' ,address=address ,scope=self.scope_stack[-1],
                                 type_var='var',no_arguments=0,line_pb=len(self.program_block)-1)
            self.symbol_table.add_symbol(temp_symbol)
            self.semantic_stack.append(int(self.token))
            #self.symbol_table.print_symbol_table()
            print('\n\n----------- push num -----------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'define_array':
            self.define_array()

            temp_num = self.semantic_stack.pop()
            temp_id = self.semantic_stack.pop()
            temp_type = self.semantic_stack.pop()

            temp_symbol = Symbol(name= temp_id,type=temp_type,address=self.reg ,scope=self.scope_stack[(len(scope_stack) - 1)],
                                 type_var='arr',no_arguments=temp_num,line_pb=len(self.program_block)-1)
            self.reg *= temp_num
            self.symbol_table.add_symbol(temp_symbol)  
            print('\n\n----------- define array -----------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')         


        elif self.action == 'define_function':
            self.define_function()
            print(self.semantic_stack)
            # print('\n\n----------- function defenition -----------')
            # self.symbol_table.print_symbol_table()
            # print('self.semantic_stack: ' + str(self.semantic_stack))
            # print('self.program_block: ' + str(self.program_block) + '\n\n')
            arguments = []
            while self.semantic_stack[-1] != 'startfun':
                arguments.append(self.semantic_stack.pop())
            self.semantic_stack.pop()
            func_name = self.semantic_stack.pop()
            function(func_name , arguments)
            temp_type = self.semantic_stack.pop()
            num_arg = len(arguments) // 3

            if func_name == 'main':
                self.main_seen = True
                self.program_block[1] = str(self.program_block[1]).replace('?' , str(self.pb_counter))
                self.semantic_stack.append(len(self.program_block)-1)

            
            self.scope_stack.append(self.scope_stack[-1] + 1)
            temp_symbol= Symbol(name=func_name, type= temp_type, scope=self.scope_stack[len(self.scope_stack)-1] ,
                                type_var='function',no_arguments=self.reg ,address=int(len(self.program_block)) )
            self.symbol_table.add_symbol(temp_symbol) # [ ... , foo , 2 ,3 ,4 ]

            self.scope_stack.append(self.scope_stack[-1] + 1)
            arguments.reverse()
            for i in range(0,len(arguments),3):
                ty=arguments[i] 
                name= arguments[i+1]
                array = arguments[i+2]

                if  array == 'arr':
                    temp_symbol= Symbol(name=name, type= ty, scope=self.scope_stack[len(self.scope_stack)-1]
                        ,type_var='arr',no_arguments=0,address=int(len(self.program_block)) )
                    self.symbol_table.add_symbol(temp_symbol)
                else:
                    temp_symbol= Symbol(name=name, type= ty, scope=self.scope_stack[len(self.scope_stack)-1]
                        ,type_var='var',no_arguments=0,address=self.reg )
                    self.symbol_table.add_symbol(temp_symbol)
                    self.reg += self.lentgh_byte
                    
            print('\n\n----------- function defenition -----------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'end_of_scope':
            self.end_of_scope()
            self.symbol_table.delete_scope(self.scope_stack.pop())
            print('\n\n----------- end of scope -----------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'start_function_call':
            self.start_function_call()
            print('\n\n------------ start function call -------------')
            self.symbol_table.print_symbol_table()
            #self.semantic_stack.append('start_funcation')
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')
            self.args_count = 0
            


        elif self.action == 'function_call':
            args = [] # [30 , 20]
            self.function_call()
            if self.semantic_stack[-2] == 'output':
                output_value = self.semantic_stack.pop()
                #self.semantic_stack.pop()
                symbol = self.symbol_table.find_address(output_value)
                self.program_block.append(f'(PRINT, {symbol.address}, , )')
                self.pb_counter += 1

            else:
                func_addr = '' #[ ... , foo , 2(20) , 3(30) ]
                for i in range (len(self.semantic_stack)):
                    temp = self.semantic_stack[-i-1]          
                    symbol = self.symbol_table.find_address(str(temp))
                    if symbol != None:
                        if symbol.type_var == 'function':
                            func_addr = symbol.address
                            break
                        else: 
                            print('parameter: ' + str(temp))
                            args.append(symbol.address)
                        #self.program_block.append(f'(ASSIGN, #{int(temp)}, {self.reg}, )')
                        #self.reg += 4
                        #self.pb_counter += 1
                        #self.args_count += 1
                #self.program_block[self.pb_counter - self.args_count] = str(self.program_block[self.pb_counter - self.args_count]).replace('?' , str(self.pb_counter + 1))
                #add args:
                #func = self.funcs.get_function(func_addr)
                # for i in range(len(func.args)):
                #     arg_address = func.args[len(func.args) -i -1]
                #     temp_symbol = self.symbol_table.find_address(self.semantic_stack.pop())
                #     arg_value_address = temp_symbol.address()
                #     self.program_block.append(f'(ASSIGN, {int(arg_value_address)}, {int(arg_address)}, )')
                # func = self.symbol_table.get_func(func_addr)
                # args_addr = func.no_arguments
                #print('func_addr: ' + str(func_addr))
                args_addr = self.symbol_table.get_func(func_addr)
                #print('args_addr: ' + str(args_addr))
                #print('len(args): ' + str(len(args)))
                #print(args)
                for i in range(len(args)):
                    #print('5555555555555555555555555')
                    self.program_block.append(f'(ASSIGN, {int(args.pop())}, {int(args_addr)}, )')
                    self.pb_counter += 1
                    args_addr += 4

                self.program_block.append(f'(ASSIGN, {int(self.pb_counter + 2)}, 500, )')
                self.pb_counter += 1
                self.program_block.append(f'(JP, {func_addr}, , )')
                self.pb_counter += 1
                
                self.semantic_stack.pop()
                self.semantic_stack.pop()
                self.semantic_stack.append(1050)
            print('\n\n------------ function call -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'end_of_function':
            self.end_of_function()
            # print('\n\n------------ end of function 1 -------------')
            # self.symbol_table.print_symbol_table()
            # print('self.semantic_stack: ' + str(self.semantic_stack))
            # print('self.program_block: ' + str(self.program_block) + '\n\n')
            #func_addr = self.semantic_stack.pop()
            if self.main_seen == False:
                self.program_block.append('(JP, @500, , )')
                self.pb_counter += 1
            #a = self.semantic_stack.pop()
            #self.semantic_stack.pop()
            #self.semantic_stack.append(a)
            print('\n\n------------ end of function -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')

        # [ .... , calee_name , caller_address , return_value ]
        # [ .... ,     foo    ,       45       ,      9       ]

        elif self.action == 'push_array_type':
            self.push_array_type()
            self.semantic_stack.append('arr')


        elif self.action == 'push_non_type':
            self.push_non_type()
            self.semantic_stack.append('nothing')


        elif self.action == 'pop':
            self.pop()
            if self.semantic_stack:
                self.semantic_stack.pop()


        elif self.action == 'if':
            self.if_stmt()
            #print('%', self.semantic_stack[-1])
            result_symbol = self.symbol_table.find_address(self.semantic_stack[-1])
            self.semantic_stack.pop()
            self.program_block.append(f'(JPF, {result_symbol.address}, ?, )')
            self.pb_counter += 1
            self.semantic_stack.append(self.pb_counter - 1)
            print('\n\n------------ if -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')
            
            
        elif self.action == 'else':
            #print(self.semantic_stack)
            #self.semantic_stack.pop()
            self.else_stmt()
            self.program_block.append(f'(JP, ?, , )')
            self.pb_counter += 1
            if_line = int(self.semantic_stack[-1])
            self.semantic_stack.pop()
            self.semantic_stack.append(self.pb_counter - 1)
            #print('33333333333333      if_line.name = ' + if_line.name)
            self.program_block[if_line] = self.program_block[if_line].replace('?', str(self.pb_counter))
            print('\n\n------------ else -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'end_if':
            self.end_if()
            # print('\n\n------------ end if  -------------')
            # self.symbol_table.print_symbol_table()
            # print('self.semantic_stack: ' + str(self.semantic_stack))
            # print('self.program_block: ' + str(self.program_block) + '\n\n')
            
            else_line = int((self.semantic_stack[-1]))
            #print('else_line: ' + str(else_line))
            self.semantic_stack.pop()
            self.program_block[else_line] = self.program_block[else_line].replace('?', str(self.pb_counter))
            print('\n\n------------ end if -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'while':
            self.while_stmt()
            #self.code_scope_stack.append(('while', len(self.semantic_stack)))
            self.scope_stack.append(self.scope_stack[-1] + 1)
            self.program_block.append(f"(JP, {self.pb_counter + 2}, , )")
            self.pb_counter += 1
            self.semantic_stack.append(self.pb_counter)
            self.program_block.append("(JP, ?, , )")
            self.pb_counter += 1
            self.semantic_stack.append(self.pb_counter)

            print('\n\n------------ while -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'while_condition':
            self.while_condition()     
            result_symbol = self.symbol_table.find_address(self.semantic_stack[-1])
            #print('result_symbol: ' + result_symbol)
            #print('self.semantic_stack[-2]: ' + self.semantic_stack[-2] )
            self.semantic_stack.pop()
            self.program_block.append(f'(JPF, {result_symbol.address}, ?, )')
            self.pb_counter += 1
            self.semantic_stack.append(self.pb_counter - 1)

            print('\n\n------------ while condition -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'end_while':
            self.end_while()     
            #print(self.semantic_stack)
            condition_line = int(self.semantic_stack[-1])
            beginning_line = int(self.semantic_stack[-2])
            outer_line = int(self.semantic_stack[-3])
            self.semantic_stack = self.semantic_stack[:-3]
            self.program_block.append(f'(JP, {beginning_line}, , )')
            self.pb_counter += 1
            #print('condition line is: ' + str(condition_line))
            self.program_block[condition_line] = self.program_block[condition_line].replace('?', str(self.pb_counter))
            self.program_block[outer_line] = self.program_block[outer_line].replace('?', str(self.pb_counter))
            self.symbol_table.delete_scope(self.scope_stack.pop())

            print('\n\n------------ end while -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'return':
            self.return_stmt()    
            #self.semantic_stack.append('nothing')
            print('\n\n------------ return -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'return_value':
            self.return_value()
            return_value = self.symbol_table.find_result(str(self.semantic_stack.pop()))
            self.program_block.append(f'(ASSIGN, {(return_value.address)}, 504, )')
            self.pb_counter += 1
            self.program_block.append('(JP, @500, , )')
            self.pb_counter += 1
            print('\n\n------------ return value -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')
            #self.semantic_stack.insert(0 , return_value.address)
            # temp_symbol = Symbol(name = f'$return_result{str(self.temp_return)}', type= 'int' , address=504,scope=self.scope_stack[-1],type_var='var'
            #                      ,no_arguments=0,line_pb=0)
            # self.temp_return += 1 
            # self.symbol_table.add_symbol(temp_symbol)
            # self.semantic_stack.append(temp_symbol.name)            


        elif self.action == 'assign':
            self.assign()
            if self.semantic_stack[-1] == 1050:
                self.semantic_stack.pop()
                a = self.symbol_table.find_result(self.semantic_stack.pop())
                self.program_block.append(f"(ASSIGN, 504, {a.address}, )")
                self.pb_counter += 1
            else:   
                print('self.semantic_stack: ' + str(self.semantic_stack))
                a = self.symbol_table.find_address(self.semantic_stack.pop())
                b = self.symbol_table.find_address(self.semantic_stack[-1])
                self.program_block.append(f"(ASSIGN, {a.name}, {b}, )")
                self.pb_counter += 1
            print('\n\n------------ assign -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')
            

        elif self.action == 'find_array_address':
            self.find_array_address()   
            a = self.symbol_table.find_address(self.self.semantic_stack.pop())
            b = self.symbol_table.find_address(self.self.semantic_stack.pop())

            address = self.get_addres(space=1)
            
            temp_symbol = Symbol(name = '$result' , address=address,scope=self.scope_stack[-1],type_var='var'
                                 ,no_arguments=0,line_pb=0) 
            self.symbol_table.add_symbol(temp_symbol)
            self.semantic_stack.append(temp_symbol.name)
            
            self.program_block.append(f"(ADD, {b.address}, {a.address}, @{address})")
            self.pb_counter += 1

            print('\n\n------------ find array address -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'relop':
            self.relop() 
            #self.symbol_table.print_symbol_table()
            # print('self.semantic_stack: ' + str(self.semantic_stack))
            # print('self.program_block: ' + str(self.program_block) + '\n\n')
            b = self.symbol_table.find_address(str(self.semantic_stack.pop()))
            op = (self.semantic_stack.pop())
            a = self.symbol_table.find_address(str(self.semantic_stack.pop()))

            address = self.get_addres(space=1)
            # print('a: ' + str(a))
            # print('b: ' + str(b))
            self.program_block.append(f'({op}, {a.address}, {b.address}, {address})')
            self.pb_counter += 1
            
            temp_symbol = Symbol(name = '$result', type= 'int' , address=address,scope=self.scope_stack[-1],type_var='var'
                                 ,no_arguments=0,line_pb=0) 
            self.symbol_table.add_symbol(temp_symbol)
            self.semantic_stack.append(temp_symbol.name)

            print('\n\n------------ relop -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')
            # self.symbol_table.print_symbol_table()
            # print('self.semantic_stack: ' + str(self.semantic_stack))
            # print('self.program_block: ' + str(self.program_block) + '\n\n')   
            # b = self.semantic_stack.pop()
            # print('b= ' + str(b))
            # relation = self.semantic_stack.pop()
            # a = self.symbol_table.find_address(self.semantic_stack.pop())
            # address = self.get_addres(space=1)
            # temp_symbol = Symbol(name = '$relop_result' , type= 'int' , address=address ,scope=self.scope_stack[-1],type_var='var'
            #                      ,no_arguments=0,line_pb=0) 
            # print('a.name= ' + str(a.name))
            # if relation == 'LT':
            #     if int(a.name) < int(b):
            #         temp_symbol.name = '1'
            #     else:
            #         temp_symbol.name = '0'
            # else:
            #     if int(a.name) == int(b):
            #         temp_symbol.name = '1'
            #     else:
            #         temp_symbol.name = '0'
            # self.semantic_stack.append(temp_symbol.name)
            

        elif self.action == 'LT':
            self.LT()
            self.semantic_stack.append('LT') 


        elif self.action == 'EQ':
            self.EQ()      
            self.semantic_stack.append('EQ')


        elif self.action == 'add_or_sub':
            self.add_or_sub()     
            a = self.symbol_table.find_address(str(self.semantic_stack.pop()))
            op =(self.semantic_stack.pop())
            b = self.symbol_table.find_address(str(self.semantic_stack.pop()))

            address = self.get_addres(space=1)

            self.program_block.append(f'({op}, {a.address}, {b.address}, {address})')
            self.pb_counter += 1
            
            temp_symbol = Symbol(name = '$result', type= 'int' , address=address,scope=self.scope_stack[-1],type_var='var'
                                 ,no_arguments=0,line_pb=0) 
            self.symbol_table.add_symbol(temp_symbol)
            self.semantic_stack.append(temp_symbol.name)

            print('\n\n------------ add or sub -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'add':
            self.add()    
            self.semantic_stack.append('ADD')


        elif self.action == 'sub':
            self.sub()    
            self.semantic_stack.append('SUB')


        elif self.action == 'mult':
            self.mult()    
            a = self.symbol_table.find_address(self.semantic_stack.pop())
            b = self.symbol_table.find_address(self.semantic_stack.pop())

            address = self.get_addres(space=1)

            self.program_block.append(f'(MULT, {a.address}, {b.address}, {address})')
            self.pb_counter += 1
            
            temp_symbol = Symbol(name = '$result' , address=address,scope=self.scope_stack[-1],type_var='var'
                                 ,no_arguments=0,line_pb=0) 
            self.symbol_table.add_symbol(temp_symbol)
            self.semantic_stack.append(temp_symbol.name)

            print('\n\n------------ mult -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')


        elif self.action == 'negate':
            self.negate()  
            a = self.semantic_stack.pop()
            self.semantic_stack.append(str(-a))

            print('\n\n------------ negate -------------')
            self.symbol_table.print_symbol_table()
            print('self.semantic_stack: ' + str(self.semantic_stack))
            print('self.program_block: ' + str(self.program_block) + '\n\n')

    def save_program(self):
        with open('output.txt', 'w') as f:
            for i in range(len(self.program_block)):
                f.write(f'{i}\t{self.program_block[i]}\n')


            











































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
    

