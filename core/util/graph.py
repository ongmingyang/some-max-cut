#
# A graph G = (V,E) is a set of nodes V and a set of edges E
#
class Graph:
  def __init__(self):
    self.nodes = []
    self.edges = {} # Dictionary of {edge: weight}

  # Returns a list of edges sorted by weight in decreasing order
  def get_sorted_edges(self, r=True):
    return sorted(self.edges, key=self.edges.get, reverse=r)

