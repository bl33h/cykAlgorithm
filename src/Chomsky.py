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
                if len(production) == 1 and production in self.grammar['VARIABLES']:
                    if production in unit_productions:
                        new_productions.extend(unit_productions[production])
            new_productions = list(set(new_productions))
            self.grammar['REGLAS'][variable] = [p for p in productions if p not in unit_productions]

    def convert_to_cnf(self):
        new_grammar = {
            "INICIAL": self.grammar["INICIAL"],
            "VARIABLES": self.grammar["VARIABLES"],
            "TERMINALES": self.grammar["TERMINALES"],
            "REGLAS": []
        }
        
        for variable, productions in self.grammar['REGLAS'].items():
            for production in productions:
                if len(production) == 1:
                    # Regla unitaria, ignorada en CNF
                    continue
                elif all(s in self.grammar['TERMINALES'] for s in production):
                    # Producción de terminales, crear nueva variable
                    new_variable = f"X_{production}"
                    new_grammar["REGLAS"].append((variable, [new_variable]))
                    new_grammar["REGLAS"].append((new_variable, list(production)))
                elif all(s in self.grammar['VARIABLES'] for s in production):
                    # Producción de variables, no es necesario cambiar
                    new_grammar["REGLAS"].append((variable, list(production)))
                else:
                    # Combinación de variables y terminales, crear nueva variable
                    new_variable = f"X_{production}"
                    new_grammar["REGLAS"].append((variable, [new_variable]))
                    new_grammar["REGLAS"].append((new_variable, list(production)))
        
        self.grammar = new_grammar
    