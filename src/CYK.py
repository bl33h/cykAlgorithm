#Copyright (C), 2023-2024, bl33h
#FileName: chomsky
#Author: Sara Echeverria, Melissa Perez, Alejandro Ortega
#Version: I
#Creation: 18/10/2023
#Last modification: 29/10/2023

from typing import Dict, List, Tuple

class TreeNode:
    def __init__(self, label: str, children: List['TreeNode'] = None):
        self.label = label
        self.children = children or []

class CYKParser:
    def __init__(self, cnf_grammar: Dict[str, any]):
        self.grammar = cnf_grammar
        self.table = None
        self.parse_tree = None

    def parse(self, sentence: str) -> bool:
        variables = self.grammar["VARIABLES"]
        n = len(sentence.split())

        # Initialize the CYK table with empty sets
        self.table = [[set() for _ in range(n)] for _ in range(n)]

        # Initialize the parse_tree with None values
        self.parse_tree = [[None for _ in range(n)] for _ in range(n)]

        # Fill in the diagonal with the terminals that match the words in the sentence
        for i, word in enumerate(sentence.split()):
            for variable in variables:
                if word in self.grammar["REGLAS"].get(variable, []):
                    self.table[i][i].add(variable)
                    self.parse_tree[i][i] = [TreeNode(variable, [TreeNode(word)])]

        # Fill in the rest of the table
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for k in range(i, j):
                    for variable in variables:
                        for rule in self.grammar["REGLAS"].get(variable, []):
                            if len(rule.split()) == 2:
                                left, right = rule.split()
                                if left in self.table[i][k] and right in self.table[k + 1][j]:
                                    self.table[i][j].add(variable)
                                    if self.parse_tree[i][k] and self.parse_tree[k + 1][j]:
                                        if self.parse_tree[i][j] is None:
                                            self.parse_tree[i][j] = []
                                        self.parse_tree[i][j].append(TreeNode(variable, [self.parse_tree[i][k], self.parse_tree[k + 1][j]]))

        # If the start symbol is in the top-right cell, the sentence is in the language
        return self.grammar["INICIAL"] in self.table[0][n - 1]

    def print_table(self):
        for row in self.table:
            print("\t".join(["\t".join(map(str, cell)) for cell in row]))

    def print_parse_tree(self, node=None, depth=0):
        if node is None:
            node = self.parse_tree[0][-1]

        if isinstance(node, list):
            for item in node:
                self.print_parse_tree(item, depth)
        else:
            variable = node.label
            print("  " * depth + variable)
            for child in node.children:
                self.print_parse_tree(child, depth + 1)
