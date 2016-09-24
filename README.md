Some Max Cut
------------

To run, do

```
$ python main.py <inputfile>
```

The input file contains the edges of the graph. For example,

```
0 1
1 2
2 3
```

Represents the complete graph on three vertices.

Tests
-----

`make test`

Or you could individually run each test with `python -m tests.nameOfTest`


Profiling
---------

To profile the script, run

```
python -m cProfile -s 'tottime' main.py <inputfile>
```
