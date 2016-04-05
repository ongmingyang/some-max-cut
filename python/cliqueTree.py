from cvxopt import spmatrix, amd
import chompack as cp
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
  def __init__(self, nodes, matrix):
    self.neighbours = set()
    self.nodes = sorted(nodes)
    self.potential = FactorTable(nodes, matrix)

  def add_neighbours(self, cliques):
    self.neighbours.update(cliques)

  # The clique in human readable format
  def __str__(self):
    return "(" + str(self.nodes) + ")"

#
# TODO: this represents a weighted clique intersection graph, NOT a clique
# tree!
#
# A CliqueTree object represents a collection of cliques, each clique is
# connected to neighbouring cliques via an undirected edge. Two cliques are
# neighbours if their scopes have non-empty intersections 
#
# The Tree property of CliqueTree is assumed to be implicit, that is, it is
# assumed that the cliques given to the instantiator already form a clique
# tree. The datatype does not enforce that there cannot be cliques that form
# cycles.
#
# @param cliques    A clique tree represented as a list of lists, each list
#                   representing the scope of a clique
# @param matrix     A pointer to the original adjacency matrix of the graph,
#                   used to instantiate clique factor tables
#
class CliqueTree:
  # Instantiation creates a clique list and connectes each clique to all its
  # neighbours in the tree
  def __init__(self, cliques, matrix):
    self.cliques = []
    self.node_to_clique = dd(list)

    # Instantiate cliques and fill node_to_clique entries
    for clique_list in cliques:
      clique = Clique(clique_list, matrix)
      for node in clique_list:
        self.node_to_clique[node].append(clique)
      self.cliques.append(clique)

    # Update list of neighbours after node_to_clique entries are filled
    for clique in self.cliques:
      for node in clique.nodes:
        # c contains all neighbours to clique
        c = list(self.node_to_clique[node])
        c.remove(clique)

        # Add neighbours to clique
        clique.add_neighbours(c)

  # The clique tree in human readable format
  def __str__(self):
    s = "\n  ".join([str(c) + " -> " + \
             ", ".join([str(x) for x in c.neighbours]) \
              for c in self.cliques])
    return "Clique Tree:\n  " + s

