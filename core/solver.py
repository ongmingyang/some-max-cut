import cliqueTree as ct
import beliefPropagation as bp

class Solver:
  #
  # @param edges    An iterator containing edges
  #
  def __init__(self, edges):
    self.edges = edges # iterator
    self.solution = Solution()

  #
  # Performs max cut on a set of edges, and returns node assignments
  #
  def solve(self):
    J, I = zip(*(sorted((int(i),int(j))) for i,j in self.edges))
    c = ct.CliqueTree(list(I),list(J))
    clique_id = 0
    m = bp.max_marginal(c, clique_id)
    bp.traceback(c, clique_id, m)

    # Include graph statistics in solution
    self.solution.number_of_nodes = c.n
    self.solution.max_clique_size = c.max_clique_size
    self.solution.number_of_edges = len(I)
    self.solution.assignment = m
    self.solution.opt = self.eval_cut(I, J, m)
    return self.solution

  #
  # Finds the value of the cut
  #
  # @param U           List containing first coordinate of edge
  # @param V           List containing second coordinate of edge
  # @param partition   A dictionary assigning nodes to partition
  #
  def eval_cut(cls, U, V, partition):
    return sum(1 - partition[U[i]]*partition[V[i]] \
            for i in xrange(len(U)))/2

#
# "Case class" representing a solution returned to the user
#
class Solution:
  maximum_clique = None
  number_of_edges = None
  number_of_nodes = None
  opt = None
  assignment = None
  
