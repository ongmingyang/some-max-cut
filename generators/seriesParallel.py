'''
Generates a series parallel graph

Usage:
$ python seriesParallel.py <n> <outputfile>
'''

import random, argparse

class Node:
  def __init__(self):
    self.neighbours = set()
    self.index = None

  # Creates an edge between self and other
  def connect(self, other):
    self.neighbours.add(other)
    other.neighbours.add(self)

  # Removes an edge between self and other
  def disconnect(self, other):
    self.neighbours.discard(other)
    other.neighbours.discard(self)

  # Merge other node into self
  def merge(self, other):
    while other.neighbours:
      neighbour = other.neighbours.pop()
      self.connect(neighbour)
      other.disconnect(neighbour)

class Graph:
  def __init__(self):
    self.s = Node()
    self.t = Node()
    self.s.connect(self.t)

  # Self becomes a series combination of self and other
  def serify(self, other):
    self.t.merge(other.s)
    self.t = other.t

  # Self becomes a parallel combination of self and other
  def parallelify(self, other):
    self.s.merge(other.s)
    self.t.merge(other.t)

def generate(n):
  if n <= 1:
    return Graph()

  # Random partition
  n1 = random.randint(1,n-1)
  n2 = n - n1
  G1 = generate(n1)
  G2 = generate(n2)

  # Select series or parallel composition at random  
  random.choice([G1.serify, G1.parallelify])(G2)
  return G1

def bfs(graph, start, f):
  index = 0
  visited, queue = set(), [start]
  while queue:
    v = queue.pop(0)
    if v not in visited:
      visited.add(v)
      for w in v.neighbours:
        if w not in visited:
          queue.append(w)
          if w.index is None:
            index += 1
            w.index = index
        if v.index < w.index:
          f.write("%d %d\n" % (v.index, w.index))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("n", help="series parallel recursion tree depth")
  parser.add_argument("outputfile", help="path to output file")
  args = parser.parse_args()

  G = generate(int(args.n))
  f = open(args.outputfile, 'w')
  G.s.index = 0
  bfs(G,G.s,f)
  f.close()
