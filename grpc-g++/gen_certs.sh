#!/bin/bash
mkdir -p certs && cd certs

openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 365 -key ca.key -out ca.crt \
    -subj "/C=CN/ST=Beijing/L=Beijing/O=Test/CN=TestCA"

# for server
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr \
    -subj "/C=CN/ST=Beijing/L=Beijing/O=Test/CN=localhost"
openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt

# for client
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr \
    -subj "/C=CN/ST=Beijing/L=Beijing/O=Test/CN=client"
openssl x509 -req -days 365 -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt

# clear
rm *.csr *.srl
cd ..
