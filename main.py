import sys, csv
sys.path.insert(0,'python')
from maxCut import max_cut

def main(argv):
  if argv == "-h":
    print "Usage: python main.py <inputfile>"
    sys.exit(1)
  else:
    path = argv
    f = open(path, 'r')
    g = csv.reader(f,delimiter=" ")
    print max_cut(g)
    f.close()

if __name__ == "__main__":
  try:
    arg = sys.argv[1]
  except:
    arg = "-h"
  main(arg)

