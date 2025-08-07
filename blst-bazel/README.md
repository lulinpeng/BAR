# Test Machine
Apple MacBook Pro (14-inch, M4, 2024). Specs: Apple M4 chip (10-core CPU/16-core GPU), 24GB Unified Memory, macOS [Sequoia 15.3.1]
# Version
```shell
blst v0.3.15
# https://github.com/supranational/blst/archive/refs/tags/v0.3.15.tar.gz

bazel --version # bazel 8.2.1-homebrew
```
# Build
```shell
bazel build //:main --cxxopt=-std=c++14 -c opt --enable_bzlmod
```
# Run
```shell
./bazel-bin/main
# msg: 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# hash: 0x094c4931fdb2f2af417c9e0322a9716006e8211fe9017f671ac6e3251300acca
# sk: 0x3562dbb3987d4feb5b898633cc9c812aec49f2c64cad5b34f5a086df199a124d
```


# BLS Signature Scheme
Let $q$ be a $381$-bit prime, $r$ be a $255$-bit prime, $G_1, G_2, G_T$ be three groups of order $r$, and $e:G_1\times G_2\rightarrow  G_T$ be a bilinear mapping. 

The details of BLS signature scheme are as follows.

- **KeyGen:** ***Input**: nothing; **Output:*** $(\mathsf{sk}, \mathsf{pk})$. Details:
$\mathsf{sk}\leftarrow\mathbb Z_r$, $\mathsf{pk} = g_1^{\mathsf{sk}}$. Note that $\mathsf{pk}\in G_1$.

- **Sign:** ***Input***: $m, \mathsf{sk}$*; **Output:*** $\sigma$. Details: $h=\mathtt{hash}(m)$, $H=\mathtt{hash2curve}(h)$, $\sigma =H^{\mathsf{sk}}\in G_2$. Note that $H\in G_2, \sigma \in G_2$.

- **Verify:** ***Input:*** $(\sigma, m), \mathsf{pk}$*; **Output:*** $y$. Details: $h=\mathtt{hash}(m)$, $H=\mathtt{hash2curve}(h)$, $y = (e(g_1, \sigma) \overset{?}{=} e(\mathsf{pk},H))$. Note that $y=0$ or $y=1$ and $H\in G_2$.


For more information about $r, q$, see and run [bls12_381_params.py](bls12_381_params.py). 
```shell
# hex
r=0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001 
# decimal
r=52435875175126190479447740508185965837690552500527637822603658699938581184513

# hex
q=0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb154000045ffaaaaaaab0000 
# decimal
q=4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129025752288709566988288
```
