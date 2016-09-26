#
# A graph G = (V,E) is a set of nodes V and a set of edges E
#
class Graph:
  def __init__(self):
    self.nodes = []
    self.edges = {} # Dictionary of {edge: weight}

  #
  # Performs Kruskal's algorithm to obtain the maximum weight spanning tree
  #
  def maximum_spanning_tree(self):
    parent = {c: c for c in self.nodes}
    self.edges = sorted(self.edges, key=self.edges.get, reverse=True)

    def find_set(node):
      p = parent[node]
      if p is node: 
        return node
      else:
        parent[node] = find_set(p)
        return parent[node]

    for ui,vi in self.edges:
      u,v = self.nodes[ui], self.nodes[vi]
      u_root, v_root = find_set(u), find_set(v)
      if u_root is not v_root:
        # Edge belongs in MST
        u.connect(v) # TODO don't use internal node representation
        parent[u_root] = v_root
      
