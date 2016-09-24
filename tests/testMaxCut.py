from python.solver import Solver

import os, csv
import unittest

PATH = os.path.join(os.path.dirname(__file__), 'inputs')
op = lambda x: os.path.join(PATH, x)

class TestEndToEnd(unittest.TestCase):
  """
  End to end test cases.
  """

  def test_chimera_2_2_4(self):
    """ 
    The chimera_2_2_4 graph is bipartite, so max cut = no of edges
    """
    f = open(op("chimera_2_2_4"))
    edges = csv.reader(f,delimiter=" ")
    solver = Solver(edges)
    solution = solver.solve()
    f.close()
    self.assertEqual(solution.opt, 80)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestEndToEnd)
  unittest.TextTestRunner(verbosity=2).run(suite)
