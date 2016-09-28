'''
Generates an (M,N,L)-chimera graph

@param M   no. of vertical clusters
@param N   no. of horizontal clusters
@param L   bipartite graph has 2L nodes
'''
import argparse

def chimera(M,N,L,f):
  high = M*N*2*L
  for i in xrange(high):
    # Consider nodes on the left of each bipartition
    i_residue = i % (2*L)
    if i_residue < L:

      # Connect node to L nodes on other side of bipartition
      i_start = i - i_residue
      for j in xrange(L,2*L):
        f.write("%d %d 1\n" % (i,j+i_start))

      # Connect to lower cluster, if it exists
      j = N*2*L + i
      if j < high:
        f.write("%d %d 1\n" % (i,j))

    # Consider nodes on the right of the bipartition
    else:
      # Connect to right cluster, if it exists
      j = 2*L + i
      if i % (2*L*N) < j % (2*L*N):
        f.write("%d %d 1\n" % (i,j))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("m", help="no. of vertical clusters")
  parser.add_argument("n", help="no. of horizontal clusters")
  parser.add_argument("l", help="bipartite graph has 2L nodes")
  parser.add_argument("outputfile", help="path to output file")
  args = parser.parse_args()

  f = open(args.outputfile, 'w')
  chimera(int(args.m),int(args.n),int(args.l),f)
  f.close()
