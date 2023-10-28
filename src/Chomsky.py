import json

class CNFConverter:
    def __init__(self, grammar: dict, epsilon_symbol: str="ep") -> None:
        self.grammar = grammar
        self.epsilon = epsilon_symbol
        
    def is_variable(self, variable) -> bool:
        return variable in self.grammar["VARIABLES"]
    
    def is_terminal(self, symbol) -> bool:
        return symbol in self.grammar["TERMINALES"]
    
    def is_terminal_variable(self, variable) -> bool:
        productions = self.grammar["REGLAS"][variable]
        return all(self.is_terminal(production) for production in productions)
    
    def is_valid_production(self, from_var: str, to_prod: str) -> bool:
        var_check = self.is_variable(from_var)
        prod_check = all([self.is_variable(x) or self.is_terminal(x) or x == self.epsilon for x in to_prod.split(" ")])
        return var_check and prod_check
    
    def has_productions(self, variable) -> bool:
        return variable in self.grammar["REGLAS"]
    
    def is_nullable(self, variable: str) -> bool:
        # If there's no productions or 'variable' is initial symbol, 'variable' is not nullable
        if not self.has_productions(variable) or variable == self.grammar["INICIAL"]: return False
        productions = self.grammar["REGLAS"][variable]
        # If production 'variable -> epsilon' exists, 'variable' is nullable
        if any([production == self.epsilon for production in productions]): return True
        # If production 'variable -> X1 X2 ... Xn' exists, and every Xi is nullable, 'variable' is nullable
        for production in productions:
            if all(self.is_variable(symbol) for symbol in production.split(" ")):
                # This checks if there's a terminal variable (variable that takes directly to a terminal) in the production
                # Also 'skips' the origin variable if it's present inside the production (recursive production)
                # to avoid an infinite recursion loop
                if any(self.is_terminal_variable(var) or var != variable for var in production.split(" ")): return False
                nullable_symbols = []
                for variable in production.split(" "):
                    nullable_symbols.append(self.is_nullable(variable))
                return all(nullable_symbols)
            else:
                continue
        return False
    
    def is_unit(self, production: str) -> bool:
        return len(production.split(" ")) == 1 and self.is_variable(production)
    
    def can_terminate(self, from_var: str, to_prod: str):
        return all(symbol != from_var for symbol in to_prod.split(" "))
    
    def get_immediately_reachable_variables(self, origin_var: str) -> set:
        reachables = set()
        for production in self.grammar["REGLAS"][origin_var]:
            symbols = production.split(" ")
            for symbol in symbols:
                if self.is_variable(symbol): reachables.add(symbol)
        return reachables
    
    def reachable_variables(self) -> set:
        # Store all the immediately reachable variables from start (S0) in the 'reachables'set
        reachables = self.get_immediately_reachable_variables(self.grammar["INICIAL"])
        # Keep adding the immediately reachable for every element in 'reachables' until there's no difference
        new_reachables = set()
        while True:
            new_reachables.update(reachables)
            for variable in reachables:
                reachable_from_var = self.get_immediately_reachable_variables(variable)
                new_reachables.update(reachable_from_var)
            if new_reachables != reachables:
                reachables.update(new_reachables)
            else:
                break
        return reachables            
    
    def is_reachable(self, variable: str) -> bool:
        return variable in self.reachable_variables()
    
    def add_variable(self, variable):
        if not self.is_variable(variable):
            self.grammar["VARIABLES"].append(variable)
            
    def remove_variable(self, variable):
        if not self.is_variable(variable):
            return
        # Remove it's productions if there's any
        if self.has_productions(variable):
            del self.grammar["REGLAS"][variable]
        # Remove productions that contain 'var'
        productions_to_remove = []
        for origin, productions in self.grammar["REGLAS"].items():
            for production in productions:
                if variable in production.split(" "):
                    productions_to_remove.append( (origin, production) )
        for origin, prod in productions_to_remove:
            self.grammar["REGLAS"][origin].remove(prod)
        # Remove the variable from the variable list
        self.grammar["VARIABLES"].remove(variable)
            
    def add_production(self, from_var: str, to_prod: str):
        # Raise an exception if from_var is not a registered variable
        if not self.is_variable(from_var):
            raise Exception(f"'{from_var}' is not registered as a variable.")
        # Only add production if it's not already in the grammar
        if not self.has_productions(from_var):      # If from_var has no productions, add the new one to the grammar
            self.grammar["REGLAS"][from_var] = [to_prod]
        else:                                       # If from_var has existing productions, add it if it's not already there
            existing_productions = self.grammar["REGLAS"][from_var]
            if to_prod not in existing_productions and self.is_valid_production(from_var, to_prod):
                self.grammar["REGLAS"][from_var].append(to_prod)
    
    def get_new_origin_symbol(self):
        # Create a new symbol 'B0'
        i = 0
        new_symbol = f"B{i}"
        # If the new symbol is already a variable, generate a new one
        while self.is_variable(new_symbol):
            i += 1
            new_symbol = f"B{i}"
        return new_symbol
    
    # START
    def replace_initial_symbol(self):
        # Define new initial variable
        new_initial_var = "S0"
        # Add the variable an create the new production to original initial variable
        self.add_variable(new_initial_var)
        self.add_production(new_initial_var, self.grammar["INICIAL"])
        # Set the new initial variable
        self.grammar["INICIAL"] = new_initial_var
    
    # TERM
    def create_variables_for_terminals(self):
        for t in self.grammar["TERMINALES"]:
            new_variable = f"X{t}"
            self.add_variable(new_variable)
            # Check every production for the terminal 't'
            for origin, productions in self.grammar["REGLAS"].items():
                for index, production in enumerate(productions):
                    prod_symbols = production.split(" ")
                    for i in range(len(prod_symbols)):
                        # If the terminal 't' appears, replace it with the newly created variable
                        if prod_symbols[i] == t: prod_symbols[i] = new_variable
                    new_production = " ".join(prod_symbols)
                    # Replace the existing production with newly created one
                    self.grammar["REGLAS"][origin][index] = new_production
            # Add production for the newly created variable (new_variable -> t)
            self.add_production(new_variable, t)
    
    # BIN
    def binarize_productions(self):
        additional_productions = {} # Dict to store the productions to be added to the grammar (same structure a grammar productions)
        for origin, productions in self.grammar["REGLAS"].items():
            for index, production in enumerate(productions):
                prod_symbols = production.split(" ")
                while len(prod_symbols) > 2:
                    # Pop the last 2 symbols from the production
                    symbol_2 = prod_symbols.pop()
                    symbol_1 = prod_symbols.pop()
                    # Create and add the new origin variable to the grammar
                    new_origin = self.get_new_origin_symbol()
                    self.add_variable(new_origin)
                    # Add the new variable to the production
                    prod_symbols.append(new_origin)
                    # Store the new production (for the new origin variable) in the 'additional_productions' dict
                    symbol_list = [str(symbol_1), str(symbol_2)]
                    new_origin_production = " ".join(symbol_list)
                    additional_productions[new_origin] = [new_origin_production]
                    # Replace existing production with an updated one (with the last 2 symbols replaced by 1)
                    updated_production = " ".join(prod_symbols)
                    self.grammar["REGLAS"][origin][index] = updated_production
        # Add the additional productions to the grammar
        for origin, productions in additional_productions.items():
            for index, production in enumerate(productions):
                self.add_production(origin, production)
    
    # DEL
    def delete_epsilon_productions(self):
        # Scan the variables for nullable ones
        for variable in self.grammar["VARIABLES"]:
            if self.is_nullable(variable):
                # Add new productions omitting the nullable variable
                for origin, productions in self.grammar["REGLAS"].items():
                    for production in productions:
                        for index, symbol in enumerate(production.split(" ")):
                            if symbol == variable:
                                # Create new production
                                new_production_symbols = production.split(" ")
                                new_production_symbols.pop(index) 
                                new_production = " ".join(new_production_symbols)
                                # Add the new production
                                self.add_production(origin, new_production)
        # Remove all direct epsilon productions (X -> epsilon)
        variables_to_remove = []
        for origin, productions in self.grammar["REGLAS"].items():
            for production in productions:
                if production == self.epsilon:
                    self.grammar["REGLAS"][origin].remove(production)
                # If the origin variable is left with no productions, mark it for removal from the productions dict
                if len(self.grammar["REGLAS"][origin]) == 0:
                    variables_to_remove.append(origin)
        # Removed all the stored variables from the productions dict
        for variable in variables_to_remove:
            self.remove_variable(variable)
            
    # UNIT
    def delete_unit_productions(self):
        # Keep scannig productions for units until there is none
        found_units = True
        while found_units:
            found_units = False
            productions_to_add = []
            productions_to_remove = []
            for origin, productions in self.grammar["REGLAS"].items():
                print(f"Checking '{origin}' productions: {productions}")
                for production in productions:
                    if self.is_unit(production):
                        print("Found UNIT:", production)
                        found_units = True
                        # Store the productions to add to the origin variable and the unit production to remove later
                        print("\tSet to add productions:", self.grammar["REGLAS"][production])
                        productions_to_add.append( (origin, self.grammar["REGLAS"][production]) )
                        print("\tSet to remove production:", production)
                        productions_to_remove.append( (origin, production) )
            # Add the stored productions
            print("Productions to add:", productions_to_add)
            for origin, productions in productions_to_add:
                for production in productions:
                    self.add_production(origin, production)
            # Remove the stored unit productions
            print("Productions to remove:", productions_to_remove)
            for origin, production in productions_to_remove:
                self.grammar["REGLAS"][origin].remove(production)

    # USELESS
    def delete_useless_productions(self):
        reachable = self.reachable_variables()
        variables_to_remove = []
        for variable in self.grammar["VARIABLES"]:
            # Ignore initial symbol
            if variable == self.grammar["INICIAL"]: continue
            # Remove if variable has no productions
            if not self.has_productions(variable):
                variables_to_remove.append(variable)
            # Remove if there's no productions that can terminate
            elif not any(self.can_terminate(variable, prod) for prod in self.grammar["REGLAS"][variable]):
                variables_to_remove.append(variable)
            # Remove if it's unreachable from the start variable
            elif variable not in reachable:
                variables_to_remove.append(variable)
        # Remove stored variables
        for var in variables_to_remove:
            self.remove_variable(var)
    
    # Final method to convert a CFG to CNF
    def convert(self) -> dict:
        self.replace_initial_symbol()           # START
        self.create_variables_for_terminals()   # TERM
        self.binarize_productions()             # BIN
        self.delete_epsilon_productions()       # DEL
        print("Pre UNIT grammar:")
        print(json.dumps(self.grammar, indent=4))
        self.delete_unit_productions()          # UNIT
        self.delete_useless_productions()       # USELESS
        # Return the converted grammar
        return self.grammar
        
# Load the json file
with open('test_grammar_2.json', 'r') as file:
    grammar = json.load(file)

# Create an instance of the CNFCoverter with the read gammar
converter = CNFConverter(grammar)

# Convert the grammar
cnf_grammar = converter.convert()

# prints the CNF grammar
print(json.dumps(cnf_grammar, indent=4))
        