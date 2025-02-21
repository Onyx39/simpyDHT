"""
Classe représentant la DHT
"""

import random as rd

import simpy
from classes.node import Node


class Dht:
    """
    Classe DHT

    Attributs :
        env (simpy.Environment) : environnement de simulation
        array_node (list[Node]) : la liste des noeuds
        id_compteur (int) : un compteur pour numéroter les noeuds
    """

    def __init__(self):
        self.env : simpy.Environment = simpy.Environment()
        self.array_node : list[Node] = []
        self.id_compteur : int = 0
        self.start()

    def start(self) -> None:
        """
        Initialise la DHT
        """

        n0 = Node(self.env, 0, 80)
        n1 = Node(self.env, 1, 6)
        n2 = Node(self.env, 2, 42)

        n0.right_neighbour = n1
        n0.left_neighbour = n2

        n1.right_neighbour = n2
        n1.left_neighbour = n0

        n2.right_neighbour = n0
        n2.left_neighbour = n1
        self.array_node.append(n0)
        self.array_node.append(n1)
        self.array_node.append(n2)
        self.id_compteur = 2

        for node in self.array_node:
            node.connected = True

        self.insert_nodes(20)

    def insert_nodes(self, nb_nodes) -> None:
        """
        Insère des noeuds aléatoirement dans la DHT
        """

        for _ in range (nb_nodes) :
            id_node = rd.randint(1, 100)
            self.id_compteur = self.id_compteur + 1
            entree = self.get_random_connected_node()
            new_node = Node(env=self.env,
                            id_simpy=self.id_compteur,
                            id_node=id_node,
                            entree_dht=entree)
            self.array_node.append(new_node)

    def get_random_connected_node(self) -> Node:
        """
        Renvoie un noeud au hasard déja inséré dans le DHT
        """
        index = None
        node = None
        while node is None:
            index = rd.randint(0, len(self.array_node) - 1)
            if self.array_node[index].connected :
                node = self.array_node[index]
        return node
