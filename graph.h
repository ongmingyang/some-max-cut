#include <stdio.h>
#include <string.h>

typedef struct Node {
  char description[32];
} Node;

typedef struct Factor {
  int vars; // Number of variables
} Factor;

// Create a junction tree given an input matrix
void create_junction_tree(int* matrix);

