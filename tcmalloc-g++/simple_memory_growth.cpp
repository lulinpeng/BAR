#include <chrono>
#include <iostream>
#include <thread>
#include <unistd.h>

char* foo0(uint32_t mem_size) {
  char *p = new char[mem_size];
  return p;
}

char* foo1(uint32_t mem_size) {
  char *p = new char[mem_size];
  return p;
}

int main() {
  std::cout << "PID: " << getpid() << std::endl;
  char *p = nullptr;
  for (int i = 0; i < 200; ++i) {
    if ((i & 1) == 0) {
      p = foo0(1024 * 512);
      std::cout << i << "-th memory leak: 1 MB" << std::endl;
    } else {
      p = foo1(1024 * 512 * 2);
      std::cout << i << "-th memory leak: 2 MB" << std::endl;
    }
    if (i % 3 == 0) {
        std::cout << "free" << std::endl;
        delete[] p;
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
  }

  std::cout << "sleep 5 seconds..." << std::endl;
  std::this_thread::sleep_for(std::chrono::seconds(5));
  std::cout << "process exit " << std::endl;
  return 0;
}
