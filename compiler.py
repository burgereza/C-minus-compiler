#Compiler Project - Sharif University Of Technology - Fall 2023
#Farid Fotuhi 98110073
#Reza Ghamghaam 99170542

from scanner import scanner
from parser1 import LL1Parser
if __name__ == '__main__':
    #myscanner = scanner('input.txt')
    #myscanner.run()
    myprser = LL1Parser()
    myprser.run_parser()
    myprser.write_syntax_errors('seynax_errors.txt')
    myprser.write_tree('parse_tree.txt')