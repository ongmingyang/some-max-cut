import stats
import cliqueTree as ct
import beliefPropagation as bp

#
# Performs max cut on a set of edges, and returns node assignments
#
# @param edges    An iterator containing edges
#
def max_cut(edges):
  J, I = zip(*(sorted((int(i),int(j))) for i,j in edges))
  stats.number_of_edges = len(I)
  c = ct.graph_to_clique_tree(list(I),list(J))
  clique_id = 0
  m = bp.max_marginal(c, clique_id)
  bp.traceback(c, clique_id, m)
  return m, eval_cut(I, J, m)

#
# Finds the value of the cut
#
# @param U           List containing first coordinate of edge
# @param V           List containing second coordinate of edge
# @param partition   A dictionary assigning nodes to partition
#
def eval_cut(U, V, partition):
  return sum(1 - partition[U[i]]*partition[V[i]] \
          for i in xrange(len(U)))/2
