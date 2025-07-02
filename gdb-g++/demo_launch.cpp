#include <iostream>
using namespace std;

void g(int *q) { cout << *q << endl; }

void f(int *p) { g(p); }

int main() {
  int *ptr = nullptr;
  f(ptr);
  return 0;
}