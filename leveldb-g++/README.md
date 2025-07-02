# Installation

```shell
brew install leveldb
```

# Build and Run
```shell
g++ main.cpp -std=c++11 -lleveldb -L/opt/homebrew/lib -I/opt/homebrew/include
./a.out testdb

# value of key1: Hello

# All Content:
# key1: Hello
# key2: LevelDB
# key3: Batch
# key4: Example

tree testdb
# testdb
# ├── 000005.ldb
# ├── 000008.ldb
# ├── 000009.log
# ├── CURRENT
# ├── LOCK
# ├── LOG
# ├── LOG.old
# └── MANIFEST-000007
```
