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
  parents = {c: c for c in cliques}
  edges = sorted(edges, key=edges.get, reverse=True)

  def find_set(clique):
    if parents[clique] == clique: 
      return clique
    else: 
      parents[clique] = find_set(parents[clique])
      return parents[clique]

  def union(u,v):
    u_root = find_set(u)
    v_root = find_set(v)
    parents[u_root] = v_root

  for ui,vi in edges:
    u,v = cliques[ui], cliques[vi]
    if find_set(u) is not find_set(v):
      # Edge belongs in MST
      u.connect(v)
      union(u,v)
    
def prim():
  raise NotImplementedError
