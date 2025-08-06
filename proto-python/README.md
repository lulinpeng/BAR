# Version
```shell
brew install protobuf
protoc --version # libprotoc 29.3

protobuf==5.29.5 # python
```

# Build
```shell
export PROTODIR=./proto
export PYPROTODIR=./generated
rm -rf ${PYPROTODIR} && mkdir ${PYPROTODIR}
protoc --proto_path=${PROTODIR} --python_out=${PYPROTODIR} $(find ${PROTODIR} -name '*.proto')
```

# Run

```shell
export PYTHONPATH="${PYTHONPATH}:${PYPROTODIR}"
python3 parser.py

# person: <class 'A.person_pb2.Person'>
# {'name': 'Alice', 'age': 18, 'emails': ['aaa@xxx.com', 'bbb@xxx.com'], 'scores': {'a': 5, 'b': 4}}
# book: <class 'addressbook_pb2.AddressBook'>
# {'holder': 'Bob', 'persons': [{'name': 'Alice', 'age': 18, 'emails': ['aaa@xxx.com', 'bbb@xxx.com'], 'scores': {'a': 5, 'b': 4}}]}
```
