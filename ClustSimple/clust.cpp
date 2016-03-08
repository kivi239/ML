#include <cstdio>
#include <cmath>
#include <algorithm>
#include "vec.h"
#include <ctime>
#include <vector>

#include <iostream> // for debug, delete these lines later
using namespace std;

const int K = 40;
const int Size = 2;
const int Iterations = 100;

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
  FILE *f = fopen(file_name, "r");
  int id_first = rand() % n;
  float tmp;
  for (int i = 0; i < id_first * Size; i++) { 
    fscanf(f, "%f", &tmp);
  }

  Vec first = Vec(Size, f);
  centers[0] = first;
  cerr << "found new center" << endl;
  fclose(f);
  float *distribution = new float[n];

  for (int step = 1; step < K; step++) {
    f = fopen(file_name, "r");
    for (int i = 0; i < n; i++) {
      Vec *vec = new Vec(Size, f);
      distribution[i] = vec->mindist(centers, step);
      delete vec;
    }

    int center_id = random_id(distribution, n);
    f = fopen(file_name, "r");
    for (int i = 0; i < center_id * Size; i++) { 
      fscanf(f, "%f", &tmp);
    }
    
    Vec center(Size, f);
    centers[step] = center;
    cerr << "found " << step << "centers"<< endl;
 
    fclose(f);
  }

  delete[] distribution;
}

void K_means(Vec *centers, int n) {
  int *clust_size  = new int[K];
  for (int it = 0; it < Iterations; it++) {
    cerr << "iteration " << it << endl;
    for (int i = 0; i < K; i++)
      clust_size[i] = 0;

    FILE *f = fopen(file_name, "r");
    Vec *new_centers = new Vec[K];
    for (int i = 0; i < K; i++)  {
      Vec *tmp = new Vec(Size);
      new_centers[i] = *tmp;
      delete tmp;
    }

    for (int i = 0; i < n; i++) {
      Vec *vec = new Vec(Size, f);
      int closest_center = 0;
      for (int j = 0; j < K; j++) {
        if (vec->sqdist(centers[j]) < vec->sqdist(centers[closest_center]))
          closest_center = j;
      }

      new_centers[closest_center] += *vec;
      clust_size[closest_center]++; 

      delete vec;
    }
    fclose(f);
  
    for (int i = 0; i < K; i++) {
      new_centers[i].print();
      new_centers[i] /= clust_size[i];
      new_centers[i].print();
    }

    for (int i = 0; i < K; i++) {
      centers[i] = new_centers[i];
      centers[i].print();
    }
    printf("\n");

    delete[] new_centers;
  }
  delete[] clust_size;
}

void print_clusters(Vec *centers, int n) {
  std::vector<std::vector<int> > clusters(K);
  
  FILE *f = fopen(file_name, "r");
  for (int i = 0; i < n; i++) {
      Vec *vec = new Vec(Size, f);
      int closest_center = 0;
      for (int j = 0; j < K; j++) {
        if (vec->sqdist(centers[j]) < vec->sqdist(centers[closest_center]))
          closest_center = j;
      }
      clusters[closest_center].push_back(i);
    }
  fclose(f);

  for (int i = 0; i < K; i++) {
    printf("Cluster #%d:\n", i);
    f = fopen(file_name, "r");
    int prev = 0;
    for (int j = 0; j < (int)clusters[i].size(); j++) {
      for (int k = 0; k < Size * (clusters[i][j] - prev); k++) {
        float tmp;
        fscanf(f, "%f", &tmp);
      }
      Vec *vec = new Vec(Size, f);
      vec->print();   
      delete vec;
      prev = clusters[i][j] + 1;
    }
  }
}

int main() {
  srand(time(NULL));
  FILE *f = fopen(file_name, "r");
  int t = clock();

  int n = 0;
  float tmp;
  while (fscanf(f, "%f", &tmp) != EOF) {
     n++;
  }
  fclose(f);
  
  n /= Size;
  cerr << "Number of vectors: " << n << endl;
  
  Vec *centers = new Vec[K];
  
  freopen("centers.txt", "w", stdout);
  cerr << "start K-means++ searching centers" << endl;
  K_meanspp(centers, n);
  cerr << "finish K-means++" << endl;
  for (int i = 0; i < K; i++)
    centers[i].print();

  cerr << "start clusterization" << endl;
  K_means(centers, n);
  

  freopen("clusters.txt", "w", stdout);
  print_clusters(centers, n);

  cerr << clock() - t << endl;
  return 0;
}