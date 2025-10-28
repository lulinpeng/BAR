#include <iostream>
#include <vector>
using namespace std;

const int N = 35;
const int M = 300;

void f3() {
  for (uint64_t i = 0; i < 50000000; i++)
    for (uint64_t j = 0; j < ((uint64_t)1 << 63); j++) j = j * j + 10;
  cout << "f3" << endl;
}

void f2() { f3(); }

void f1() { f2(); }

void f0() { f1(); }

void f() { f0(); }

long fibonacci(int n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

void mat_mul(double a[M][M], double b[M][M], double c[M][M]) {
  for (int i = 0; i < M; i++)
    for (int j = 0; j < M; j++)
      for (int k = 0; k < M; k++) c[i][j] += a[i][k] * b[k][j];
}

int main() {
  f();

  long res = fibonacci(N);
  cout << "fibonacci " << res << endl;

  double a[M][M];
  double b[M][M];
  double c[M][M];
  mat_mul(a, b, c);
  cout << "matrix multiplication done" << endl;

  return 0;
}
