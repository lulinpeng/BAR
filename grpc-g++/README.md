# ENV
```shell
Ubuntu:22.04
# See Dockerfile for more details 
```
# BUILD
```shell
protoc -I proto --cpp_out=. proto/hello.proto
protoc -I proto --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` proto/hello.proto

FLAG="-I/usr/include -I/usr/local/include -L/usr/lib/x86_64-linux-gnu -L/usr/local/lib  -lgrpc++ -lgrpc -lgpr -lprotobuf -lssl -lcrypto -lpthread -ldl"

g++ -std=c++14 -o server server.cpp utils.h hello.pb.cc hello.grpc.pb.cc $FLAG

g++ -std=c++14 -o client client.cpp utils.h hello.pb.cc hello.grpc.pb.cc $FLAG


# Code Format
clang-format -style='{BasedOnStyle: google, ColumnLimit: 300}' -i *.cpp *.h
```

# RUN
## Insecure Version
```shell
./server -h 0.0.0.0 -p 5000
./client -h localhost -p 5000
```
## (One-Way TLS) Secure Version
```shell
sh gen_certs.sh # generate certs

./server -h 0.0.0.0 -p 5000 -s 
./client -h localhost -p 5000 -s 
```

## (Mutual TLS) Secure Version
```shell
sh gen_certs.sh # generate certs

./server -h 0.0.0.0 -p 5000 -s -d
./client -h localhost -p 5000 -s -d
```

# Sniffer

```shell
# apt install tshark tcpdump -y
tcpdump -i any -A -s 0 'tcp port 5000'

tcpdump -i any -s 0 -w xxx.pcap port 5000

tshark -r xxx.pcap
```


```shell
python3 sniffer.py

# http
curl --http1.1 -v localhost:5000
curl --http1.0 -v localhost:5000
curl --http2 -v localhost:5000

# https
curl --http1.0 -v https://localhost:5000
curl --http2 -v https://localhost:5000
```
# ABOUT CERTIFICATE
**Root Certificate:** it serves as a ***trust anchor*** and *requires no verification* ***since it is assumed to be trusted.*** Moreover, the root certificate is a **self-signed certificate** that represents the identity and public key of a Certificate Authority (CA), which can be loaded from either a ***specified path or the system default.***

>**The core validation logic for CA certificate:**
>1. I get a public key as a verifying key from the root certificate.
>2. I verify the signature of the certificate sent by the counterpart to ensure the certificate is really issued by the CA of the root certificate.
>3. I challenge the counterpart to prove ownership of private key which is corresponds to the public key inside the certificate.

**My certificate: prove my own identity.** *It contains my public key and identity information, signed by a CA to authenticate me to others. Moreover, it is paired with its private key, creates digital signatures that demonstrate I control this identity.*

## Why use certificates instead of just public keys?
Rather than just being a static key string, a certificate **binds a public key to a human-readable identity (like a name or domain)**, enforces a **validity period** with set expiration dates, and supports **revocation mechanisms** to actively invalidate a compromised key.
