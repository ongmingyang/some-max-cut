Some Max Cut
------------

This is an exact solver for instances of the QUBO problem. Given a symmetric
`Q`, we want to obtain an assignment `x` such that `x'Qx` is maximized, with
the restriction on `x` being that every `x_i` in `x` takes on the value `1` or
`-1`.

We can think of `Q` as the adjacency matrix of a weighted graph `G`, then the
maximizing assignment for `x'Qx` is simply the maximum cut of the graph.

There are some dependencies in this project. You can run `make install` to
install them.

Running
-------

To run the main procedure, do

```
$ make INPUT=<inputfile>
```

The input file contains the edges of the graph. Each row is a triple `i, j, w`
representing an edge connecting node `i` to node `j` with edge weight `w`. For
example,

```
0 1 1
1 2 1
2 3 1
```

Represents the complete graph on three vertices. A list of sample graphs are
available in the directory `sample`

Tests
-----

```
$ make test
```

Runs the test suite. Or you could run each test individually with 
`python -m tests.nameOfTest`


Profiling
---------

To profile the script, do

```
$ make profile INPUT=<inputfile>
```
