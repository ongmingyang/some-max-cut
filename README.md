Some Max Cut
------------

There are some dependencies in this project. You can run `make install` to
install them.

Running
-------

To run the main procedure, do

```
$ make INPUT=<inputfile>
```

The input file contains the edges of the graph. For example,

```
0 1
1 2
2 3
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
