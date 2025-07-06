# Test Machine
Apple MacBook Pro (14-inch, M4, 2024). Specs: Apple M4 chip (10-core CPU/16-core GPU), 24GB Unified Memory, macOS [Sequoia 15.3.1]

# Version
```shell
ollama v0.9.5

go version go1.24.1 darwin/arm64
```
# Build
```shell
git clone https://github.com/ollama/ollama.git
cd ollama/
git checkout v0.9.5
# brew install go
go env -w GOPROXY=https://goproxy.cn,direct
go build -ldflags="-s -w" -o ollama -buildvcs=false   .
```

# Run
## Start Ollama Server
```shell
export OLLAMA_HOST=0.0.0.0:11439
export OLLAMA_FLASH_ATTENTION=1
export OLLAMA_KEEP_ALIVE=100m
```

```shell
./ollama serve  # add '--verbose' for details
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
Refer to https://github.com/ollama/ollama/blob/v0.9.5/api/types.go#L416 for more details.
