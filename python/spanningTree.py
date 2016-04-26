'''
This file includes algorithms that can compute the maximum weight spanning
tree of a graph. Two algorithms are included: kruskal and prim
'''

#
# Performs Kruskal's algorithm by modifying a weighted clique intersection
# graph
#
# @ param CIG   A weighted clique intersection graph
#
def kruskal(cliques, edges):
  parent = {c: c for c in cliques}
  edges = sorted(edges, key=edges.get, reverse=True)

  def find_set(clique):
    p = parent[clique]
    if p is clique: 
      return clique
    else:
      parent[clique] = find_set(p)
      return parent[clique]

  for ui,vi in edges:
    u,v = cliques[ui], cliques[vi]
    u_root, v_root = find_set(u), find_set(v)
    if u_root is not v_root:
      # Edge belongs in Clique Tree (MST)
      u.connect(v)
      parent[u_root] = v_root
    
def prim():
  raise NotImplementedError
