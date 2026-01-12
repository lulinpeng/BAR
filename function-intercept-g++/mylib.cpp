#include <iostream>

double add(double a, double b) {
  std::cout << "[demo library: add function is called]" << std::endl;
  return a + b;
}

extern "C" {
    double multiply(double a, double b) {
        std::cout << "[demo library with extern C: multiply function is called]" << std::endl;
        return a * b;
      }
}