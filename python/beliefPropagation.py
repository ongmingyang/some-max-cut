from factorTable import FactorTable
from operator import mul

#
# Computes the maximum entries of the table over the new scope lv. This method
# returns a new instance of FactorTable.
#
# @param table  The instance of FactorTable
# @param lv     A list of variables to remain i.e. the new scope of
#               FactorTable after marginal maximization
#
def compute_max(table, lv):
  # Define current variables
  old_scope = table.nodes
  new_scope = sorted(lv)
  new_table = FactorTable(new_scope)

  # Indicator vector if variable is in new scope
  i_s = [(x in new_scope) for x in old_scope]

  # Iterate through all rows in the old table
  for old_assignment in table.rows: 
    # Determine row assignment in new table
    r = tuple([v for i,v in enumerate(old_assignment) if i_s[i]])

    # Update row in new table if necessary
    new_table.rows[r] = max(new_table.rows[r], table.rows[old_assignment])

  return new_table

#
# Returns a new table that is maximized over the variables that are already
# assigned
#
# @param table          The instance of FactorTable
# @param assignment     A dictionary of variables that are already assigned,
#                       and their assignment values
#
def assign_max(table, assignment):
  # Define current variables
  cv = table.nodes
  new_scope = list(set(cv) - set(assignment))
  new_table = FactorTable(new_scope)

  # Indicator vector if variable is in new scope
  i_s = [(x in new_scope) for x in cv]

  # Iterate through all rows in the old table
  for old_assignment in table.rows: 
    reject, r = False, []
    for i,v in enumerate(old_assignment):
      if i_s[i]: r.append(v)
      else:
        if assignment[table.nodes[i]] is not v:
          reject = True
          break
      
    # Reject row if row is not compatible with assignment
    if reject: continue

    # If row is compatible, update row in new table
    r = tuple(r)
    new_table.rows[r] = table.rows[old_assignment]

  return new_table

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
  children = set(clique.neighbours) - set([parent]) - visited
  visited.update(children)
  messages = [upwards_propagate(child, visited, clique) for child in children]

  # Variables to retain
  lv = list(set(clique.nodes) & set(parent.nodes)) if parent else clique.nodes

  if messages:
    message_table = reduce(mul,messages)
    print "Clique " + str(clique) + " receiving message table: "
    print message_table.nodes
    print message_table
    print "Table product with itself:"
    psi = clique.potential * message_table
    print psi.nodes
    print psi
    new_table = compute_max(psi, lv)
  else:
    new_table = compute_max(clique.potential, lv)

  print "Performing upwards pass from clique " + str(clique)
  print "to parent " + str(parent)
  print "Sending message:"
  print new_table.nodes
  print new_table
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
def downwards_propagate(assignment, clique, visited=set(), parent=None):
  children = set(clique.neighbours) - set([parent]) - visited
  visited.update(children)

  # Assign current clique
  maximized_potential = assign_max(clique.potential, assignment)

  # Get MAP over current scope
  cur_assignment = maximized_potential.get_map()

  # Update MAP over combined scope, prioritizing newer assignment if conflicts
  # between node assignments arise
  assignment.update(cur_assignment)

  print "Performing downwards pass:"
  print clique
  print assignment
  print "\n"

  # Recurse onto children in tree
  for child in children:
    downwards_propagate(assignment, child, visited, clique)

