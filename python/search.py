#
# Executes a depth first search on a clique tree, starting from a root node,
# and returns a list of the leaves
#
# If the graph has cycles, the list of leaves may not be accurate
#
# @param tree     An instance of cliqueTree
# @param rootid   The root node chosen to start the depth first search. If no
#                 root node is specified, it defaults to the first node
#
def depthFirstSearch(tree, rootid=0):
  root = tree.cliques[rootid]
  leaves = []
  visited = set()
  q = [root]
  while q:
    v = q.pop()
    if v not in visited:
      visited.add(v)
      descendents = v.neighbours - visited
      if descendents:
        q.extend(descendents)
      else:
        leaves.append(v)
  return leaves

