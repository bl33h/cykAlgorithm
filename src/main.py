#Copyright (C), 2023-2024, bl33h
#FileName: main
#Author: Sara Echeverria, Melissa Perez, Alejandro Ortega
#Version: I
#Creation: 18/10/2023
#Last modification: 29/10/2023

import json
from Chomsky import *
from CYK import *

if __name__ == "__main__":
    # Specify the file path for the grammar json
    file_path = "src/input.json"
    
    # Load the json file
    with open(file_path, "r") as grammar_file:
        grammar = json.load(grammar_file)


    #-----CNF Converter-----
    # Create an instance of the CNFCoverter with the read gammar
    converter = CNFConverter(grammar)

    # Convert the grammar
    cnf_grammar = converter.convert()

    # prints the CNF grammar
    print(json.dumps(cnf_grammar, indent=4))
    

    #-----CYK Parser-----
    grammar_file_path = "src/input.json"
    
    with open(grammar_file_path, "r") as grammar_file:
        grammar_json = json.load(grammar_file)
    
    cyk_parser = CYKParser(grammar_json)
    sentence = "he cooks with a knife"
    result = cyk_parser.parse(sentence)
    
    print(f"Accepted: {result}")
    if result:
        print(f"The sentence '{sentence}' is in the language.")
    else:
        print(f"The sentence '{sentence}' is not in the language.")