#Compiler Project - Sharif University Of Technology - Fall 2023
#Farid Fotuhi 98110073
#Reza Ghamghaam 99170542

from scanner import scanner
from parser2 import LL1Parser2
if __name__ == '__main__':
    #myscanner = scanner('input.txt')
    #myscanner.run()
    myprser = LL1Parser2()
    myprser.run_parser()
    myprser.write_tree()
    myprser.write_syntax_errors()