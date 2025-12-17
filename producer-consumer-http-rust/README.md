 # VERSION
```shell
cargo 1.89.0

flask==3.1.2
```

# RUN
```shell
# terminal 0
cd producer-consumer-http-rust/
python3 server.py

# terminal 1
cd cd producer-consumer-http-rust/
cargo run

# 2025-01-01T00:00:35.174453Z  INFO rust_http_demo: src/main.rs:45: producer: status 200
# 2025-01-01T00:00:35.174648Z  INFO rust_http_demo: src/main.rs:49: producer: send 0-th request
# 2025-01-01T00:00:35.175605Z  INFO rust_http_demo: src/main.rs:52: producer: tx send channel success, result ()
# 2025-01-01T00:00:35.175627Z  INFO rust_http_demo: src/main.rs:85: consumer: recv 0-th response: RpcResp { name: "xxx", time: "2025-01-01 00:00:35", id: 100 }
# 2025-01-01T00:00:35.176490Z  INFO rust_http_demo: src/main.rs:45: producer: status 200
# 2025-01-01T00:00:35.176542Z  INFO rust_http_demo: src/main.rs:49: producer: send 1-th request
# 2025-01-01T00:00:35.176567Z  INFO rust_http_demo: src/main.rs:52: producer: tx send channel success, result ()
# 2025-01-01T00:00:35.177270Z  INFO rust_http_demo: src/main.rs:45: producer: status 200
# 2025-01-01T00:00:35.177411Z  INFO rust_http_demo: src/main.rs:49: producer: send 2-th request
# 2025-01-01T00:00:35.177429Z  INFO rust_http_demo: src/main.rs:52: producer: tx send channel success, result ()
```
