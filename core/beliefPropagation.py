import logging as log
from util.table import max_projection, projection
from operator import mul

#
# Performs the max marginal operation on a clique tree, using the clique with
# index clique_id as the root
#
def max_marginal(tree, assignment):
  #root = tree.cliques[clique_id]
  root = tree.root.index
  root_belief = upwards_propagate(tree, root)
  #log.info("Final table: %s\n%s" % (root_belief.nodes, root_belief))
  assignment.update(root_belief.get_map())
  return

#
# Performs upwards pass from clique to parent clique. Returns message to parent
#
def upwards_propagate(tree, clique_id):
  children = tree.get_children(clique_id)
  parent = tree.get_parent_clique(clique_id)
  messages = [upwards_propagate(tree, child) for child in children]

  # Variables to retain
  clique = tree.get_clique(clique_id)
  sepset = clique.sepset(parent) if parent else clique.nodes

  if messages:
    message_table = reduce(mul,messages)
    #log.info("Clique %s receiving message table:\n%s\n%s" \
    #   % (clique, message_table.nodes, message_table))

    # TODO clique potential should be explicit in tree not implicit in clique
    psi = clique.potential * message_table
    clique.belief = psi
    new_table = max_projection(psi, sepset)

    #log.info("Table product with itself:\n%s\n%s" % (psi.nodes, psi))
  else:
    new_table = max_projection(clique.potential, sepset)

  #log.info("Performing upwards pass from clique %s to parent %s" \
  #       % (clique, parent))
  #log.info("Sending message: %s\n%s" % (new_table.nodes, new_table))
  return new_table

#
# Given the max marginal for x, we can find the maximizing values for y
# conditioned on the most probable assignment for x. This is known as a
# traceback procedure
#
def traceback(tree, assignment):
  #root = tree.cliques[clique_id]
  root = tree.root
  downwards_propagate(tree, assignment, root.index)

#
# Performs downward pass from clique to its children. Assigns variables along
# the way
#
def downwards_propagate(tree, assignment, clique_id):
  # Assign current clique
  clique = tree.get_clique(clique_id)
  table = clique.belief if clique.belief else clique.potential
  maximized_potential = projection(table, assignment)

  # Get MAP over current scope
  cur_assignment = maximized_potential.get_map()

  # Update MAP over combined scope
  assignment.update(cur_assignment)

  #log.info("Performing downwards pass:\n%s\n%s\n" % (clique, assignment))

  # Recurse onto children in tree
  for child_id in tree.children[clique_id]:
    downwards_propagate(tree, assignment, child_id)

