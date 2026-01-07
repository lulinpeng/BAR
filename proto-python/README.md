# Version
```shell
brew install protobuf
protoc --version # libprotoc 29.3

protobuf==5.29.5 # python
```

# Build
```shell
export PROTO_DIR=./proto
export PYTHON_OUTPUT_DIR=./generated
rm -rf ${PYTHON_OUTPUT_DIR} && mkdir ${PYTHON_OUTPUT_DIR}
protoc --proto_path=${PROTO_DIR} --python_out=${PYTHON_OUTPUT_DIR} $(find ${PROTO_DIR} -name '*.proto')
```

# Run

```shell
export PYTHONPATH="${PYTHONPATH}:${PYTHON_OUTPUT_DIR}"
python3 parser.py

# person: <class 'A.person_pb2.Person'>
# {'name': 'Alice', 'age': 18, 'emails': ['aaa@xxx.com', 'bbb@xxx.com'], 'scores': {'a': 5, 'b': 4}}
# book: <class 'addressbook_pb2.AddressBook'>
# {'holder': 'Bob', 'persons': [{'name': 'Alice', 'age': 18, 'emails': ['aaa@xxx.com', 'bbb@xxx.com'], 'scores': {'a': 5, 'b': 4}}]}
```
