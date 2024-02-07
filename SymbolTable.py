class Symbol:
    def __init__(self, name, type, address, scope, type_var ,no_arguments=0,line_pb=0):
        self.name = name
        self.type = type
        self.address = address
        self.scope = scope
        self.no_arguments = no_arguments
        self.line_pb = 0
        self.type_var = type_var


class SymbolTable:
    def __init__(self):
        self.symbols = list()
        self.start_data = 500
        self.byte_length = 4
        #self.line_no = 0

    def find_result(self, result):
        l = len(self.symbols) 
        for i in range(l):
            temp_symbol = self.symbols[l-i]
            if temp_symbol.name == str(result):
                #del self.symbols[l-i]
                return temp_symbol
        return None

    def find_address(self, symbol_name):
        for symbol in self.symbols:
            if symbol.name == symbol_name:
                return symbol
        return None

    def delete_scope(self, scope):
        for symbol in self.symbols:
            if symbol.scope == scope:
                self.symbols.remove(symbol)

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    def print_symbol_table(self):
        print('------------  symbol table -----------')
        for symbol in self.symbols:
            print('symbol.name: ' + str(symbol.name) + '   symbol.address: ' + str(symbol.address))
        print('--------------------------------------')

    def get_func(self , addr):
        for symbol in self.symbols:
            if symbol.address == addr:
                return symbol.no_arguments
