#include <iostream>
using namespace std;

void g(int *q) {
  int a = 0;
  while (true) {
    cout << "here is g" << endl;
    a += (a+1);
  }
}

void f(int *p) { g(p); }

int main() {
  int *ptr = nullptr;
  f(ptr);
  return 0;
}