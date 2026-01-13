#include <assert.h>
#include <dlfcn.h>
#include <iostream>
using namespace std;

int main() {
  // open a shared library
  // RTLD_LAZY, Lazy binding: resolve symbols only when they are actually used
  // RTLD_NOW, immediate binding: resolve all symbols at load time
  // RTLD_GLOBAL, Make symbols globally available for other loaded libraries
  // RTLD_LOCAL, Symbols are visible only to this dlopen() call
  void *lib_handle = dlopen("./libmylib.so", RTLD_LAZY);
  if (!lib_handle) {
    cout << "Error: " << dlerror() << endl;
    return 1;
  }

  dlerror(); // clear error info

  { // get function by symbol
    double (*add_func)(double, double) = (double (*)(double, double))dlsym(lib_handle, "_Z3adddd");
    assert(dlerror() == nullptr);
    // const char *error = dlerror();
    // cout << "Error: " << error << endl;
    // assert(error);
    cout << "Result: 1.1 + 2.2 = " << add_func(1.1, 2.2) << endl;
  }

  { // get function by symbol
    double (*multiply_func)(double, double) = (double (*)(double, double))dlsym(lib_handle, "multiply");
    // const char *error = dlerror();
    assert(dlerror() == nullptr);
    // cout << "Error: " << error << endl;
    // assert(error);
    cout << "Result: 1.1 * 2.2 = " << multiply_func(1.1, 2.2) << endl;
  }

  // close the shared library
  dlclose(lib_handle);
  return 0;
}
