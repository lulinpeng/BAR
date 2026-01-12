#include <iostream>
#include <stdlib.h>
#include <time.h>
using namespace std;

int main() {
  time_t current_time = time(NULL);
  cout << "timestamp: " << (long)current_time << endl;

  struct tm *tm_info = localtime(&current_time);
  cout << tm_info->tm_year + 1900 << "-" << tm_info->tm_mon + 1 << "-" << tm_info->tm_mday << endl;
  
  srand(time(NULL));
  for (int i = 0; i < 5; i++) cout << "random number: " << rand() % 1000 << endl;
  return 0;
}