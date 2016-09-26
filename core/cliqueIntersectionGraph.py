from clique import Clique
from cvxopt import spmatrix, amd
from collections import defaultdict as dd
import chompack as cp
from util.graph import Graph

LARGEST_CLIQUE_SIZE = 20

#
# A CliqueIntersectionGraph is a graph (V,E), where V is a set of cliques, each
# bag containing a clique, and (i,j) in E if clique i and clique j have a non
# empty sepset
#
# @param I,J        (I[i],J[i]) is an edge in the original graph. 
#                   We require I > J
#
class CliqueIntersectionGraph(Graph):
  def __init__(self, I, J):
    Graph.__init__(self)
    self.cliques = self.nodes # We use a different alias to prevent confusion

    n = max(max(I),max(J))+1
    A = spmatrix(1, I+range(n), J+range(n))
    self.n = n

    # Compute symbolic factorization using AMD ordering
    # This automatically does a chordal completion on the graph
    symb = cp.symbolic(A, p=amd.order)

    # The factorization permutes the node indices, we need to unpermute these
    cliques = symb.cliques()
    perm = symb.p
    cliques = [[perm[i] for i in clique] for clique in cliques]

    # If the largest clique is above threshold, we terminate the algorithm
    self.max_clique_size = max(len(x) for x in cliques)
    if self.max_clique_size > LARGEST_CLIQUE_SIZE:
      sys.exit('''
      Chordal completion has clique of size %d,
      Max allowed size is %d,
      Program terminating...
      ''' % (self.max_clique_size, LARGEST_CLIQUE_SIZE))

    node_to_clique = dd(list)

    # Instantiate cliques and fill node_to_clique entries
    for index, nodes in enumerate(cliques):
      clique = Clique(index, nodes, A)
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
          self.edges[edge] = clique.determine_sepset_size(neighbour)

