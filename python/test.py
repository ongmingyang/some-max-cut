import random
import cliqueTree as ct
import beliefPropagation as bp
from factorTable import FactorTable

# generate sparse matrix
I = [0, 1, 3, 1, 5, 2, 6, 3, 4, 5, 4, 5, 6, 5, 6]
J = [0, 0, 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 6]
#A = spmatrix(1.0, I, J, (7,7))

c = ct.graph_to_clique_tree(I,J)
print c

# compute symbolic factorization using AMD ordering
#symb = cp.symbolic(A, p=amd.order)
#csp = cp.cspmatrix(symb) + A # can use blkval=1.0 to init values
#print symb.sparsity_pattern(reordered=False, symmetric=False)
#print csp.spmatrix(reordered=False)
#print symb.p
#cliques = symb.cliques()
#print cliques

#clique_tree = ct.CliqueTree(cliques)
#print clique_tree
#print symb.sparsity_pattern(reordered=True, symmetric=False)
#print csp.spmatrix(reordered=True)
#print symb

n = len(c.cliques)
clique_id = random.randint(0,n-1)
m = bp.max_marginal(c, clique_id)
print "max marginal:"
print m
print "\n"

bp.traceback(c, clique_id, m)

print "final assignment:"
print m


#l = [1,2,3,4,5]
#a = FactorTable(l, True)
#print a.rows
#print a
