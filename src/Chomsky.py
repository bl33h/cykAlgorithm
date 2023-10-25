#Copyright (C), 2023-2024, bl33h
#FileName: chomsky
#Author: Sara Echeverria, Melissa Perez, Alejandro Ortega
#Version: I
#Creation: 18/10/2023
#Last modification: 25/10/2023

import json

class Chomsky:
    def __init__(self, grammar):
        self.grammar = grammar

    def remove_epsilon_rules(self):
        epsilon_productions = set()

        for variable, productions in self.grammar['REGLAS'].items():
            if 'ε' in productions:
                epsilon_productions.add(variable)
        
        while epsilon_productions:
            for variable, productions in self.grammar['REGLAS'].items():
                new_productions = []
                for production in productions:
                    if not any(ep in production for ep in epsilon_productions):
                        new_productions.append(production)
                self.grammar['REGLAS'][variable] = new_productions

            epsilon_productions = set()
            for variable, productions in self.grammar['REGLAS'].items():
                if 'ε' in productions:
                    epsilon_productions.add(variable)

    def remove_unit_rules(self):
        unit_productions = {}
        
        for variable, productions in self.grammar['REGLAS'].items():
            new_productions = []
            for production in productions:
                if len(production) == 1 and production[0] in self.grammar['VARIABLES']:
                    if production[0] in unit_productions:
                        new_productions.extend(unit_productions[production[0]])
            new_productions = list(set(new_productions))
            self.grammar['REGLAS'][variable] = [p for p in productions if p not in unit_productions]

    def convert_to_cnf(self):
        new_grammar = {
            "INICIAL": self.grammar["INICIAL"],
            "VARIABLES": self.grammar["VARIABLES"],
            "TERMINALES": self.grammar["TERMINALES"],
            "REGLAS": {}
        }
        
        for variable, productions in self.grammar['REGLAS'].items():
            for production in productions:
                if len(production) == 1:
                    # unit rule
                    continue
                elif all(s in self.grammar['TERMINALES'] for s in production):
                    # terminal production (new variable)
                    new_variable = f"X_{production[0]}"
                    if new_variable not in new_grammar['REGLAS']:
                        new_grammar['REGLAS'][new_variable] = [production]
                    else:
                        new_grammar['REGLAS'][new_variable].append(production)
                    new_grammar['REGLAS'][variable] = [[new_variable] if production == [s] else production for s in production]
                elif all(s in self.grammar['VARIABLES'] for s in production):
                    # variables production
                    if variable not in new_grammar['REGLAS']:
                        new_grammar['REGLAS'][variable] = []
                    new_grammar['REGLAS'][variable].append(production)
                else:
                    # combining variables and terminals (new variable)
                    new_variable = f"X_{production[0]}"
                    if new_variable not in new_grammar['REGLAS']:
                        new_grammar['REGLAS'][new_variable] = [production]
                    else:
                        new_grammar['REGLAS'][new_variable].append(production)
                    new_grammar['REGLAS'][variable] = [[new_variable] if production == [s] else production for s in production]
        
        self.grammar = new_grammar

# loads the json file
with open('input.json', 'r') as archivo:
    datos = json.load(archivo)

# creates an instance of Chomsky in the grammar
chomsky_converter = Chomsky(datos)

# applies the necessary transformations
chomsky_converter.remove_epsilon_rules()
chomsky_converter.remove_unit_rules()
chomsky_converter.convert_to_cnf()

# prints the CNF
print(json.dumps(chomsky_converter.grammar, indent=4))