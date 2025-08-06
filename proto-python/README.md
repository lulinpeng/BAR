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
```
