import networkx as nx
from math import log

def returnsConceptIterator(f):
    def wrap(self, *args, **kwargs):
        ret = f(self, *args, **kwargs)
        for c in ret:
            yield Concept(self.network, c)
    return wrap

def returnsArcIterator(f):
    def wrap(self, *args, **kwargs):
        ret = f(self, *args, **kwargs)
        for (i, j, key, data) in ret:
            yield Arc(self.network, i, j, key, data)
    return wrap


class Network:
    def __init__(self):
        self.network = nx.MultiDiGraph()

    def get(self, id):
        return Concept(self.network, id)


class Concept:
    def __init__(self, network, id):
        self.network = network
        self.id = id

    def __getattr__(self, attr):
        return self.network.node[self.id][attr]

    def __setattr__(self, attr, value):
        self.network.node[self.id][attr] = value

    @returnsConceptIterator
    def successors(self):
        return self.network.successors_iter(self.id)

    @returnsConceptIterator
    def predecessors(self):
        return self.network.predecessors_iter(self.id)

    @returnsArcIterator
    def outArcs(self):
        return self.network.out_edges_iter(self.id, data=True, keys=True)

    @returnsArcIterator
    def inArcs(self):
        return self.network.in_edges_iter(self.id, data=True, keys=True)


    def compute_activation(self):
        """
        computes the new node activation, using :
        -divlog : logarithmic divisor (connexity)
        -activation of neighbours
        -self-desactivation
        """
        divlog = log(3 + len(self.inArcs())) / log(3)
        divlog = 1  # deactivated for now
        i = 0
        for arc in self.inArcs():
            i = i + (arc.weight or 0) * arc.origin.activation
            # does not take
        act = self.activation
        i = i / (100 * divlog)  # neighbours
        d = act / (100 * (self.ic or 1))  # self desactivation
        self.activation = min(act + i - d, 100)  # we do not go beyond 100




class Arc:
    def __init__(self, network, fromId, toId, key=0, data=None):
        self.network = network
        self.fromId = fromId
        self.toId = toId
        self.key = key

    def __getattr__(self, attr):
        return self.network[self.fromId][self.toId][self.key][attr]

    def __setattr__(self, attr, value):
        self.network[self.fromId][self.toId][self.key][attr] = value

    def origin(self):
        return Concept(self.network, self.fromId)

    def destination(self):
        return Concept(self.network, self.toId)