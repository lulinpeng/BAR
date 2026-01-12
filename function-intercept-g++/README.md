# Env
```shell
ubuntu:22.04
```
# Function Interception
```shell

gcc -fPIC -shared -o libintercept.so intercept.c -ldl
g++ -o main_intercept main_intercept.cpp

export INTERCEPT=1
LD_PRELOAD=./libintercept.so ./main_intercept
# libintercept.so is loaded
# original time function address: time=0x7fffa51e4f40,
# timestamp: 1672531200
# 2023-1-1
# srand functon is called with parameter: seed = 1672531200
# random number: 42
# random number: 42
# random number: 42
# random number: 42
# random number: 42

unset INTERCEPT
LD_PRELOAD=./libintercept.so ./main_intercept
# libintercept.so is loaded
# original time function address: time=0x7fffb91cef40,
# timestamp: 1768207575
# 2026-1-12
# srand functon is called with parameter: seed = 1768207575
# random number: 42
# random number: 42
# random number: 42
# random number: 42
# random number: 42
```

The dynamic linker ***resolves symbols*** in the following **order**: 
1. the executable's own symbol table
2. libraries specified by ```LD_PRELOAD``` (in the order listed)
3. dependencies specified by the executable's DT_NEEDED entries (searched breadth-first)
4. standard system libraries

Note that ```LD_LIBRARY_PATH``` doesn't change this priority order but ***only affects where the linker searches*** for the library files on disk.

# Load Function by Symbol
```shell
g++ -shared -fPIC -o libmylib.so mylib.cpp
nm -D libmylib.so # list all symbols in the shared library
#                  w _ITM_deregisterTMCloneTable
#                  w _ITM_registerTMCloneTable
# 0000000000001179 T _Z3adddd
#                  U _ZNSolsEPFRSoS_E@GLIBCXX_3.4
#                  U _ZNSt8ios_base4InitC1Ev@GLIBCXX_3.4
#                  U _ZNSt8ios_base4InitD1Ev@GLIBCXX_3.4
#                  U _ZSt4cout@GLIBCXX_3.4
#                  U _ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_@GLIBCXX_3.4
#                  U _ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@GLIBCXX_3.4
#                  U __cxa_atexit@GLIBC_2.2.5
#                  w __cxa_finalize@GLIBC_2.2.5
#                  w __gmon_start__
# 00000000000011d0 T multiply

nm -D --demangle libmylib.so # more readable output
objdump -T libmylib.so # alternative using objdump

g++ -o main_dl main_dl.cpp -ldl
./main_dl
# Result: 1.1 + 2.2 = [demo library: add function is called]
# 3.3
# Result: 1.1 * 2.2 = [demo library with extern C: multiply function is called]
# 2.42
```

# About dlfcn.h
**dlopen:** loads a shared library (.so file) into memory and returns a handle. It can load libraries at runtime rather than at program startup.
>
>RTLD_LAZY, Lazy binding: resolve symbols only when they are actually used.
>
>RTLD_NOW, immediate binding: resolve all symbols at load time.
>
>RTLD_GLOBAL, Make symbols globally available for other loaded libraries.
>
>RTLD_LOCAL, Symbols are visible only to this dlopen() call.

**dlsym:** looks up a symbol (function or variable) by name in a loaded library and returns its address, enabling runtime symbol resolution.

**dlerror:** returns a human-readable error string if any of the DL functions fail, making debugging easier.

**dlclose:** decrements the reference count of a loaded library and unloads it if no longer needed, freeing resources.