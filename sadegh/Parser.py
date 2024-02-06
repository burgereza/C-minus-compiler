# Amir Hosein Rahmati 99103922
# Saba Shamekhi 99170489

import json
import anytree
import scanner
import Code_gen



class Parser:
    def __init__(self, scanner):
        self.code_gen = Code_gen.Code_gen(self)
        self.scanner = scanner
        self.token_type, self.token = None , None
        self.first = {}
        self.follow = {}
        self.diagrams = {}
        self.load_dicts()
        self.parent = anytree.Node("Program")
        self.errors = []        
        self.finished = False
        self.is_last_one = True
    
    def get_next_token(self):
        self.token_type, self.token = self.scanner.get_next_token()
        while (self.token_type == "comment" or self.token_type == "whitespace"):
            self.token_type, self.token = self.scanner.get_next_token()
    
    def get_lookahead(self):
        if self.token_type in ["SYMBOL" , "KEYWORD"]:
            return self.token
        else:
            return self.token_type

    def load_dicts(self):
        # load json files 
        with open("./json/" + "first.json", "r") as json_file:
            self.first = json.load(json_file)
        with open("./json/" + "follow.json", "r") as json_file:
            self.follow = json.load(json_file)
        with open("./json/" + "diagrams.json", "r") as json_file:
            self.diagrams = json.load(json_file)


    def go_through(self, NT):
        if self.finished :
            return True
        if self.get_lookahead() in self.first[NT] or \
            (self.get_lookahead() in self.follow[NT] and "epsilon" in self.diagrams[NT]):
            
            if self.get_lookahead() in self.first[NT]:
                NT_diagram = self.diagrams[NT][self.get_lookahead()]
            else:
                NT_diagram = self.diagrams[NT]["epsilon"]

            if len(NT_diagram) == 0 :
                node = anytree.Node("epsilon", parent = self.parent)

            # go into diagram
            for i in range(len(NT_diagram)):
                # check if the NT_diagram i starts with #

                if NT_diagram[i][0] == "#":
                    self.code_gen.write_method(NT_diagram[i])
                    continue

                if NT_diagram[i] in self.diagrams:
                    node = anytree.Node(NT_diagram[i], parent = self.parent)
                    # add the node to the parse tree and change the parent
                    parent = self.parent
                    self.parent = node
                    # go into the diagram
                    status = self.go_through(NT_diagram[i])

                    while(not status):
                        status = self.go_through(NT_diagram[i])
                    
                    self.parent = parent
                    if self.finished :
                        return True 
                else:
                    if self.get_lookahead() == NT_diagram[i]:
                        if (self.token != "$"):
                            node = anytree.Node("(" + self.token_type + ", " + self.token + ")", parent = self.parent)
                        else:
                            node = anytree.Node(self.token, parent = self.parent)
                        # add the node to the parse tree 
                        self.get_next_token()
                    else:
                        # missing NT_diagram[i] on line self.scanner.line_number
                        if self.get_lookahead() != "$":
                            error = "#" + str(self.scanner.get_line_number()) + " : syntax error, missing " + NT_diagram[i]
                            self.errors.append(error)
                        else:
                            self.finished = True
                            error = "#" + str(self.scanner.get_line_number()) + " : syntax error, Unexpected EOF"
                            self.errors.append(error)

        else:
            if self.get_lookahead() in self.follow[NT]:
                # missing NT on line self.scanner.line_number
                error = "#" + str(self.scanner.get_line_number()) + " : syntax error, missing " + NT
                self.errors.append(error)
                self.parent.parent = None
            else:
                # illegal token on line self.scanner.line_number
                if self.get_lookahead() != "$":
                    error = "#" + str(self.scanner.get_line_number()) + " : syntax error, illegal " + self.get_lookahead()
                    self.errors.append(error)
                    self.get_next_token()
                    return False
                else :
                    self.finished = True
                    error = "#" + str(self.scanner.get_line_number()) + " : syntax error, Unexpected EOF"
                    self.errors.append(error)
                    self.parent.parent = None
                    return False

        return True
    
    def make_parse_tree_txt(self):
        with open(self.scanner.path + "parse_tree.txt", "w") as txt_file:
            txt_file.write(anytree.RenderTree(self.parent).by_attr())
    def make_errors_txt(self):
        with open(self.scanner.path + "syntax_errors.txt", "w") as txt_file:
            if len(self.errors) == 0 :
                txt_file.write("There is no syntax error.")
            for i in range(len(self.errors)):
                error = self.errors[i]
                if i == len(self.errors) -1 :
                    txt_file.write(error)
                else:
                    txt_file.write(error + "\n")


    def parse(self):
        self.get_next_token()
        self.go_through("Program")
        self.make_parse_tree_txt()
        self.make_errors_txt()
        self.code_gen.write_program()




