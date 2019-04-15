import heapq

class FilePriorite:
    def __init__(self):
        self.L = []
        self.compte = 0

    def inserer(self, element, priorite):
        e = (priorite, self.compte, element)
        self.compte -= 1
        heapq.heappush(self.L, e)

    def popMinimum(self):
        return heapq.heappop(self.L)[2]

    def estVide(self):
        return len(self.L) == 0

    def items(self):
        for e in self.L:
            yield e[2]
