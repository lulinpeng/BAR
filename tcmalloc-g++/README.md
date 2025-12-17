# INTRO
```tcmalloc``` records ***how much memory has been allocated so far*** and ***how much is still in use and not yet released.*** Further, the sampling report can show ***which functions are using how much memory***.

*When an application is **linked with the TCMalloc** library (typically via a compiler flag like -ltcmalloc), TCMalloc's allocation functions effectively **"take over" all calls** to the standard memory management routines. The program continues to call malloc()and free()as usual, but these calls are **transparently redirected** to TCMalloc's implementation.*

```shell
Dumping heap profile to ./profiles/heap.0001.heap (2 MB allocated cumulatively, 1 MB currently in use)
```
# ENV

```shell
Machine: Intel Xeon
ubuntu:22.04
apt update && apt install -y libgoogle-perftools-dev google-perftools
```

# BUILD
```shell
g++ -std=c++11 -g -o simple_memory_growth simple_memory_growth.cpp -ltcmalloc -pthread
```

# RUN
```shell
export HEAPPROFILE=./profiles/heap # path for profile
export HEAP_PROFILE_ALLOCATION_INTERVAL=2097152 # generate a profile for every 2MB allocated
./simple_memory_growth

# Starting tracking the heap
# PID: 4130
# 0-th memory leak: 1 MB
# free
# 1-th memory leak: 2 MB
# Dumping heap profile to ./profiles/heap.0001.heap (2 MB allocated cumulatively, 1 MB currently in use)
# 2-th memory leak: 1 MB
# 3-th memory leak: 2 MB
# free
# 4-th memory leak: 1 MB
# Dumping heap profile to ./profiles/heap.0002.heap (4 MB allocated cumulatively, 3 MB currently in use)
# 5-th memory leak: 2 MB
# 6-th memory leak: 1 MB
# ...
# 22-th memory leak: 1 MB
# Dumping heap profile to ./profiles/heap.0008.heap (18 MB allocated cumulatively, 12 MB currently in use)
# 23-th memory leak: 2 MB
# 24-th memory leak: 1 MB
# free
```

# ANALYSIS
```shell
google-pprof --list=main ./simple_memory_growth ./profiles/heap.0008.heap

# Using local file ./simple_memory_growth.
# Argument "MSWin32" isn't numeric in numeric eq (==) at /usr/bin/google-pprof line 5047.
# Argument "linux" isn't numeric in numeric eq (==) at /usr/bin/google-pprof line 5047.
# Using local file ./profiles/heap.0008.heap.
# ROUTINE ====================== main in /yuanlu/tcmalloc-g++/simple_memory_growth.cpp
#    0.0   12.0 Total MB (flat / cumulative)
#      .      .   11: char* foo1(uint32_t mem_size) {
#      .      .   12:   char *p = new char[mem_size];
#      .      .   13:   return p;
#      .      .   14: }
#      .      .   15:
# ---
#      .      .   16: int main() {
#      .    0.0   17:   std::cout << "PID: " << getpid() << std::endl;
#      .      .   18:   char *p = nullptr;
#      .      .   19:   for (int i = 0; i < 200; ++i) {
#      .      .   20:     if ((i & 1) == 0) {
#      .    4.0   21:       p = foo0(1024 * 512);
#      .      .   22:       std::cout << i << "-th memory leak: 1 MB" << std::endl;
#      .      .   23:     } else {
#      .    8.0   24:       p = foo1(1024 * 512 * 2);
#      .      .   25:       std::cout << i << "-th memory leak: 2 MB" << std::endl;
#      .      .   26:     }
#      .      .   27:     if (i % 3 == 0) {
#      .      .   28:         std::cout << "free" << std::endl;
#      .      .   29:         delete[] p;
#      .      .   30:     }
#      .      .   31:     std::this_thread::sleep_for(std::chrono::milliseconds(500));
#      .      .   32:   }
#      .      .   33:
#      .      .   34:   std::cout << "sleep 5 seconds..." << std::endl;
#      .      .   35:   std::this_thread::sleep_for(std::chrono::seconds(5));
#      .      .   36:   std::cout << "process exit " << std::endl;
#      .      .   37:   return 0;
#      .      .   38:
# ---
```
