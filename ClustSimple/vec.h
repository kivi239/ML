#include <cstdio>
#include <algorithm>

#include <iostream> // for debug, delete these lines later
using namespace std;

struct Vec {
  
  private:
  int size;
  float *coord; 

  public:
  Vec() : size(0), coord(NULL) {}

  Vec(int size, FILE *f) : size(size) {
    coord = new float[size];
    for (int i = 0; i < size; i++) {
      fscanf(f, "%f", &coord[i]);
    }
  }

  Vec(const Vec &x) {
    size = x.size;
    coord = new float[size];
    for (int i = 0; i < size; i++)
      coord[i] = x.coord[i];
  }

  ~Vec() {
    if (coord)  
      delete[] coord;
  }

  void print() {
    for (int i = 0; i < size - 1; i++)
      printf("%.4f ", coord[i]);
    printf("%.4f\n", coord[size - 1]); 
  }

  float sqdist(Vec x) {
    float sum = 0;
    for (int i = 0; i < size; i++)
      sum += (x.coord[i] - coord[i]) * (x.coord[i] - coord[i]);

    return sum;
  }

  float mindist(Vec *xs, int n) {
    float sum = 1e9;
    for (int i = 0; i < n; i++) {                                           
      float dist = sqdist(xs[i]);
      sum = std::min(dist, sum);
    }

    return sum;
  }

  Vec & operator = (Vec &x) {
    Vec tmp(x);
    this->swap(tmp);

    return *this;
  }

  void swap(Vec &x) {
    std::swap(x.size, size);
    std::swap(x.coord, coord);
  }
      
} ;
                                                     