import sys, csv, time, argparse
import logging as log
sys.path.insert(0,'python')
from maxCut import max_cut
import stats 

def timing(func):
  def wrapper(*args):
    start = time.time()
    res = func(*args)
    end = time.time()
    t = (end-start)
    print "Function <%s> took %0.5f seconds to run" \
          % (func.__name__, t)
    return res
  return wrapper

@timing
def main(path):
  f = open(path, 'r')
  edges = csv.reader(f,delimiter=" ")
  assignment, opt = max_cut(edges)
  f.close()
  return opt

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("inputfile", help="path to file")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
  args = parser.parse_args()
  if args.verbose:
    log.basicConfig(format="%(message)s", level=log.DEBUG)

  opt = main(args.inputfile)
  print "Graph has %d nodes, %d edges, with maximum clique size %d" \
        % (stats.number_of_nodes, stats.number_of_edges, stats.maximum_clique),
  print "and max cut of %d" % opt

