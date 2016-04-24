import cliqueTree as ct
import beliefPropagation as bp
from factorTable import FactorTable

#
# Performs max cut on a set of edges, and returns node assignments
#
# @param edges    An iterator containing edges
#
def max_cut(edges):
  J, I = zip(*(sorted((int(i),int(j))) for i,j in edges))
  c = ct.graph_to_clique_tree(list(I),list(J))
  clique_id = 0
  m = bp.max_marginal(c, clique_id)
  bp.traceback(c, clique_id, m)
  return m
