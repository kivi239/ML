#include <cstdio>
#include <cmath>
#include <algorithm>
#include "Vec.h"
#include <ctime>

#include <iostream> // for debug, delete these lines later
using namespace std;

const int K = 5;
const int Size = 2;

#define file_name "sample2d.in"

// returns the id of new center according to the centers distribution
int random_id(float *distribution, int n) {
  float *prefix = new float[n + 1];
  prefix[0] = 0;
  for (int i = 1; i <= n; i++) 
    prefix[i] = prefix[i - 1] + distribution[i - 1];
  
  float p = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/prefix[n]));
  int l = 0, r = n;
  int m;
  while (l + 1 < r) {
    m = (l + r) / 2;
    if (prefix[m] > p)
      r = m;
    if (prefix[m + 1] <= p)
      l = m;
    if (prefix[m] <= p && p < prefix[m + 1])
      break;
  }

  return m;
}

// for centers initialization
void K_meanspp(Vec *centers, int n) {
  FILE *f = fopen("sample2d.in", "r");
  int id_first = rand() % n;
  int cur_id = 0;
  Vec *vec = new Vec();
  for (int i = 0; i <= id_first; i++) { 
    delete vec;
    vec = new Vec(Size, f); 
  }

  fclose(f);
  centers[0] = *vec;

  float *distribution = new float[n];

  for (int step = 1; step < K; step++) {
    for (int i = 0; i < n; i++) {
      vec = new Vec(Size, f);
      distribution[i] = vec->mindist(centers, step);
      delete vec;
    }

    int center_id = random_id(distribution, n);
    f = fopen(file_name, "r");
    for (int i = 0; i <= center_id; i++)
      vec = new Vec(Size, f);
    centers[step] = *vec; 
  }

  delete[] distribution;
}


int main() {
  srand(time(NULL));
  FILE *f = fopen(file_name, "r");

  int n = 0;
  char *tmp;
  while (fscanf(f, "  %s  ", &tmp) != EOF) {
     n++;
  }
  fclose(f);
  
  n /= Size;
    
  int *ids = new int[n];
  Vec *centers = new Vec[K];
  
  cerr << "finish count vectors" << endl;

  freopen("centers.txt", "w", stdout);
  K_meanspp(centers, n);
  for (int i = 0; i < K; i++)
    centers[i].print();


  return 0;
}