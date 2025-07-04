# Test Machine
Apple MacBook Pro (14-inch, M4, 2024). Specs: Apple M4 chip (10-core CPU/16-core GPU), 24GB Unified Memory, macOS [Sequoia 15.3.1]
# Version
```shell
c-kzg-4844 v2.1.1
# https://github.com/ethereum/c-kzg-4844/archive/refs/tags/v2.1.1.tar.gz

bazel --version # bazel 8.2.1-homebrew
```
# Build
```shell
bazel build //:main --cxxopt=-std=c++14 -c opt --enable_bzlmod
```
# Run
```shell
./bazel-bin/main
# kzg commitment size: 48
# kzg commitment: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
# (the first 16 bytes of) blob: 00 01 02 03 04 06 07 00 00 00 00 00 00 00 00 00
# kzg commitment: 82 d4 84 99 53 7e cf ac 76 f8 aa 45 eb de b5 4d 3e cd 93 76 47 3a d7 68 fc 8f a1 e2 3a 9f ff ed 6f 2f f0 15 2f a1 66 aa 66 19 86 fd f1 e6 4c e2
```
