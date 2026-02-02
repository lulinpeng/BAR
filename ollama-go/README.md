# Test Machine
Apple MacBook Pro (14-inch, M4, 2024). Specs: Apple M4 chip (10-core CPU/16-core GPU), 24GB Unified Memory, macOS [Sequoia 15.3.1]

# Version
```shell
ollama v0.15.2

go version go1.24.1 darwin/arm64
```
# Build
```shell
brew install go

git clone https://github.com/ollama/ollama.git
cd ollama/

export VERSION=v0.15.2
git checkout v0.15.2
go env -w GOPROXY=https://goproxy.cn,direct
go build -ldflags="-s -w" -o ollama_test -buildvcs=false   .

./ollama_test --version
```

## CUDA Version
```shell
cd ollama/
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES="86"
cmake --build build --config Release -j 16
ls -al build/lib/ollama/ # find all *.so
```

# Run
## Start Ollama Server
```shell
export OLLAMA_HOST=0.0.0.0:11439
export OLLAMA_FLASH_ATTENTION=1
export OLLAMA_KEEP_ALIVE=100m
# export OLLAMA_MODELS=/root.ollama/models # set ollama models path
```

```shell
export OLLAMA_PATH=xxx
export PATH=$PATH:$OLLAMA_PATH

ollama_test --version # check ollama version

ollama_test serve  # start ollama service

ollama_test list # list avaliable models
```
or 
```shell
go run . serve
```
## Access Ollama Server
```shell
export OLLAMA_HOST=0.0.0.0:11434

# pull a model
curl http://${OLLAMA_HOST}/api/pull -d '{"model":"llama3.2"}'

curl http://${OLLAMA_HOST}/api/generate -d '{"model": "llama3.2", "prompt":"Why is the sky blue?", "stream":false}'
```

# More about Ollama
## Directory Structure
Refer to https://github.com/ollama/ollama/blob/v0.9.5/api/types.go#L416 for more details.

```shell
tree ~/.ollama

# ├── config.yml
# ├── history
# ├── id_ed25519
# ├── id_ed25519.pub
# ├── logs
# │   ├── app.log
# │   └── server.log
# └── models
#     ├── blobs # raw data of models
#     │   ├── sha256-2d54d...897f9
#     │   ├── sha256-34bb5...e242b
#     │   ├── sha256-3e4cb...44e4f
#     │   ├── sha256-56bb8...d4dcb
#     │   ├── sha256-66b9e...e281e
#     │   ├── sha256-832dd...2e92e
#     │   ├── sha256-833f5...8e2a1
#     │   ├── sha256-966de...66396
#     │   ├── sha256-a70ff...9e0cd
#     │   ├── sha256-cff3f...fbbdb
#     │   ├── sha256-d18a5...8aa12
#     │   ├── sha256-dde5a...ccdff
#     │   ├── sha256-e18a7...336fc
#     │   ├── sha256-eabc9...d1a41
#     │   ├── sha256-eb440...55175
#     │   └── sha256-fcc5a...a265d
#     └── manifests # metadata of models, you can find here all things about the models
#         └── registry.ollama.ai
#             └── library
#                 ├── llama3.2
#                 │   └── latest
#                 ├── qwen2.5
#                 │   └── 32b
#                 └── qwen3
#                     └── 4b
```

## Edit

```shell
# parse ollama command
cmd/cmd.go

# all handlers for APIs
server/rouges.go

GenerateHandler # /api/generate
ChatHandler # /api/chat

```