import logging as log
from cliqueIntersectionGraph import CliqueIntersectionGraph
from cliqueTree import CliqueTree
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
    arrange = lambda i,j,w: (min(i,j), max(i,j), w) 
    J, I, W = zip(*(arrange(int(i),int(j),int(w)) for i,j,w in self.edges))
    c = CliqueIntersectionGraph(list(I),list(J), list(W))
    ct = CliqueTree(c)

    # Current assignment
    m = {}
    bp.max_marginal(ct, m)
    bp.traceback(ct, m)

    # Include graph statistics in solution
    self.solution.number_of_nodes = c.n
    self.solution.max_clique_size = c.max_clique_size
    self.solution.number_of_edges = len(I)
    self.solution.assignment = m
    self.solution.opt = self.eval_cut(I, J, m)
    log.info("Final solution: %s\n" % (m))
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
  
