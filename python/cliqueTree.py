from cvxopt import spmatrix, amd
import chompack as cp
import spanningTree
from collections import defaultdict as dd
from factorTable import FactorTable

#
# Converts a graph into a clique tree, and returns the clique tree object
#
# @param I,J   (I[i],J[i]) is an edge in E. We require I > J
#
def graph_to_clique_tree(I, J):
  n = max(max(I),max(J))+1
  A = spmatrix(1, I+range(n), J+range(n))
  print A

  # Compute symbolic factorization using AMD ordering
  # This automatically does a chordal completion on the graph
  symb = cp.symbolic(A, p=amd.order)

  # The factorization permutes the node indices, we need to unpermute these
  cliques = symb.cliques()
  perm = symb.p
  cliques = [[perm[i] for i in clique] for clique in cliques]

  return CliqueTree(cliques, A)

#
# A Clique object represents a clique in the clique tree
#
# @param nodes    A list of nodes representing the scope of the clique
# @param matrix   A pointer to the original adjacency matrix of the graph,
#                 used to determine factor table potentials
#
class Clique:
  # Instantiation generates the factor table
  def __init__(self, index, nodes, matrix):
    self.index = index
    self.neighbours = set() # edges in clique intersection graph
    self.active_neighbours = set() # edges in clique tree
    self.nodes = sorted(nodes)
    self.potential = FactorTable(nodes, matrix)

  def add_neighbours(self, cliques):
    self.neighbours.update(cliques)

  # Returns a list of variables representing the sepset of self and other
  def determine_sepset(self, other):
    return list(set(self.nodes) & set(other.nodes))

  # Use this to get neighbours for BP algorithm
  def get_neighbours(self):
    return self.active_neighbours

  # The clique in human readable format
  def __str__(self):
    return "(" + str(self.nodes) + ")"

#
# A CliqueTree object represents a collection of cliques, each clique is
# connected to neighbouring cliques via an undirected edge. 
#
# @param cliques    A clique intersection graph represented as a list of lists, each list
#                   representing the scope of a clique
# @param matrix     A pointer to the original adjacency matrix of the graph,
#                   used to instantiate clique factor tables
#
class CliqueTree:
  # Instantiation creates a clique list and connects each clique to all its
  # neighbours in the tree
  def __init__(self, cliques, matrix):
    self.cliques = []
    self.edges = {} # Dictionary of {edge: weight}
    self.node_to_clique = dd(list)

    # Instantiate cliques and fill node_to_clique entries
    for index, nodes in enumerate(cliques):
      clique = Clique(index, nodes, matrix)
      for node in nodes:
        self.node_to_clique[node].append(clique)
      self.cliques.append(clique)

    # Update list of neighbours after node_to_clique entries are filled
    for clique in self.cliques:
      for node in clique.nodes:
        neighbours = list(self.node_to_clique[node])
        neighbours.remove(clique)

        # Add neighbours to clique
        clique.add_neighbours(neighbours)

        # Add edge to edgeset
        for neighbour in neighbours:
          edge = tuple(sorted([neighbour.index, clique.index]))
          self.edges[edge] = len(clique.determine_sepset(neighbour))

    # Perform Kruskal to turn clique intersection graph into clique tree
    spanningTree.kruskal(self)
          
  # The clique tree in human readable format
  def __str__(self):
    s = "\n  ".join([str(c) + " -> " + \
             ", ".join([str(x) for x in c.get_neighbours()]) \
              for c in self.cliques])
    return "Clique Tree:\n  " + s

