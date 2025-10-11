# Build
```shell
# install libs
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# generate 'service_pb2.py' and 'service_pb2_grpc.py'
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
```
<center><img src="graphviz.svg" ></center>

# Run
# Start server
```shell
python3 server.py

# Get request:
# name: "alice"
# age: 15

# Get request:
# id: "0x1234"

# send 1/4 chunk for request id 0x1234
# send 2/4 chunk for request id 0x1234
# send 3/4 chunk for request id 0x1234
# send 4/4 chunk for request id 0x1234
# Completed streaming for request id 0x1234
```
# Start client
```shell
python3 client.py # generate 'request.bin' and 'response.bin'

# Get response:
# names: "bob"
# names: "mike"
# names: "lisa"
# age: 20

# recv: chunk: "chunk0"

# recv: chunk: "chunk1"

# recv: chunk: "chunk2"

# recv: chunk: "chunk3"
```
