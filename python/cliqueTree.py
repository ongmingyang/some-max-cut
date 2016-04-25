import sys
from cvxopt import spmatrix, amd
import chompack as cp
import spanningTree
import stats 
from collections import defaultdict as dd
from factorTable import FactorTable

LARGEST_CLIQUE_SIZE = 10

#
# Converts a graph into a clique tree, and returns the clique tree object
#
# @param I,J   (I[i],J[i]) is an edge in E. We require I > J
#
def graph_to_clique_tree(I, J):
  n = max(max(I),max(J))+1
  stats.number_of_nodes = n
  A = spmatrix(1, I+range(n), J+range(n))

  # Compute symbolic factorization using AMD ordering
  # This automatically does a chordal completion on the graph
  symb = cp.symbolic(A, p=amd.order)

  # The factorization permutes the node indices, we need to unpermute these
  cliques = symb.cliques()
  perm = symb.p
  cliques = [[perm[i] for i in clique] for clique in cliques]

  # If the largest clique is above threshold, we terminate the algorithm
  cs = max(len(x) for x in cliques)
  if cs > LARGEST_CLIQUE_SIZE:
    sys.exit('''
    Chordal completion has clique of size %d,
    Max allowed size is %d,
    Program terminating...
    ''' % (cs, LARGEST_CLIQUE_SIZE))

  stats.maximum_clique = cs
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
    self.neighbours = set() # edges in clique tree
    self.nodes = sorted(nodes)
    self.potential = FactorTable(nodes, matrix)

  # Returns a list of variables representing the sepset of self and other
  def determine_sepset_size(self, other):
    return len(set(self.nodes) & set(other.nodes))

  # Creates an edge between self and other cliques
  def connect(self, other):
    self.neighbours.add(other)
    other.neighbours.add(self)

  # Use this to get neighbours in the clique tree 
  def get_neighbours(self):
    return self.neighbours

  # The clique in human readable format
  def __str__(self):
    return "(%s)" % str(self.nodes)

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
    edges = {} # Dictionary of {edge: weight}
    node_to_clique = dd(list)

    # Instantiate cliques and fill node_to_clique entries
    for index, nodes in enumerate(cliques):
      clique = Clique(index, nodes, matrix)
      for node in nodes:
        node_to_clique[node].append(clique)
      self.cliques.append(clique)

    # Update list of neighbours after node_to_clique entries are filled
    for clique in self.cliques:
      for node in clique.nodes:
        neighbours = list(node_to_clique[node])
        neighbours.remove(clique)

        # Add edge to edgeset
        for neighbour in neighbours:
          edge = tuple(sorted([neighbour.index, clique.index]))
          edges[edge] = clique.determine_sepset_size(neighbour)

    # Perform Kruskal to turn clique intersection graph into clique tree
    spanningTree.kruskal(self.cliques, edges)
          
  # The clique tree in human readable format
  def __str__(self):
    s = "\n  ".join([str(c) + " -> " + \
             ", ".join([str(x) for x in c.get_neighbours()]) \
              for c in self.cliques])
    return "Clique Tree:\n  " + s

