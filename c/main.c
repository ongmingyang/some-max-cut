#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>

#include "matrix.h"

static char* DEFAULT_INPUT_FILE_PATH = "A.in";

int* parse_file(int* dim) {
  int n;
  FILE *fin;
  fin = fopen(DEFAULT_INPUT_FILE_PATH, "r");
  assert(fin != NULL);

  // Read first line for dimension
  if (!fscanf(fin, "%d\n", &n)) exit(-1);

  // Malloc a matrix object to hold data
  int* matrix = (int *) malloc(sizeof(int) * n * n);

  for (int i=0;i<n;i++) {
    for (int j=0;j<n;j++) {
      if (!fscanf(fin, "%d", &matrix[n*i + j])) 
        exit(-1);
    }
  }

  // Close file pointer
  fclose(fin);

  *dim = n;
  return matrix;
}

int main(void) {
  int dim; // Matrix is square
  int *matrix = parse_file(&dim);

  // Verify input sum
  int sum = 0;
  for (int i = 0; i < dim*dim; i++) {
    sum += matrix[i];
  }
  printf("Sum of entries is %d\n", sum);

  int x[dim];
  cilk_for (int i=0; i<dim; i++) {
    x[i] = 1;
  }
  
  // Compute b = x'Ax where x is ones
  sum = objective(matrix, x, dim);
  printf("x'Ax is %d\n", sum); // should be the same

  // Try naive hillclimb
  sum = naive_hillclimb(matrix, x, dim);
  printf("Naive hillclimb is %d\n", sum); // should be the same
  printf("Vector is: \n( ");
  for (int i=0; i<dim; i++) {
    printf("%d ", x[i]);
  }
  printf(")\n");

  return 0;
}
