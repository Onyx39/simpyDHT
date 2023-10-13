import simpy
import random as rd
from classes.node import Node


class Dht:

    def __init__(self):
        self.env = simpy.Environment()
        self.array_node = []
        self.id_compteur = 0
        self.start()

    def start(self):

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


        for _ in range (20) :
            id_node = rd.randint(1, 100)
            self.id_compteur = self.id_compteur + 1
            entree = self.get_random_connected_node()
            new_node = Node(env=self.env, id_simpy=self.id_compteur, id_node=id_node, entree_dht=entree)
            self.array_node.append(new_node)

        return self.array_node

    def get_random_connected_node(self):
        index = None
        node = None
        while node is None:
            index = rd.randint(0, len(self.array_node) - 1)
            if self.array_node[index].connected :
                node = self.array_node[index]
        return node
