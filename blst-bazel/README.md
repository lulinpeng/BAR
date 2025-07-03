# Test Machine
Apple MacBook Pro (14-inch, M4, 2024). Specs: Apple M4 chip (10-core CPU/16-core GPU), 24GB Unified Memory, macOS [Sequoia 15.3.1]
# Version
```shell
blst v0.3.15
# https://github.com/supranational/blst/archive/refs/tags/v0.3.15.tar.gz

bazel --version # bazel 8.2.1-homebrew
```
# Build
```shell
bazel build //:main --cxxopt=-std=c++14 -c opt --enable_bzlmod
```
# Run
```shell
./bazel-bin/main
# msg: 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# hash: 0x094c4931fdb2f2af417c9e0322a9716006e8211fe9017f671ac6e3251300acca
# sk: 0x3562dbb3987d4feb5b898633cc9c812aec49f2c64cad5b34f5a086df199a124d
```
