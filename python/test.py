import cliqueTree as ct

# generate sparse matrix
I = [0, 1, 3, 1, 5, 2, 6, 3, 4, 5, 4, 5, 6, 5, 6]
J = [0, 0, 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 6]
#A = spmatrix(1.0, I, J, (7,7))

print ct.graph_to_clique_tree(I,J)

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
