import math
import pprint as pp

class Node:

    def __init__(self, similarity=0, nextval=None, subject= "", length=50):
        self._similarity = similarity
        self.subject = subject
        self._nextval = nextval
        self.max_length = length
        self.node = {"subject": subject,
                     "similarity": similarity,
                     "nextval": nextval}

    def change_next(self, n):

        self._nextval = n
        if n is not None:
            self.node["nextval"] = n.subject
        else:
            self.node["nextval"] = None

    def get_sim(self):

        return self._similarity

    def get_next(self):

        return self._nextval

    def set_sim(self, n):

        self._similarity = n


class LinkedList:

    def __init__(self):
        self._head = None
        self._tail = None
        self.length = 0
        self.linkedlist = {"length": 0}

    def add_node_tail(self, n):

        self._tail.change_next(n)
        n.change_next(None)
        self.linkedlist[n.subject] = n.node
        self._tail = n
        self.length += 1
        self.linkedlist["length"] = self.length

    def add_node_head(self, n):

        n.change_next(self._head)
        self.linkedlist[n.subject] = n.node
        self._head = n
        self.length += 1
        self.linkedlist["length"] = self.length

    def add_node_middle(self, n):

        current = self._head.get_next()
        previous = self._head

        while current is not None and current.get_next() is not None:

            if (n.get_sim() <= current.get_sim()) and (n.get_sim() >= previous.get_sim()):
                print("adding node")
                n.change_next(current)
                previous.change_next(n)
                self.linkedlist[n.subject] = n.node
                self.length += 1
                self.linkedlist["length"] = self.length
                break

            else:

                previous = current
                current = current.get_next()

    def update_node(self, n):

        node = self.search(n.subject)

        if node is not None:

            node.set_sim(n.get_sim()**2)

    def search(self, n):

        current = self._head

        while current is not None:

            if current.subject == n:

                return current

            else:

                current = current.get_next()

        return None


    def check_sim(self, n):
         
        if self.length == 0:
            self.add_node_head(n)
            self._tail = n
            return

        exists = self.search(n.subject)

        if exists is not None:

            if exists.get_sim() < n.get_sim():

                exists.set_sim(n.get_sim()**2)

            else:

                exists.set_sim(exists.get_sim()**2)

            return

        if n.get_sim() <= self._head.get_sim():

            self.add_node_head(n)

        elif n.get_sim() >= self._tail.get_sim() and self.length < 50:

            self.add_node_tail(n)

        elif (n.get_sim() > self._head.get_sim()) and (n.get_sim() < self._tail.get_sim() and self.length < 50) or (self.length < 50):
            self.add_node_middle(n)

    def get_head(self):

        return self._head

    def get_tail(self):

        return self._tail

    def to_str(self):
  
        pp.pprint(self.linkedlist)
