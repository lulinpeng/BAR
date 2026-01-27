# Env
## MacOS
```shell
brew update && brew install solidity npm foundry

solc --version # Version: 0.8.33+commit.64118f21.Darwin.appleclang

npm -v # 11.7.0

node --version # v25.3.0

forge --version # forge Version: 1.5.1-Homebrew

cast --version # cast Version: 1.5.1-Homebrew
```
## Linux
```shell
#ubuntu:22.04
cd xxx/
docker run -d -it --name chain -p 10000:10000 --mount type=bind,source="$(pwd)",target=/test ubuntu:22.04

apt update && apt upgrade -y 
apt install -y git jq curl python3-pip nodejs npm
node --version # v12.22.9
npm --version # 8.5.1

# install Rust (for Foundry)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env
rustc --version # rustc 1.93.0 (254b59607 2026-01-19)

curl -L https://foundry.paradigm.xyz | bash
source $HOME/.bashrc
foundryup
forge --version # forge Version: 1.5.1-stable
cast --version # cast Version: 1.5.1-stable

pip3 install solc-select
solc-select install 0.8.20
solc-select use 0.8.20
solc --version # Version: 0.8.20
```


# Demo
```shell
cd simple-storage/
git init
forge install foundry-rs/forge-std

export PRIVATE_KEY=0x...

# deploy the contract
forge script script/DeploySimpleStorage.s.sol --broadcast --rpc-url $SEPOLIA_RPC_URL

# check the contract on sepolia-explorer
https://sepolia.etherscan.io/tx/[tx hash 0x...]
https://sepolia.etherscan.io/address/[address 0x...]


CONTRACT_ADDRESS=0x9089bc120ab13f8e831aa5f3d2a46bc8aa3a5a22

export SEPOLIA_RPC_URL=https://api.zan.top/node/v1/eth/sepolia/[api key]
export ETH_RPC_URL=https://api.zan.top/node/v1/eth/sepolia/[api key]

# check balance of contract account
cast balance $CONTRACT_ADDRESS
# 0

# transfer to contract account
cast send $CONTRACT_ADDRESS --value 0.001ether --rpc-url $SEPOLIA_RPC_URL --private-key $PRIVATE_KEY

# check balance of contract account again
cast balance $CONTRACT_ADDRESS 
# 1000000000000000

# check nonce of some address account
cast nonce $CONTRACT_ADDRESS
# 1

# check contract bytecode
cast code $CONTRACT_ADDRESS
# 0x6080604052600436106100715...

# check constract storage
cast storage $CONTRACT_ADDRESS 0
# 0x000...0000

# call contract interface
cast send $CONTRACT_ADDRESS "set(uint256)" 666 --private-key $PRIVATE_KEY

# check constract storage again
cast storage $CONTRACT_ADDRESS 0
# 0x000...029a
```

## More About ```cast```
```shell
# get the latest block number
cast block-number

# get the latest gas-price
cast gas-price

# check a block
cast block <block number>

# check a transaction
cast tx <tx hash> # tx hash is calculated by on-chain node

# check the receipt of a transaction
cast receipt <tx hash>

# create new wallet
cast wallet new
# Successfully created new keypair.
# Address:     0x0846a22d0...
# Private key: 0x86d4daf4b...
```

# Run Tests
```shell
cd simple-storage/
git init
forge install foundry-rs/forge-std

# build
forge build --sizes

# run tests
forge test -vv
forge test --match-test testReceiveEther -vv

# generate gas report
forge test --gas-report

# call contract function
export PRIVATE_KEY=0x...
export CONTRACT_ADDRESS=0x182B0f58Fcd4Ca9Ab94A8372fAb28c393f5801B1
forge script script/ReadSimpleStorage.s.sol --rpc-url $SEPOLIA_RPC_URL
forge script script/CallSetFunction.s.sol --rpc-url $SEPOLIA_RPC_URL
```

# ByteCode

```shell
forge inspect src/SimpleStorage.sol:SimpleStorage bytecode # Creation Bytecode (deployment) = Constructor Logic + Runtime Bytecode. The constructor executes once and is discarded, leaving only the runtime code on-chain.

forge inspect src/SimpleStorage.sol:SimpleStorage deployedBytecode # Runtime Bytecode
# 0x608060405260043610610071575f3560e01c8063893d20e81161004c578063...
```

## Disassemble
```shell
forge inspect src/SimpleStorage.sol:SimpleStorage deployedBytecode > bytecode.hex

cast disassemble < bytecode.hex

# 00000000: PUSH1 0x80
# 00000002: PUSH1 0x40
# 00000004: MSTORE
# 00000005: PUSH1 0x04
# 00000007: CALLDATASIZE
# 00000008: LT
# 00000009: PUSH2 0x0071
# 0000000c: JUMPI
# 0000000d: PUSH0
# 0000000e: CALLDATALOAD
# 0000000f: PUSH1 0xe0
# ...
```