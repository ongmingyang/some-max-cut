from core.solver import Solver

import os, csv
import unittest

PATH = os.path.join(os.path.dirname(__file__), 'inputs')

class TestEndToEnd(unittest.TestCase):
  """
  End to end test cases.
  """
  def assertGraphOpt(self, filename, opt):
    f = open(os.path.join(PATH, filename))
    edges = csv.reader(f,delimiter=" ")
    solver = Solver(edges)
    solution = solver.solve()
    f.close()
    self.assertEqual(solution.opt, opt)

  def test_small_test_case(self):
    """
    This is a small test case with 8 edges and max cut = 7
    """
    self.assertGraphOpt("small_test_case", 7)

  def test_chimera_2_2_4(self):
    """
    The chimera_2_2_4 graph is bipartite, so max cut = no of edges
    """
    self.assertGraphOpt("chimera_2_2_4", 80)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestEndToEnd)
  unittest.TextTestRunner(verbosity=2).run(suite)
