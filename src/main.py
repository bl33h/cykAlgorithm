import json
from Chomsky import *

# Cargar el archivo JSON
with open('src/input.json', 'r') as archivo:
    datos = json.load(archivo)

# Acceder a las diferentes secciones de tu JSON
inicial = datos['INICIAL']
variables = datos['VARIABLES']
terminales = datos['TERMINALES']
reglas = datos['REGLAS']
