def cyk_parse(grammar, sentence):
    variables = grammar["VARIABLES"]
    n = len(sentence)

    # Initialize the CYK table with empty sets
    table = [[set() for _ in range(n)] for _ in range(n)]

    # Fill in the diagonal with the terminals that match the words in the sentence
    for i in range(n):
        for variable in variables:
            if sentence[i] in grammar["REGLAS"].get(variable, []):
                table[i][i].add(variable)

    # Fill in the rest of the table
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for variable in variables:
                    for rule in grammar["REGLAS"].get(variable, []):
                        if len(rule.split()) == 2:
                            left, right = rule.split()
                            if left in table[i][k] and right in table[k + 1][j]:
                                table[i][j].add(variable)

    # If the start symbol is in the top-right cell, the string is in the language
    return grammar["INICIAL"] in table[0][n - 1]

# Example usage
if __name__ == "__main__":
    grammar = {
        "INICIAL": "S",
        "VARIABLES": ["S", "VP", "PP", "NP", "V", "P", "N", "Det"],
        "TERMINALES": ["cooks", "drinks", "eats", "cuts", "he", "she", "in", "with", "cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon", "a", "the"],
        "REGLAS": {
            "S": ["NP VP"],
            "VP": ["VP PP", "V NP", "cooks", "drinks", "eats", "cuts"],
            "PP": ["P NP"],
            "NP": ["Det N", "he", "she"],
            "V": ["cooks", "drinks", "eats", "cuts"],
            "P": ["in", "with"],
            "N": ["cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon"],
            "Det": ["a", "the"]
        }
    }

    sentence = "he cooks with a knife"
    result = cyk_parse(grammar, sentence.split())
    
    print(f"Accepted: {result}")
    if result:
        print(f"The sentence '{sentence}' is in the language.")
    else:
        print(f"The sentence '{sentence}' is not in the language.")
