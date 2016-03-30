from itertools import product

#
# A FactorTable object represents a factor/potential table
#
# @param nodes    The nodes corresponding to the scope of the factor
#
class FactorTable:
  def __init__(self, nodes):
    row_generator = product([-1,1], repeat=len(nodes))
    self.node_indices = sorted(nodes)
    self.rows = {x: -sum(x) for x in row_generator}

  # Returns the associated log potential of the assignment
  #
  # @param assignment    An assignment like {4:1, 5:-1} means node 4 is
  #                      assigned 1 and node 5 is assigned -1. Represents a
  #                      valid binary assignment over all node indices
  def eval_row(self, assignment):
    tup = tuple([assignment[x] for x in self.node_indices])
    return self.rows[tup]

  # Updates the log potential of the assignment
  #
  # @param assignment    An assignment like {4:1, 5:-1} means node 4 is
  #                      assigned 1 and node 5 is assigned -1. Represents a
  #                      valid binary assignment over all node indices
  # @param new_potential The new potential assigned to the variable assignment
  #
  def update_row(self, assignment, new_potential):
    tup = tuple([assignment[x] for x in self.node_indices])
    self.rows[tup] = new_potential
    
  # Returns a FactorTable that is the product of the current table and
  # the other table. The new table has a scope that is the union of the
  # scopes of the two tables
  #
  # @param other    An instance of FactorTable that represents the other
  #                 table
  def __mul__(self, other):
    cv = self.node_indices
    lv = other.node_indices
    new_scope = list(set(cv) + set(lv))
    sepset = list(set(cv) - set(lv))
    new_table = FactorTable(new_scope)

    # Indicator vector if variable is in the scope of the two table
    i_cv = [(x in cv) for x in new_scope]
    i_lv = [(x in lv) for x in new_scope]

    for new_assignment in new_table.rows:
      # Determine row in current and other tables
      cv_row = tuple([v for i,v in enumerate(new_assignment) if i_cv[i]])
      lv_row = tuple([v for i,v in enumerate(new_assignment) if i_lv[i]])

      # Compute joint product
      new_table[new_assigment] = self.rows[cv_row] + other.rows[lv_row]

    return new_table
