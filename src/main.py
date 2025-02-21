"""
Fichier principal, exécutable
"""

# import os
# import logging as log

from classes.dht import Dht

# log.basicConfig(filename='logging.log',
#                 filemode='a',
#                 level = log.INFO,
#                 format='%(process)s - %(levelname)s - %(message)s')

# try:
#     os.remove("logging.log")
# except FileNotFoundError:
#     print("Le fichier 'logging.log' n'existe pas.")
# except Exception as e:
#     print(f"Une erreur est survenue lors de la suppression du fichier : {e}")

# open("logging.log", 'a').close()

dht = Dht()
env = dht.env

print("Début de simulation\n")
env.run(until=1000)
print("\nFin de simulation\n")

for i in dht.array_node:
    print(i)
