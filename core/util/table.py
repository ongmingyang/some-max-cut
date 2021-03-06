from itertools import product

#
# Returns a new table that is the projection of the domain of the old table
# onto sepset, with f(x) = max(f(inverse_projection(x)))
#
# @param table  The instance of Table
# @param sepset The new scope of Table after marginal maximization
#
def max_projection(table, sepset):
  # Define current variables
  old_scope = table.nodes
  new_scope = sorted(sepset)
  new_table = Table(new_scope)

  # Indicator vector if variable is in new scope
  i_s = [(x in new_table.nodes) for x in old_scope]

  # Iterate through all rows in the old table
  for old_assignment in table.rows: 
    # Determine row assignment in new table
    r = tuple([v for i,v in enumerate(old_assignment) if i_s[i]])

    # Update row in new table if necessary
    new_table.rows[r] = max(new_table.rows[r], table.rows[old_assignment])

  return new_table

#
# Returns a new table that is the projection of the domain of the old table to
# the space of unassigned variables
#
# @param table          The instance of Table
# @param assignment     A dictionary of variables that are already assigned,
#                       and their assignment values
#
def projection(table, assignment):
  # Define current variables
  old_scope = table.nodes
  new_scope = [x for x in old_scope if x not in assignment]
  new_table = Table(new_scope)

  # Indicator vector if variable is in new scope
  i_s = [(x in new_table.nodes) for x in old_scope]

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
    new_table.rows[tuple(r)] = table.rows[old_assignment]

  return new_table

#
# A Table object represents a potential table
#
# @param nodes        The nodes corresponding to the scope of the factor
# @param matrix       If matrix is set, each row with assignment x will be
#                     initialized with potential x'Ax, where A is the
#                     submatrix of matrix spanned by the indices in node. If
#                     matrix is not set, initialize all entries to 0.
#
class Table:
  def __init__(self, nodes, matrix=False):
    row_generator = product([-1,1], repeat=len(nodes))
    self.nodes = sorted(nodes)

    # Factor table is initialized to be clique
    if matrix:
      self.rows = {}
      for x in row_generator:
        self.rows[x] = 0

        # Computes x'Ax
        for i in xrange(len(self.nodes)):
          for j in xrange(i):
            self.rows[x] -= matrix[self.nodes[i],self.nodes[j]]*x[i]*x[j]

    else:
      self.rows = {x: 0 for x in row_generator}

  # Returns the associated log potential of the assignment
  #
  # @param assignment    An assignment like {4:1, 5:-1} means node 4 is
  #                      assigned 1 and node 5 is assigned -1. Represents a
  #                      valid binary assignment over all node indices
  def eval_row(self, assignment):
    tup = tuple([assignment[x] for x in self.nodes])
    return self.rows[tup]

  # Updates the log potential of the assignment
  #
  # @param assignment    An assignment like {4:1, 5:-1} means node 4 is
  #                      assigned 1 and node 5 is assigned -1. Represents a
  #                      valid binary assignment over all node indices
  # @param new_potential The new potential assigned to the variable assignment
  #
  def update_row(self, assignment, new_potential):
    tup = tuple([assignment[x] for x in self.nodes])
    self.rows[tup] = new_potential
    
  # Returns the MAP assignment of a factor table, in the form of a dictionary
  #
  def get_map(self):
    MAP = max(self.rows, key=self.rows.get)
    return {v: MAP[i] for i,v in enumerate(self.nodes)}

  # Returns a Table that is the product of the current table and
  # the other table. The new table has a scope that is the union of the
  # scopes of the two tables
  #
  # @param other    An instance of Table that represents the other
  #                 table
  #
  def __mul__(self, other):
    cv = set(self.nodes)
    lv = set(other.nodes)
    new_table = Table(cv | lv)

    # Indicator vector if variable is in the scope of the old tables
    i_cv = [(x in cv) for x in new_table.nodes]
    i_lv = [(x in lv) for x in new_table.nodes]

    for r in new_table.rows:
      # Determine row in current and other tables
      cv_row = tuple([v for i,v in enumerate(r) if i_cv[i]])
      lv_row = tuple([v for i,v in enumerate(r) if i_lv[i]])

      # Compute log linear joint product
      new_table.rows[r] = self.rows[cv_row] + other.rows[lv_row]

    return new_table

  #
  # Prints Table in human-readable format
  #
  def __str__(self):
    s = ""
    for i in sorted(self.rows):
      f = lambda x: "+" if x > 0 else "-"
      s += " ".join(f(x) for x in i) + " " + str(self.rows[i]) + "\n"
    return s

