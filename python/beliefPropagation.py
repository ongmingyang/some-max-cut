import logging as log
from factorTable import compute_max, assign_max
from operator import mul

#
# Performs the max marginal operation on a clique tree, using the clique with
# index clique_id as the root
#
def max_marginal(tree, clique_id):
  root = tree.cliques[clique_id]
  visited = set()
  cpd = upwards_propagate(root, visited)
  return cpd.get_map()

#
# Performs upwards pass from clique to parent clique. Returns message to parent
#
def upwards_propagate(clique, visited, parent=None):
  children = set(clique.get_neighbours()) - set([parent]) - visited
  visited.update(children)
  messages = [upwards_propagate(child, visited, clique) for child in children]

  # Variables to retain
  lv = list(set(clique.nodes) & set(parent.nodes)) if parent else clique.nodes

  if messages:
    message_table = reduce(mul,messages)
    #log.info("Clique %s receiving message table:\n%s\n%s" \
    #   % (clique, message_table.nodes, message_table))

    psi = clique.potential * message_table
    new_table = compute_max(psi, lv)

    #log.info("Table product with itself:\n%s\n%s" % (psi.nodes, psi))
  else:
    new_table = compute_max(clique.potential, lv)

  #log.info("Performing upwards pass from clique %s to parent %s" \
  #       % (clique, parent))
  #log.info("Sending message: %s\n%s" % (new_table.nodes, new_table))
  return new_table

#
# Given the max marginal for x, we can find the maximizing values for y
# conditioned on the most probable assignment for x. This is known as a
# traceback procedure
#
def traceback(tree, clique_id, assignment):
  root = tree.cliques[clique_id]
  downwards_propagate(assignment, root)

#
# Performs downward pass from clique to its children. Assigns variables along
# the way
#
def downwards_propagate(assignment, clique, parent=None):
  # Assign current clique
  maximized_potential = assign_max(clique.potential, assignment)

  # Get MAP over current scope
  cur_assignment = maximized_potential.get_map()

  # Update MAP over combined scope
  assignment.update(cur_assignment)

  #log.info("Performing downwards pass:\n%s\n%s\n" % (clique, assignment))

  # Recurse onto children in tree
  for neighbour in clique.get_neighbours():
    if neighbour is parent: continue
    downwards_propagate(assignment, neighbour, clique)

