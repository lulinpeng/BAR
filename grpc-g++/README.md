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
**CA Certificate: verify other's identity.** *It establishes trust by validating that remote parties' certificates are signed by trusted authorities. Moreover, The CA cert contains the public key needed to verify signatures on other parties' certificates in the PKI chain.*

>**The core validation logic for CA certificate:**
>1. I hold a public key of a CA that I trust.
>2. I verify the signature of the certificate from the counterpart to ensure the certificate is really issued by the CA.
>3. I challeng the counterpart to prove ownership of private key which is corresponds to the public key inside the certificate.

**My certificate: prove my own identity.** *It contains my public key and identity information, signed by a CA to authenticate me to others. Moreover, it is paired with its private key, creates digital signatures that demonstrate I control this identity*
