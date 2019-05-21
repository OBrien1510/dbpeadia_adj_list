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
        self.node["nextval"] = n.subject

    def get_sim(self):

        return self._similarity

    def get_next(self):

        return self._nextval


class LinkedList:

    # similiarity = distance so smaller the better

    def __init__(self):
        self._head = None
        self._tail = None
        self.length = 0
        self.linkedlist = {}

    def add_node_tail(self, n):

        self._tail.change_next(n)
        n.change_next(None)
        self.linkedlist[n.subject] = n
        self.length += 1

    def add_node_head(self, n):

        n.change_next(self.head)
        self._head = n
        self.length += 1

    def add_node_middle(self, n):

        current = self.head.get_next()
        previous = self.head

        while current.get_next() is not None:

            if (n.similarity <= current.similarity) and (n.similarity >= previous.similarity):

                # if similarity is between previous and current node
                n.change_next(current)
                previous.change_next(n)
                self.length += 1
                break

            else:

                # else continue through linked list
                previous = current
                current = current.nextval


    def check_sim(self, n):

        if n.similarity <= self._head.get_sim():

            self.add_node_head(n)

        elif n.similarity >= self._tail.get_sim() and self.length <= 20:

            self.add_node_tail(n)

        elif (n.get_sim() > self._head.get_sim()) and (n.get_sim() < self._tail.get_sim()) or (self.length <= 20):

            self.add_node_middle(n)

    def get_head(self):

        return self._head

    def get_tail(self):

        return self._tail