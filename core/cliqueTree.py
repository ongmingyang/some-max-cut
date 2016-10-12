from util.tree import Tree

#
# A CliqueTree is a CliqueIntersectionGraph with the following properties: 1.
# it is a tree, 2. cliques in the graph have the running intersection property
#
# @param cig        An instance of CliqueIntersectionGraph
#
class CliqueTree(Tree):
  # Instantiation creates a clique list and connects each clique to all its
  # neighbours in the tree
  def __init__(self, cig):
    self.cliques = cig.cliques

    # The maximum spanning tree turns a clique intersection graph into a
    # clique tree
    T = Tree.maximum_spanning_tree(cig)
    self.nodes = T.nodes
    self.children = T.children
    self.parent = T.parent
    self.root = T.root

  def get_parent_clique(self, index):
    i = self.parent[index]
    return self.nodes[i] if i else None
          
  def get_clique(self, index):
    return self.nodes[index]

  def get_children(self, index):
    return self.children[index]

  # The clique tree in human readable format
  def __repr__(self):
    s = "\n  ".join([str(c) + " -> " + \
             ", ".join([str(x) for x in c.get_neighbours()]) \
              for c in self.cliques])
    return "Clique Tree:\n  " + s

