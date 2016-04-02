from factorTable import FactorTable
from operator import mul

# Computes the maximum entries of the table after variables in lv have been
# eliminated. This method returns a new instance of FactorTable.
#
# TODO this function is bad as it touches the internal representation of
# table, maybe we should make this a method in FactorTable instead?
#
# @param table  The instance of FactorTable
# @param lv     A list of variables to be eliminated
def compute_max(table, lv):
  # Define current variables
  cv = table.nodes
  new_scope = list(set(cv) - set(lv))
  new_table = FactorTable(new_scope)

  # Indicator vector if variable is in new scope
  i_s = [(x in new_scope) for x in cv]

  # Iterate through all rows in the old table
  for old_assignment in table.rows: 
    # Determine row assignment in new table
    r = tuple([v for i,v in enumerate(old_assignment) if i_s[i]])

    # Update row in new table if necessary
    new_table.rows[r] = max(new_table.rows[r], table.rows[old_assignment])

  return new_table

#
# Performs the max marginal operation on a clique tree, using the clique with
# index clique_id as the root
#
def max_marginal(tree, clique_id=0):
  root = tree.cliques[clique_id]
  return upwards_propagate(root)

#
# Performs upwards pass from clique to parent clique. Returns message to parent
#
def upwards_propagate(clique, visited=set(), parent=None):
  visited.add(clique)
  children = set(clique.neighbours) - set([parent]) - visited
  messages = [upwards_propagate(child, visited, clique) for child in children]
  lv = parent.nodes if parent else []
  if messages:
    return compute_max(reduce(mul,messages), lv)
  else:
    return compute_max(clique.potential, lv)

#
# Given the max marginal for x, we can find the maximizing values for y
# conditioned on the most probable assignment for x. This is known as a
# traceback procedure
#
def traceback(tree, clique_id=0, assignment=None):
  pass
