import json
from typing import Dict

class CYKParser:
    def __init__(self, cnf_grammar: Dict[str, any]):
        self.grammar = cnf_grammar

    def parse(self, sentence: str) -> bool:
        variables = self.grammar["VARIABLES"]
        n = len(sentence.split())

        # Initialize the CYK table with empty sets
        table = [[set() for _ in range(n)] for _ in range(n)]

        # Fill in the diagonal with the terminals that match the words in the sentence
        for i, word in enumerate(sentence.split()):
            for variable in variables:
                if word in self.grammar["REGLAS"].get(variable, []):
                    table[i][i].add(variable)

        # Fill in the rest of the table
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for k in range(i, j):
                    for variable in variables:
                        for rule in self.grammar["REGLAS"].get(variable, []):
                            if len(rule.split()) == 2:
                                left, right = rule.split()
                                if left in table[i][k] and right in table[k + 1][j]:
                                    table[i][j].add(variable)

        # If the start symbol is in the top-right cell, the sentence is in the language
        return self.grammar["INICIAL"] in table[0][n - 1]

# Example usage
if __name__ == "__main__":
    # Specify the correct file path
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
