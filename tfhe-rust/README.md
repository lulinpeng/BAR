# Env
```shell
ubuntu:22.04 on MacOS M4
```

# Run
```shell
cargo run --release
# +++ Target: min((a * b) >> b, c) & 1 = min((1344 + 5) >> 5, 7) & 1 +++
# 13:52:34 1. key generation ...
# 13:52:36 2. save keys into files ...
# 13:52:36 2. encrypting ...
# 13:52:36    2.1 a -> [a]
# 13:52:36    2.2 b -> [b]
# 13:52:36    2.3 c -> [c]
# 13:52:36    2.4 save ciphertexts into files
# 13:52:36 3. homomorhpic evaluation ...
# 13:52:36    3.1 [x] * [y]
# 13:52:37    3.2 [x] >> [y]
# 13:52:37    3.4 min([x], [y])
# 13:52:37    3.5 [x] & 1
# 13:52:37 4. decrypting
# 13:52:37 result 1

ls -alh
#  23K client_key.bin
# 258K encrypted_a.bin
# 258K encrypted_b.bin
#  65K encrypted_c.bin
#  65K encrypted_res.bin
# 119M server_key.bin
```