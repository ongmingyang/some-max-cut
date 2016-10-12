from collections import defaultdict as dd

#
# A tree is a graph with no cycles
#
class Tree:
  def __init__(self, nodes, children, parent, root):
    self.nodes = nodes
    self.children = children # Dictionary of {node_id: [list of children_id]}
    self.parent = parent # Dictionary of {node_id: parent_id}
    self.root = root

  #
  # Performs Kruskal's algorithm to obtain the maximum weight spanning tree
  # from a graph object
  #
  @classmethod
  def maximum_spanning_tree(cls, graph):
    root_of = {c: c for c in graph.nodes}
    new_edges = dd(set)

    def find_set(node):
      p = root_of[node]
      if p is node: 
        return node
      else:
        root_of[node] = find_set(p)
        return root_of[node]

    for ui,vi in graph.get_sorted_edges():
      u,v = graph.nodes[ui], graph.nodes[vi]
      u_root, v_root = find_set(u), find_set(v)
      if u_root is not v_root:
        # Edge belongs in MST
        new_edges[u.index].add(v.index)
        new_edges[v.index].add(u.index)
        root_of[u_root] = v_root
      
    # Now, we have the root of the tree (0 is arbitrary, since they all point
    # to the main root anyway)
    root = find_set(graph.nodes[0])
    parent_of = dd(lambda: None)
    
    def connect_children(node, parent):
      if parent: new_edges[node].remove(parent)
      for child in new_edges[node]:
        parent_of[child] = node
        connect_children(child, node)

    connect_children(root.index, None)
    children = new_edges

    return Tree(graph.nodes, children, parent_of, root)
