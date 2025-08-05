# Test Machine
Apple MacBook Pro (14-inch, M4, 2024). Specs: Apple M4 chip (10-core CPU/16-core GPU), 24GB Unified Memory, macOS [Sequoia 15.3.1]
# Version
```shell
zsdt 1.5.7
# https://github.com/facebook/zstd/blob/v1.5.7/doc/README.md

bazel --version # bazel 8.2.1-homebrew
```
# Build
```shell
bazel build //:main -c opt --enable_bzlmod
./bazel-bin/main
# buf size: 100405
# out size: 22
# Time elapsed: 798 us
```
# Reference
ZSTD API: https://raw.githack.com/facebook/zstd/release/doc/zstd_manual.html
