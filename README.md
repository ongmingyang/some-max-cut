Some Max Cut
------------

This module requires cvx_opt and chompack.

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


Profiling
---------

To profile the script, run

```
python -m cProfile -s 'tottime' main.py <inputfile>
```
