# Build And Run
```shell
 g++ -std=c++11 demo.cpp
 ./a.out

# __FILE__ demo.cpp
# __FUNCTION__ main
# __PRETTY_FUNCTION__ int main()
# __LINE__ 11
# __DATE__ Jul  21 2020
# __TIME__ 18:42:22
# __TIMESTAMP__ Sun Jul  21 18:41:41 2020
# 11:18:00 [INFO] demo.cpp:16 - successfully
```
# FYI
**Predefined compiler macros** are special identifiers automatically defined by the C++ compiler that expand to useful compilation-time constants like the ***current line number, filename, function name, and timestamp***, providing essential context information during preprocessing.​​

Examples: ***__LINE__, __FILE__, __DATE__, __TIME__, __func__, __FUNCTION__, __PRETTY_FUNCTION__, __cplusplus***
