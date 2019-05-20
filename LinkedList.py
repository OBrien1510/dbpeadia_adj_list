import math
import pprint as pp

class Node:

    def __init__(self, similarity=0, nextval=None, subject= ""):
        self._similarity = similarity
        self.subject = subject
        self._nextval = nextval
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

    """
    Class to implement a linked list for semantic similarity
    linked list is aranged in descending order of similarity
    head represents highest sim and tail represents lowest sim
    note: the higher the sim, the lower the distance value and vice versa
    (so head actually has the lowest numerical value)
    """

    def __init__(self, length=50):
        self._head = None
        self._tail = None
        self._max_length = length
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
        if self.length > self._max_length:
            self.remove_tail()
            self.length -= 1

        if self.length > self._max_length:
            self.remove_tail()
            self.length -= 1

        self.linkedlist["length"] = self.length

    def add_node_middle(self, n, update):

        current = self._head.get_next()
        previous = self._head

        while current is not None and current.get_next() is not None:

            # if the the sim is less than the current node but greater than the previous node
            # then we want to insert between the two
            if (n.get_sim() <= current.get_sim()) and (n.get_sim() >= previous.get_sim()):
                n.change_next(current)
                previous.change_next(n)
                self.linkedlist[n.subject] = n.node
                self.length += 1
                self.linkedlist["length"] = self.length
                # if we are updating a node's similarity we want to continue on until we find the old node to delete
                if update:
                    previous = current
                    current = current.get_next()
                else:
                    break
            # if we are continuing after an update and we find the old node, delete it
            elif update and current.get_next().subject == n.subject:
                # remove old node
                self.remove_middle(current, current.get_next)

            else:

                previous = current
                current = current.get_next()

    def remove_middle(self, previous, current):

        nextval = current.get_next()
        previous.change_next(nextval)
        del nextval

    def remove_tail(self):
        # sometimes adding a new node takes it over the max length
        # in this case simply remove the tail to return to max length

        current = self._head

        while current is not None and current.get_next() is not None:
            # if next value is the tail, delete the tail and make the current the next tail
            if current.get_next() == self._tail:

                self._tail = current
                current.change_next(None)
                self.linkedlist[current.subject] = current.node

                # remove all references to previous tail node
                del self.linkedlist[current.get_next().subject]
                next_val = current.get_next()
                del next_val
                return

            current = current.get_next()

    def update_node(self, n):

        node = self.search(n.subject)

        if node is not None:

            # reduce not distance metric by raising it to the power of 2
            new_distance = node.get_sim()**2

            # create new node with new similiarity
            new_node = Node(new_distance, node.get_next(), node.subject)

            # insert the new node while deleting the old one
            self.add_node_middle(new_node, True)

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

        self.update_node(n)

        if n.get_sim() <= self._head.get_sim():

            self.add_node_head(n)

        # no case where we ever want to add to tail if list is already at max length
        elif n.get_sim() >= self._tail.get_sim() and self.length < 50:

            self.add_node_tail(n)

        elif (n.get_sim() > self._head.get_sim()) and (n.get_sim() < self._tail.get_sim() and self.length < 50) or (self.length < 50):
            self.add_node_middle(n, False)

    def get_head(self):

        return self._head

    def get_tail(self):

        return self._tail

    def get_max(self):

        return self._max_length

    def to_str(self):
  
        pp.pprint(self.linkedlist)
