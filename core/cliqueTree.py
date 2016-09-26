#
# A CliqueTree is a CliqueIntersectionGraph with the following properties: 1.
# it is a tree, 2. cliques in the graph have the running intersection property
#
# @param cig        An instance of CliqueIntersectionGraph
#
class CliqueTree:
  # Instantiation creates a clique list and connects each clique to all its
  # neighbours in the tree
  def __init__(self, cig):
    self.cliques = cig.cliques

    # The maximum spanning tree turns a clique intersection graph into a
    # clique tree
    # TODO the representation of the tree should be explicit in the
    # CliqueTree object, not encapsulated in Node connections
    cig.maximum_spanning_tree()
          
  # The clique tree in human readable format
  def __repr__(self):
    s = "\n  ".join([str(c) + " -> " + \
             ", ".join([str(x) for x in c.get_neighbours()]) \
              for c in self.cliques])
    return "Clique Tree:\n  " + s

