#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <cilk/reducer_opadd.h>

#include "matrix.h"

// compute the dot product of two vectors.
int dot_product(int *v, int *u, size_t n) {
  CILK_C_REDUCER_OPADD(sum, int, 0);
  CILK_C_REGISTER_REDUCER(sum);
  cilk_for (size_t i = 0; i < n; i++) {
    REDUCER_VIEW(sum) += v[i] * u[i];
  }
  CILK_C_UNREGISTER_REDUCER(sum);
  return sum.value;
}

// compute matrix * vector
void multiply_matrix_vector(int *matrix, int *vector, int *output, size_t n) {
  cilk_for (size_t i = 0; i < n; i++) {
    output[i] = dot_product(&matrix[i*n], vector, n);
  }
}

// compute x'Qx
int objective(int *matrix, int *vector, size_t n) {
  int b[n];
  multiply_matrix_vector(matrix, vector, b, n);
  return dot_product(vector, b, n);
}

// Iteratively finds better vectors and writes the vector to *vector
// This method is non-deterministic
// Assumes *vector is a valid vector to begin with
int naive_hillclimb(int *matrix, int *vector, size_t n) {
  int best = objective(matrix, vector, n);
  int can_climb = 1;

  while (can_climb) {
    can_climb = 0;
    cilk_for (int i=0; i<n; i++) {
      vector[i] *= -1;
      int new_obj = objective(matrix, vector, n);
      if (new_obj > best) {
        can_climb = 1;
        best = new_obj;
      } else {
        vector[i] *= -1;
      }
    }
  }

  return objective(matrix, vector, n);
}
