#include <cstdio>
#include <cmath>
#include <algorithm>
#include <ctime>
#include <vector>

#include <iostream> 
using namespace std;

const int K = 40;
const int Size = 2;
const int Iterations = 100;
const int N = (int)1e7;

#define file_name "sample2d.in"

float centers[K][Size];
float new_centers[K][Size];
float vec[Size];
float distribution[N];
float prefix[N];
int clust_size[K];

// returns the id of new center according to the centers distribution
int random_id(int n) {
  prefix[0] = 0;
  for (int i = 1; i <= n; i++) 
    prefix[i] = prefix[i - 1] + distribution[i - 1];
  
  float p = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/prefix[n]));
  int l = 0, r = n;
  int m = (l + r) / 2;
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

float sqdist(float *x, float *y) {
  float sum = 0;
  for (int i = 0; i < Size; i++) {
    sum += (x[i] - y[i]) * (x[i] - y[i]);
  }

  return sum;
}

// returns the distance to the nearest center to x
float mindist(float *x, int n) {
  float sum = 1e9;
  for (int i = 0; i < n; i++) {                                           
    float dist = sqdist(x, centers[i]);
    sum = std::min(dist, sum);
  }

  return sum;
}

// divide all coordinates vector x by n
void division(float *x, float n) {
  for (int i = 0; i < Size; i++) {
    x[i] /= n;
  }
}

// adds y to x
void add(float *x, float *y) {
  for (int i = 0; i < Size; i++)
    x[i] += y[i];
}

void print(float *x) {
  for (int i = 0; i < Size - 1; i++)
    printf("%.4f ", x[i]);
  printf("%.4f\n", x[Size - 1]); 
}

// for centers initialization
void K_meanspp(int n) {
  FILE *f = fopen(file_name, "r");
  int id_first = rand() % n;
  float tmp;
  for (int i = 0; i < id_first * Size; i++) { 
    fscanf(f, "%f", &tmp);
  }

  for (int i = 0; i < Size; i++) {
    fscanf(f, "%f", &centers[0][i]);
  }

  cerr << "found new center" << endl;
  fclose(f);

  for (int step = 1; step < K; step++) {
    f = fopen(file_name, "r");
    for (int i = 0; i < n; i++) {
      for (int j = 0; j < Size; j++) {
  	    fscanf(f, "%f", &vec[j]);
	    }

      distribution[i] = mindist(vec, step);
    }
    fclose(f);

    int center_id = random_id(n);
    f = fopen(file_name, "r");
    for (int i = 0; i < center_id * Size; i++) { 
      fscanf(f, "%f", &tmp);
    }
    
    for (int i = 0; i < Size; i++) {
    	fscanf(f, "%f", &centers[step][i]);
    }
    cerr << "found " << step << " centers"<< endl;
 
    fclose(f);
  }
}

void K_means(int n) {
  for (int it = 0; it < Iterations; it++) {
    cerr << "iteration " << it << endl;
    for (int i = 0; i < K; i++)
      clust_size[i] = 0;

    FILE *f = fopen(file_name, "r");
    for (int i = 0; i < K; i++)  {
    	for (int j = 0; j < Size; j++) 
    		new_centers[i][j] = 0;
    }

    for (int i = 0; i < n; i++) {
      for (int j = 0; j < Size; j++)
      	fscanf(f, "%f", &vec[j]);
      int closest_center = 0;
      float mndist = 1e9;
      for (int j = 0; j < K; j++) {
        if (sqdist(vec, centers[j]) < mndist) {
          closest_center = j;
          mndist = sqdist(vec, centers[j]);
        }
        
      }

      add(new_centers[closest_center], vec);
      clust_size[closest_center]++; 
    }

    fclose(f);
  
    for (int i = 0; i < K; i++) {
      division(new_centers[i], clust_size[i]);
      print(new_centers[i]);
    }

    for (int i = 0; i < K; i++) {
      for (int j = 0; j < Size; j++)
      	centers[i][j] = new_centers[i][j];
    }
    printf("\n");
  }
}

void print_clusters(int n) {
  std::vector<std::vector<int> > clusters(K);
  
  FILE *f = fopen(file_name, "r");
  for (int i = 0; i < n; i++) {
      for (int j = 0; j < Size; j++)
      	fscanf(f, "%f", &vec[j]);

      int closest_center = 0;
      float mndist = 1e9;
      for (int j = 0; j < K; j++) {
        if (sqdist(vec, centers[j]) < mndist) {
          closest_center = j;
          mndist = sqdist(vec, centers[j]);
        }
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

      for (int k = 0; k < Size; k++)
      	fscanf(f, "%f", &vec[k]);

      print(vec);   
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
  
  freopen("centers.txt", "w", stdout);
  
  cerr << "start K-means++ searching centers" << endl;
  K_meanspp(n);
  
  cerr << "finish K-means++" << endl;
  
  puts("Initialize centers");
  for (int i = 0; i < K; i++)
    print(centers[i]);
  puts("");

  cerr << "start clusterization" << endl;
  K_means(n);
  cerr << "finish clasterization, " << (clock() - t) / CLOCKS_PER_SEC << endl;
  
  freopen("clusters.txt", "w", stdout);
  print_clusters(n);

  cerr << clock() - t << endl;
  
  return 0;
}