# Version
```shell
ubuntu:22.04
apt install nlohmann-json3-dev
```

# BUILD
```shell
g++ -std=c++11 main.cpp
./a.out

# a: t1, b: 50, d: t2, e: 60
# {
#   "a": "t1",
#   "b": 50,
#   "c": {
#     "d": "t2",
#     "e": 60
#   }
# }
```
