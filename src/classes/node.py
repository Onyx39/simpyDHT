import random as rd
import logging as log

log.basicConfig(filename='logging.log',
                filemode='a',
                level = log.INFO,
                format='%(process)s - %(levelname)s - %(message)s')

class Node:

    def __init__(self, env, id_simpy: int, id_node: int, entree_dht=None):
        self.connected = False
        self.entree_dht = entree_dht
        self.id_simpy = id_simpy
        self.id_node = id_node
        self.env = env
        self.right_neighbour = None
        self.left_neighbour = None
        self.action = env.process(self.run())
        self.queue = []
        self.flag = False

    def run(self):
        yield from self.generator(rd.randint(3, 5))
        if self.connected:
            print("CONNECTION : ", self, ' [TEMPS : ', self.env.now, ']')
        while True:
            if self.connected:
                yield from self.generator(rd.randint(1, 5))
                if len(self.queue) != 0 and self.flag == False:
                    if self.queue[0][0] == "Insertion":
                        self.setup_flag_up()
                        self.insert(self, a_connecter=self.queue[0][1])
                    self.queue.pop(0)
                    self.setup_flag_down()
            else:
                yield from self.generator(rd.randint(20, 21))
                self.insert(self.entree_dht)

    def setup_flag_up(self):
        self.flag = True
        self.right_neighbour.flag = True
        self.left_neighbour.flag = True

    def setup_flag_down(self):
        self.flag = False
        self.right_neighbour.flag = False
        self.left_neighbour.flag = False

    def __str__(self):
        return f'Je suis le noeud simpy {self.id_simpy} , mon nom est {self.id_node} !      ' \
               f'({self.left_neighbour.id_node} <- {self.id_node} -> {self.right_neighbour.id_node})'

    def generator(self, duration):
        yield self.env.timeout(duration)

    def verify(self, target, entree_dht):
        if target.id_node > entree_dht.id_node and target.id_node < entree_dht.right_neighbour.id_node \
                or target.id_node > entree_dht.id_node and entree_dht.right_neighbour.id_node < entree_dht.id_node:

            target.right_neighbour = entree_dht.right_neighbour
            target.left_neighbour = entree_dht
            entree_dht.right_neighbour.left_neighbour = target
            entree_dht.right_neighbour = target
            target.connected = True
            print("CONNECTION : ", target, ' [TEMPS : ', self.env.now, ']')

        elif target.id_node < entree_dht.id_node and target.id_node > entree_dht.left_neighbour.id_node \
                or target.id_node < entree_dht.id_node and entree_dht.left_neighbour.id_node > entree_dht.id_node:

            target.left_neighbour = entree_dht.left_neighbour
            target.right_neighbour = entree_dht
            entree_dht.left_neighbour.right_neighbour = target
            entree_dht.left_neighbour = target
            target.connected = True
            print("CONNECTION : ", target, ' [TEMPS : ', self.env.now, ']')

        elif target.id_node == entree_dht.id_node or target.id_node == entree_dht.left_neighbour.id_node \
            or target.id_node == entree_dht.right_neighbour.id_node :
            ajout = rd.randint(1, 5)
            print(f"MODIFICATION : Noeud {target.id_node} ({target.id_simpy}) devient {target.id_node + ajout} [TEMPS : {self.env.now}]")
            target.id_node = target.id_node + ajout

        elif not target.connected:
            if target.id_node > entree_dht.right_neighbour.id_node:
                target.send_message("Insertion", entree_dht.right_neighbour)
                print('INFO SYSTEM : ' + str(self.id_node) + ' envoi ' + str(target.id_node) + ' à droite vers ' + str(
                    entree_dht.right_neighbour.id_node) + ' [TEMPS : ' + str(self.env.now) + ']')
            else:
                target.send_message("Insertion", entree_dht.left_neighbour)
                print('INFO SYSTEM : ' + str(self.id_node) + ' envoi ' + str(target.id_node) + ' à gauche vers ' + str(
                    entree_dht.left_neighbour.id_node) + ' [TEMPS : ' + str(self.env.now) + ']')
        

    def insert(self, entree_dht, a_connecter=None):
        if a_connecter is None:
            self.verify(self, entree_dht)
        else:
            self.verify(a_connecter, entree_dht)

    def receive(self, message):
        self.queue.append(message)

    def send_message(self, message, neighbour):
        neighbour.receive([message, self])
