# cykAlgorithm
This CYK (Cocke-Younger-Kasami) parser is a Python program that demonstrates parsing a sentence using a Context-Free Grammar (CFG) represented in Chomsky Normal Form (CNF). It utilizes the provided Python files and a JSON configuration file to perform the parsing. The CNF conversion is done by the `CNFConverter` class in `chomsky.py`, and the CYK parsing is performed in `cyk.py`.

## Files

- `main.py`: The main Python script that loads the CFG from the `input.json` file, converts it to CNF, and then performs CYK parsing on a sample sentence.
- `chomsky.py`: The Python module responsible for the CNF conversion of the provided CFG.
- `cyk.py`: The Python module that implements the CYK parsing algorithm.
- `input.json`: The JSON configuration file containing the CFG in CNF format.

## How to Use
To run the CYK parser for the given CFG, follow these steps:
1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/bl33h/CYK-Parser
   cd src
   python main.py

