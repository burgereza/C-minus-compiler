class Symbol:
    def __init__(self, lexeme, type, address, scope, type_var ,no_arguments=0,line_pb=0):
        self.name = lexeme
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

    def find_address(self, symbol_name):
        for symbol in self.symbols:
            if symbol.name == symbol_name:
                return symbol
        return None

    def get_temp(self):
        self.start_temp += self.byte_length
        return self.start_temp - self.byte_length

    def delete_scope(self, scope):
        for symbol in self.symbols:
            if symbol.scope == scope:
                self.symbols.remove(symbol)

    def get_global(self):
        self.start_data += self.byte_length
        return self.start_data - self.byte_length

    def make_space(self, value):
        self.start_data += int(value) * self.byte_length
        return self.start_data - int(value) * self.byte_length

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    def print_symbol_table(self):
        print('------------  symbol table -----------')
        for symbol in self.symbols:
            print('symbol.name: ' + symbol.name + ' symbol.type: ' + symbol.type)
