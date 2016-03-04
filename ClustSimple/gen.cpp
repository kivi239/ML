#include <cstdio>
#include <cmath>
#include <algorithm>

const int N = 100;

int main() {
	freopen("sample2d.in", "w", stdout);
	//srand(time(NULL))

	for (int i = 0; i < N / 4; i++) {
		double x = (rand() % 10000) * 1.0 / 100;
		double y = (rand() % 10000) * 1.0 / 100;

		printf("%.4lf %.4lf\n", x, y);
	}

	for (int i = 0; i < N / 4; i++) {
	  double x = (rand() % 3000) * 1.0 / 100;
	  double y = (rand() % 3000) * 1.0 / 100;
	   
	  printf("%.4lf %.4lf\n", x, y);
	}

	for (int i = 0; i < N / 4; i++) {
	  double x = (rand() % 3000) * 1.0 / 100 + 50;
	  double y = (rand() % 3000) * 1.0 / 100 + 70;
	   
	  printf("%.4lf %.4lf\n", x, y);
	}

	for (int i = 0; i < N / 4; i++) {
	  double x = (rand() % 3000) * 1.0 / 100;
	  double y = (rand() % 1000) * 1.0 / 100 + 80;
	   
	  printf("%.4lf %.4lf\n", x, y);
	}

	return 0;
}