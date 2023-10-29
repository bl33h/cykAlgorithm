#Copyright (C), 2023-2024, bl33h
#FileName: main
#Author: Sara Echeverria, Melissa Perez, Alejandro Ortega
#Version: I
#Creation: 18/10/2023
#Last modification: 29/10/2023

import json
import time
from Chomsky import *
from CYK import *
from ParseTree import *

if __name__ == "__main__":
    #-----CFG file-----
    # Load the json file
    with open("src/input.json", "r") as grammar_file:
        grammar = json.load(grammar_file)


    #-----CNF Converter-----
    # Create an instance of the CNFCoverter with the read gammar
    converter = CNFConverter(grammar)

    # Convert the grammar
    cnf_grammar = converter.convert()

    # prints the CNF grammar
    print(json.dumps(cnf_grammar, indent=4))
    
    #time starts to count
    start = time.time()
    #-----Converted grammar file-----
    with open("src/input.json", "r") as convertedGrammar_file:
        converterGrammar_json = json.load(convertedGrammar_file)

    #-----CYK Parser-----
    cyk_parser = CYKParser(converterGrammar_json)
    sentence = "he cooks with a knife"
    result = cyk_parser.parse(sentence)
    
    print(f"Accepted: {result}")
    if result:
        print(f"The sentence '{sentence}' is in the language.")
    else:
        print(f"The sentence '{sentence}' is not in the language.")

    #-----Time-----
    end = time.time()
    processTime = (end - start) * 1000
    print("Execution time: {:0.2f} milliseconds".format(processTime))
