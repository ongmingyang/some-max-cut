import sys, csv, argparse
import logging as log
sys.path.insert(0,'python')
from maxCut import max_cut

def main(path):
  f = open(path, 'r')
  g = csv.reader(f,delimiter=" ")
  print max_cut(g)
  f.close()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("inputfile", help="path to file")
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
  args = parser.parse_args()
  if args.verbose:
    log.basicConfig(format="%(message)s", level=log.DEBUG)
  main(args.inputfile)

