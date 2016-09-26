#
# Represents a Node in a graph
#
# @param index  The node ID
#
class Node:
  def __init__(self, index):
    self.index = index
    self.neighbours = set() # edges in a graph

  # Creates an edge between self and other cliques
  def connect(self, other):
    self.neighbours.add(other)
    other.neighbours.add(self)

  # Use this to get neighbours in the clique tree 
  def get_neighbours(self):
    return self.neighbours

