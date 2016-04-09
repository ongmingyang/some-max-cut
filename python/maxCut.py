import cliqueTree as ct
import beliefPropagation as bp
from factorTable import FactorTable

#
# Performs max cut on a set of edges, and returns node assignments
#
# @param edges    An iterator containing edges
#
def max_cut(edges):
  I, J = zip(*(sorted(row, reverse=True) for row in edges))
  I = [int(i) for i in I]
  J = [int(j) for j in J]
  c = ct.graph_to_clique_tree(I,J)
  clique_id = 0
  m = bp.max_marginal(c, clique_id)
  bp.traceback(c, clique_id, m)
  return m
