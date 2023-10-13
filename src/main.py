import os

from classes.dht import Dht


dht = Dht()
env = dht.env

os.remove("logging.log")
open("logging.log", 'a').close()

print("\nDébut de simulation\n")
env.run(until=1000)
print("\nFin de simulation\n")

for i in dht.array_node:
    print(i)
