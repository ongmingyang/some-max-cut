from itertools import product, combinations

#
# A FactorTable object represents a factor/potential table
#
# @param nodes        The nodes corresponding to the scope of the factor
# @param init_entires If init_entries is true, set entries to size of cut in
#                     clique, otherwise set entries to 0
#
class FactorTable:
  def __init__(self, nodes, init_entries=False):
    row_generator = product([-1,1], repeat=len(nodes))
    self.nodes = sorted(nodes)

    # Factor table is initialized to be clique
    if init_entries:
      entries = lambda x: -sum([y[0]*y[1] for y in combinations(x,2)])
      self.rows = {x: entries(x) for x in row_generator}
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

  # Returns a FactorTable that is the product of the current table and
  # the other table. The new table has a scope that is the union of the
  # scopes of the two tables
  #
  # @param other    An instance of FactorTable that represents the other
  #                 table
  #
  def __mul__(self, other):
    cv = self.nodes
    lv = other.nodes
    new_scope = list(set(cv) | set(lv))
    new_table = FactorTable(new_scope)

    # Indicator vector if variable is in the scope of the two table
    i_cv = [(x in cv) for x in new_scope]
    i_lv = [(x in lv) for x in new_scope]

    for r in new_table.rows:
      # Determine row in current and other tables
      cv_row = tuple([v for i,v in enumerate(r) if i_cv[i]])
      lv_row = tuple([v for i,v in enumerate(r) if i_lv[i]])

      # Compute log linear joint product
      # TODO is there an error here?
      new_table.rows[r] = self.rows[cv_row] + other.rows[lv_row]

    return new_table

  #
  # Prints FactorTable in human-readable format
  #
  def __str__(self):
    s = ""
    for i in sorted(self.rows):
      f = lambda x: "+" if x > 0 else "-"
      s += " ".join(f(x) for x in i) + " " + str(self.rows[i]) + "\n"
    return s

