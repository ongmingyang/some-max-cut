from util.node import Node
from util.table import Table 

#
# A Clique object represents a clique in the clique tree
# TODO this really should be a bag, because the nodes in the bag are not
# necessarily a clique
#
# @param nodes    A list of nodes representing the scope of the clique
# @param matrix   A pointer to the original adjacency matrix of the graph,
#                 used to determine factor table potentials
#
class Clique(Node):
  # Instantiation generates the potential table
  def __init__(self, index, nodes, matrix):
    Node.__init__(self, index)
    self.nodes = sorted(nodes)
    self.potential = Table(nodes, matrix)
    self.belief = None

  def sepset(self, other):
    return list(set(self.nodes) & set(other.nodes))

  # Returns a list of variables representing the sepset of self and other
  def determine_sepset_size(self, other):
    return len(sepset(other))

  # The clique in human readable format
  def __repr__(self):
    return "(%s)" % str(self.nodes)

