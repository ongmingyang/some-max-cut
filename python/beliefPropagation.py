from factorTable import FactorTable

# Computes the maximum entries of the table after variables in lv have been
# eliminated. This method returns a new instance of FactorTable.
#
# @param table  The instance of FactorTable
# @param lv     A list of variables to be eliminated
def compute_max(table, lv):
  # Define current variables
  cv = table.node_indices
  new_scope = list(set(cv) - set(lv))
  new_table = FactorTable(new_scope)

  # Indicator vector if variable is in new scope
  i_s = [(x in new_scope) for x in cv]

  # Iterate through all rows in the old table
  for old_assignment in table.rows: 
    # Determine row in new table
    row = tuple([v for i,v in enumerate(old_assignment) if i_s[i]])

    # Update row in new table if necessary
    new_table[row] = max(new_table[row], table.rows[old_assignment])

  return new_table

#
# Performs the max marginal operation on a clique tree
#
def max_marginal(tree, clique_id=0):
  pass
