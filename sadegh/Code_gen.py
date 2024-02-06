class Code_gen:
    def __init__(self):
        #self.parser = parser
        self.semantic_stack = []
        self.scope_stack = []
        self.scope_stack.append(0)
        self.scope = 1
        self.symbol_table = []
        self.program_line = 0
        self.data_block_line = 1000
        self.temp_block_line = 3000
        self.program = []
        self.number_of_open_assignment = 0
        self.semantic_errors = []
        self.current_method_params = []
        self.current_called_method_params = []
        self.current_method_params_pointers = []
        self.return_address = 5004
        self.stackPointer_address = 5008
        self.stack_machine_start_point = 5012
        self.function_assigns = []

    def symbol_table_insert(self, lexeme , func_var_array , array_size , 
                            type , scope ):
        if lexeme in self.symbol_table:
            print("Error: Redeclaration of variable " + lexeme)
        else:
            self.symbol_table.append(
                [lexeme, func_var_array , array_size , type , scope , self.data_block_line])
            self.data_block_line += array_size * 4

    def symbol_table_lookup(self, lexeme, line_number):
        for i in range(len(self.symbol_table)):
            if self.symbol_table[len(self.symbol_table)-1-i][0] == lexeme:
                return (len(self.symbol_table)-1-i)
        self.semantic_errors.append("#"+ str(line_number) + ": Semantic Error! " + "\'" + lexeme +"\' is not defined.")
        return 0

    def symbol_table_lookup_by_data_block_line(self, data_block_line):
        for i in range(len(self.symbol_table)):
            try:
                if int(self.symbol_table[i][5]) == int(data_block_line):
                    return self.symbol_table[i]
            except:
                pass
        return "Not Found"
            

    def write_program(self):
        if len(self.semantic_errors) == 0:
            with open("output.txt", "w") as txt_file:
                for i in range(len(self.program)):
                    txt_file.write(str(i) + "\t" + self.program[i] + "\n")
            with open("semantic_errors.txt","w") as txt_file:
                txt_file.write("The input program is semantically correct.")
        else:
            with open("output.txt", "w") as txt_file:
                txt_file.write("The output code has not been generated.")

            with open("semantic_errors.txt","w") as txt_file:
                for error in self.semantic_errors:
                    txt_file.write(error + "\n")
            
    
    
    def write_method(self,method_name, token , line_number):
        if method_name == "#j_main":
            # assign the first address of the stack to stack pointer
            self.program.append("(ASSIGN, " + "#" + str(self.stack_machine_start_point) + ", " + str(self.stackPointer_address) + ",   )")
            self.program_line += 1

            # assign default value to the first address of the stack
            self.program.append("(ASSIGN, " + "#0" + ", " + str(self.stack_machine_start_point) + ",   )")
            self.program_line += 1
            
            # self.semantic_stack.append(self.program_line)
            # self.program.append("")
            # self.program_line += 1

        elif method_name == "#p_input":
            self.semantic_stack.append(token)

        elif method_name == "#dec_id":
            self.semantic_stack.append(token)
    
        elif method_name == "#dec_var":
            var_lexeme = self.semantic_stack.pop()
            var_type = self.semantic_stack.pop()
            if var_type == "void":
                self.semantic_errors.append("#"+ str(line_number) + ": Semantic Error! Illegal type of void for \'" + var_lexeme + "\'.")
            var_scope = self.scope
            self.symbol_table_insert(var_lexeme , "var" , 1 , var_type , var_scope)

        elif method_name == "#dec_array":
            array_size = int(token)
            array_lexeme = self.semantic_stack.pop()
            array_type = self.semantic_stack.pop()
            array_scope = self.scope
            self.symbol_table_insert(array_lexeme , "array" , array_size , array_type , array_scope)
        
        elif method_name == "#start_func_scope":
            # check if this function is main 

            # if self.semantic_stack[-1] == "main":
            #     self.program[self.semantic_stack[0]] = \
            #         "(JP, " + str(self.program_line + 2) + ",  ,   )"    
            
            # declare function in symbol table
            func_lexeme = self.semantic_stack.pop()
            func_type = self.semantic_stack.pop()
            func_scope = self.scope
            self.scope = self.scope + 1
            self.symbol_table_insert(func_lexeme , "func" , 1 , func_type , func_scope)
            self.scope_stack.append(len(self.symbol_table))

            # put function label address in data block
            function_data = self.symbol_table[self.symbol_table_lookup(func_lexeme)]
            self.program.append(
                "(ASSIGN, " + "#" + str(self.program_line + 2) + ", " + str(function_data[5]) + ",   )")
            self.program_line += 1

            # save jump line for function
            if func_lexeme != "main":
                self.semantic_stack.append(self.program_line)
                self.program.append("")
                self.program_line += 1
            else:
                self.semantic_stack.append("main")





        elif method_name == "#end_func_params":
            start_line_of_symbol_table = self.scope_stack[-1]
            function_data = self.symbol_table[start_line_of_symbol_table - 1]
            number_of_params = len(self.current_method_params)
            params = self.current_method_params.copy()
            self.current_method_params = []
            new_function_data = [function_data[0], function_data[1], function_data[2] ,
                                  function_data[3], function_data[4], function_data[5],
                                    number_of_params, params]
            self.symbol_table[start_line_of_symbol_table - 1] = new_function_data



        elif method_name == "#end_func_scope":
            # pop n
            # pop the value of n
            # get temp for value of n
            temp_value = self.temp_block_line
            self.temp_block_line += 4
            self.program.append(
                "(ASSIGN, " + "@" + str(self.stackPointer_address) + ", " + str(temp_value) + ",   )")
            self.program_line += 1
            # move the stack pointer
            self.program.append(
                "(SUB, " + str(self.stackPointer_address) + ", " + "#4" + ", " + str(self.stackPointer_address) + " )")
            self.program_line += 1
            # pop the address of the n
            temp_address = self.temp_block_line
            self.temp_block_line += 4
            self.program.append(
                "(ASSIGN, " + "@" + str(self.stackPointer_address) + ", " + str(temp_address) + ",   )")
            self.program_line += 1
            # move the stack pointer
            self.program.append(
                "(SUB, " + str(self.stackPointer_address) + ", " + "#4" + ", " + str(self.stackPointer_address) + " )")
            self.program_line += 1
            # assign value to the address of n
            self.program.append(
                "(ASSIGN, " + str(temp_value) + ", " + "@" + str(temp_address) + ",   )")
            self.program_line += 1

            # jump back to the caller
            # pop the value of the stack pointer
            temp_add = self.temp_block_line
            self.temp_block_line += 4
            self.program.append(
                "(ASSIGN, " + "@" + str(self.stackPointer_address) + ", " + str(temp_add) + ",   )")
            self.program_line += 1
            # move the stack pointer
            self.program.append(
                "(SUB, " + str(self.stackPointer_address) + ", " + "#4" + ", " + str(self.stackPointer_address) + " )")
            self.program_line += 1
            # jump to the temp address
            self.program.append(
                "(JP, " + "@" + str(temp_add) + ",  ,   )")
            self.program_line += 1
            

            # write jump to end of function
            program_line = self.semantic_stack.pop()
            if str(program_line) != "main":
                self.program[program_line] = "(JP, " + str(self.program_line) + ",  ,   )"

            # end function scope
            self.scope = self.scope - 1
            start_line_of_symbol_table = self.scope_stack.pop()
            self.symbol_table = self.symbol_table[:start_line_of_symbol_table]

        elif method_name == "#dec_param":
            var_lexeme = self.semantic_stack.pop()
            var_type = self.semantic_stack.pop()
            # append var type to current method params
            self.current_method_params.append(var_type)
            var_scope = self.scope
            # why param ?
            self.symbol_table_insert(var_lexeme , "param" , 1 , var_type , var_scope)


        elif method_name == "#dec_array_for_func":
            array_lexeme = self.semantic_stack.pop()
            array_type = self.semantic_stack.pop()
            # append array type to current method params
            self.current_method_params.append("array")
            array_scope = self.scope
            self.symbol_table_insert(array_lexeme , "array_param" , 1 , array_type , array_scope)
            
        elif method_name == "#jp_break_save":
            # jump to first line before repeat
            i = 1

            while True:
                try:
                    if self.semantic_stack[-i] < len(self.program):
                        if self.program[self.semantic_stack[-i]] == "break":
                            break
                    i += 1
                except:
                    self.semantic_errors.append("#"+ str(line_number) + ": Semantic Error! No 'repeat ... until' found for 'break'.")
                    i = 1
                    break
            
            self.program.append("(JP, " + str(self.semantic_stack[-i]) + ",  ,   )")
            self.program_line += 1
        
        elif method_name == "#save_if":
            # save jump line for if
            self.semantic_stack.append(self.program_line)
            self.program.append("")
            self.program_line += 1

        elif method_name == "#jp_save_else":
            # jump to end of if
            program_line = self.semantic_stack.pop()
            value_address = self.semantic_stack.pop()
            self.program[program_line] = "(JPF, " + str(value_address) + ", " + str(self.program_line + 1) + ",   )"
            # save jump line for else
            self.semantic_stack.append(self.program_line)
            self.program.append("")
            self.program_line += 1

        elif method_name == "#jp_else":
            program_line = self.semantic_stack.pop()
            try:
                self.program[program_line] = "(JP, " + str(self.program_line) + ",  ,   )"
            except:
                program_line = self.semantic_stack.pop()
                self.program[program_line] = "(JP, " + str(self.program_line) + ",  ,   )"

    
        elif method_name == "#start_repeat_scope":
            # jump one line
            self.program.append("(JP, " + str(self.program_line + 2) + ",  ,   )")
            self.program_line += 1

            # save jump line for breaks 
            self.semantic_stack.append(self.program_line)
            self.program.append("break")
            self.program_line += 1

            # new scope for repeat
            self.scope = self.scope + 1
            self.scope_stack.append(len(self.symbol_table))

        elif method_name == "#end_repeat_scope":
            # end repeat scope
            self.scope = self.scope - 1
            start_line_of_symbol_table = self.scope_stack.pop()
            self.symbol_table = self.symbol_table[:start_line_of_symbol_table]
            
        elif method_name == "#jp_repeat":
            value_address = self.semantic_stack.pop()
            program_line = self.semantic_stack[-1] + 1
            self.program.append("(JPF, " + str(value_address) + ", " + str(program_line) + ",   )")
            self.program_line += 1


        elif method_name == "#jp_break":
            program_line = self.semantic_stack.pop()
            self.program[program_line] = "(JP, " + str(self.program_line) + ",  ,   )"

        elif method_name == "#p_id":
            if token == "output":
                self.semantic_stack.append(token)
            else:
                # push data address of variable in semantic stack
                var_data = self.symbol_table[self.symbol_table_lookup(token)]
                if var_data[1] == "array_param":
                    self.semantic_stack.append("A" + str(var_data[5]))
                else:
                    self.semantic_stack.append(str(var_data[5]))
                            
        elif method_name == "#p_num":
            # get temp address for number
            temp_address = self.temp_block_line
            self.temp_block_line += 4
            self.semantic_stack.append(temp_address)
            # put number in data block
            self.program.append(
                "(ASSIGN, " + "#" + str(token) + ", " + str(temp_address) + ",   )")
            self.program_line += 1


        elif method_name == "#assign":
            value_address = self.semantic_stack.pop()
            data_address = self.semantic_stack.pop()
            self.program.append(
                "(ASSIGN, " + str(value_address) + ", " + str(data_address) + ",   )")
            
            self.program_line += 1
            self.number_of_open_assignment -= 1
            if self.number_of_open_assignment > 0:
                self.semantic_stack.append(value_address)
            


        elif method_name == "#increase_assign":
            self.number_of_open_assignment += 1
        
        elif method_name == "#array_address":
            index_address = self.semantic_stack.pop()
            # multiply index by 4 in code 
            new_temp_address = self.temp_block_line
            self.temp_block_line += 4
            self.program.append(
                "(MULT, " + str(index_address) + ", " + "#4" + ", " + str(new_temp_address) + ")")
            self.program_line += 1

            base_address = self.semantic_stack.pop()
            if base_address[0] == "A":
                # TOF
                self.program.append(
                    "(ADD, " + str(new_temp_address) + ", " + str(base_address[1:]) + ", " + str(new_temp_address) + ")")
            else:
                self.program.append(
                    "(ADD, " + str(new_temp_address) + ", #" + str(base_address) + ", " + str(new_temp_address) + ")")
                
            # add index to array address

            self.program_line += 1

            self.semantic_stack.append("@"+ str(new_temp_address))
  

        
        # elif method_name == "#assign_array":
        #     value_address = self.semantic_stack.pop()
        #     indirect_address = self.semantic_stack.pop()
        #     self.program.append(
        #         "(ASSIGN, " + str(value_address) + ", @" + str(indirect_address) + ",   )")


            
        elif method_name == "#bool_op":
            second_operand = self.semantic_stack.pop()
            operation_type = self.semantic_stack.pop()
            first_operand = self.semantic_stack.pop()

            if operation_type == "==" :
                # get temp address for result
                temp_address = self.temp_block_line
                self.temp_block_line += 4
                self.semantic_stack.append(temp_address)
                self.program.append(
                    "(EQ, " + str(first_operand) + ", " + str(second_operand) + ", " + str(temp_address) + ")")
                self.program_line += 1
            elif operation_type == "<" :
                # get temp address for result
                temp_address = self.temp_block_line
                self.temp_block_line += 4
                self.semantic_stack.append(temp_address)
                self.program.append(
                    "(LT, " + str(first_operand) + ", " + str(second_operand) + ", " + str(temp_address) + ")")
                self.program_line += 1
            
        elif method_name == "#add":
            second_operand = self.semantic_stack.pop()
            operation_type = self.semantic_stack.pop()
            first_operand = self.semantic_stack.pop()

            if operation_type == "+" :
                # get temp address for result
                temp_address = self.temp_block_line
                self.temp_block_line += 4
                self.semantic_stack.append(temp_address)
                self.program.append(
                    "(ADD, " + str(first_operand) + ", " + str(second_operand) + ", " + str(temp_address) + ")")
                self.program_line += 1
            elif operation_type == "-" :
                # get temp address for result
                temp_address = self.temp_block_line
                self.temp_block_line += 4
                self.semantic_stack.append(temp_address)
                self.program.append(
                    "(SUB, " + str(first_operand) + ", " + str(second_operand) + ", " + str(temp_address) + ")")
                self.program_line += 1
        
        elif method_name == "#mult":
            second_operand = self.semantic_stack.pop()
            first_operand = self.semantic_stack.pop()
            # get temp address for result
            temp_address = self.temp_block_line
            self.temp_block_line += 4
            self.semantic_stack.append(temp_address)
            self.program.append(
                "(MULT, " + str(first_operand) + ", " + str(second_operand) + ", " + str(temp_address) + ")")
            self.program_line += 1

        elif method_name == "#check_func":
            # check if the name of the function is output
            function_address = self.semantic_stack.pop()
            if function_address == "output":
                self.program.append("(PRINT, " + str(self.current_method_params_pointers[0]) + ",  ,   )")
                self.program_line += 1
                self.current_called_method_params = []
                self.current_method_params_pointers = []
            else:
                function_data = self.symbol_table_lookup_by_data_block_line(function_address)
                if function_data == "Not Found":
                    return
                function_params = function_data[7]
                function_params_number = function_data[6]
                function_data_line = function_data[5] + 4
                # check if the number of params is correct
                if len(self.current_called_method_params) != function_params_number:
                    self.semantic_errors.append("#"+ str(line_number) 
                                                +": Semantic Error! Mismatch in numbers of arguments of \'"
                                                  + function_data[0] + "\'.")
                    if function_data[3] != "void" :
                        self.semantic_stack.append(self.return_address)
                    self.current_called_method_params = []
                    self.current_method_params_pointers = []

                else:
                    for i in range(len(self.current_called_method_params)):
                        if self.current_called_method_params[i] != function_params[i]:
                            self.semantic_errors.append("#"+ str(line_number)
                                                        +": Semantic Error! Mismatch in type of argument " + str(i+1)
                                                        +" of \'"+ function_data[0] + "\'." +
                                                         " Expected \'" + function_params[i] +  "\' but got \'" +
                                                         self.current_called_method_params[i] +  "\' instead.")
                        else:
                            if self.current_called_method_params[i] == "array":
                                # check if it is a pointer or a address
                                # find the data from the symbol table
                                param_data = self.symbol_table_lookup_by_data_block_line(self.current_method_params_pointers[i])
                                if param_data == "Not Found":
                                    5/0
                                if param_data[1] == "array":
                                    self.program.append("(ASSIGN, " +"#"+ str(self.current_method_params_pointers[i]) + ", " + str(function_data_line) + ",   )")
                                    self.program_line += 1
                                    function_data_line += 4
                                elif param_data[1] == "array_param":
                                    self.program.append("(ASSIGN, " + str(self.current_method_params_pointers[i]) + ", " + str(function_data_line) + ",   )")
                                    self.program_line += 1
                                    function_data_line += 4
                            else:
                                self.program.append("(ASSIGN, " + str(self.current_method_params_pointers[i]) + ", " + str(function_data_line) + ",   )")
                                self.program_line += 1
                                function_data_line += 4

                    # add 4 to the stack pointer 
                    self.program.append("(ADD, " + str(self.stackPointer_address) + ", " + "#4" + ", " + str(self.stackPointer_address) + ")")
                    self.program_line += 1

                    #push the return line to the machine stack
                    self.program.append("(ASSIGN, " + "#" +  str(self.program_line + 2) + ", " + "@" + str(self.stackPointer_address) + ")")
                    self.program_line += 1


                    # push n to the machine stack
                        # add 4 to the stack pointer 
                    self.program.append("(ADD, " + str(self.stackPointer_address) + ", " + "#4" + ", " + str(self.stackPointer_address) + ")")
                    self.program_line += 1
                        # push the n address to the machine stack
                    self.program.append("(ASSIGN, " + "#" +  str(function_data_line) + ", " + "@" + str(self.stackPointer_address) + ")")
                    self.program_line += 1


                        # add 4 to the stack pointer 
                    self.program.append("(ADD, " + str(self.stackPointer_address) + ", " + "#4" + ", " + str(self.stackPointer_address) + ")")
                    self.program_line += 1
                        # push the n value to the machine stack
                    self.program.append("(ASSIGN, " + str(function_data_line) + ", " + "@" + str(self.stackPointer_address) + ")")
                    self.program_line += 1



                    # call the function
                    self.program.append("(JP, " + "@" + str(function_data[5]) + ",  ,   )")
                    self.program_line += 1

                    # return address
                    if function_data[3] != "void" :
                        # get temp address for result
                        temp_address = self.temp_block_line
                        self.temp_block_line += 4
                        # assign the return value to the temp address
                        self.program.append("(ASSIGN, "  + str(self.return_address) + ", " + str(temp_address) + ",   )")
                        self.program_line += 1
                        self.semantic_stack.append(temp_address)

                    self.current_called_method_params = []
                    self.current_method_params_pointers = []


        elif method_name ==  "#assign_param":
            obj = self.semantic_stack.pop()
            try:
                if obj[0] == "A":
                    obj = int(obj[1:])
                else:
                    obj = int(obj)
                data_obj = self.symbol_table_lookup_by_data_block_line(obj)
                if data_obj == "Not Found":
                    self.current_called_method_params.append("int")
                    self.current_method_params_pointers.append(obj)
                else:
                    obj_type = data_obj[1]
                    if obj_type == "var" or obj_type == "param" or obj_type == "func":
                        self.current_called_method_params.append("int")
                        self.current_method_params_pointers.append(obj)
                    elif obj_type == "array" or obj_type == "array_param":
                        self.current_called_method_params.append("array")
                        self.current_method_params_pointers.append(obj)
            except:
                    self.current_called_method_params.append("int")
                    self.current_method_params_pointers.append(obj)
        
        elif method_name == "#check_operand_type":
            address = self.semantic_stack[-1]
            data = self.symbol_table_lookup_by_data_block_line(address)
            data_type = data[1]
            if data_type == "array":
                self.semantic_errors.append("#"+ str(line_number)
                                                +": Semantic Error! Type mismatch in operands, Got array instead of int.")

        elif method_name == "#return":
            value_address = self.semantic_stack.pop()
            # assign the value to the return address
            self.program.append("(ASSIGN, " + str(value_address) + ", " + str(self.return_address) + ",   )")
            self.program_line += 1

        elif method_name == "#jp_return":
            # pop n
            # pop the value of n
            # get temp for value of n
            temp_value = self.temp_block_line
            self.temp_block_line += 4
            self.program.append(
                "(ASSIGN, " + "@" + str(self.stackPointer_address) + ", " + str(temp_value) + ",   )")
            self.program_line += 1
            # move the stack pointer
            self.program.append(
                "(SUB, " + str(self.stackPointer_address) + ", " + "#4" + ", " + str(self.stackPointer_address) + " )")
            self.program_line += 1
            # pop the address of the n
            temp_address = self.temp_block_line
            self.temp_block_line += 4
            self.program.append(
                "(ASSIGN, " + "@" + str(self.stackPointer_address) + ", " + str(temp_address) + ",   )")
            self.program_line += 1
            # move the stack pointer
            self.program.append(
                "(SUB, " + str(self.stackPointer_address) + ", " + "#4" + ", " + str(self.stackPointer_address) + " )")
            self.program_line += 1
            # assign value to the address of n
            self.program.append(
                "(ASSIGN, " + str(temp_value) + ", " + "@" + str(temp_address) + ",   )")
            self.program_line += 1

            # jump back to the caller
            # pop the value of the stack pointer
            temp_add = self.temp_block_line
            self.temp_block_line += 4
            self.program.append(
                "(ASSIGN, " + "@" + str(self.stackPointer_address) + ", " + str(temp_add) + ",   )")
            self.program_line += 1
            # move the stack pointer
            self.program.append(
                "(SUB, " + str(self.stackPointer_address) + ", " + "#4" + ", " + str(self.stackPointer_address) + " )")
            self.program_line += 1
            # jump to the temp address
            self.program.append(
                "(JP, " + "@" + str(temp_add) + ",  ,   )")
            self.program_line += 1

        elif method_name == "#delete_j_main":
            # delete the last jump 
            self.program.pop()



        
            


# function call : just rewrite in the memory
# the array size in function params is fixed 
# operands should be int unless it is a assignment (how to assign a array pointer to another one ?)
# not dec var if type is void 
# fixed point for return value 
# jump back stack 
