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

g++ -std=c++14 -o server_compress server_compress.cpp utils.h hello.pb.cc hello.grpc.pb.cc $FLAG

g++ -std=c++14 -o client_compress client_compress.cpp utils.h hello.pb.cc hello.grpc.pb.cc $FLAG


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

## Communication Compression Version
Note that: the compression algorithm specified ***by the client controls request compression***, while the compression algorithm specified ***by the server controls response compression***, with **each operating independently**.


```shell
# both enable gPRC compression
./server_compress -h 0.0.0.0 -p 5000 -c # '-c' server compressses response
./client_compress -h localhost -p 5000 -c # '-c' client compresses request

# only client compresses request
./server_compress -h 0.0.0.0 -p 5000
./client_compress -h localhost -p 5000 -c 

# only server compresses response 
./server_compress -h 0.0.0.0 -p 5000 -c
./client_compress -h localhost -p 5000

# both do not enable gPRC compression
./server_compress -h 0.0.0.0 -p 5000
./client_compress -h localhost -p 5000
```

To monitor the network traffic, you may use the command ```nload lo -a 4 -m```.

```shell
apt update && apt install -y nload iproute2
ip a # list all network card
# nload [network card name] -a [time window] -m
nload lo -a 4 -m

# Device lo [127.0.0.1] (1/1):
# ===================================================================
# Incoming:                                     Outgoing:
# Curr: 0.00 Bit/s                              Curr: 0.00 Bit/s
# Avg: 0.00 Bit/s                               Avg: 0.00 Bit/s
# Min: 0.00 Bit/s                               Min: 0.00 Bit/s
# Max: 0.00 Bit/s                               Max: 0.00 Bit/s
# Ttl: 326.99 MByte                             Ttl: 326.99 MByte
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


# ABOUT TLS
| Version | Release Year | RTT | Current Status | TLS Version (Hex) |
|:-------:|:------------:|:---:|:--------------:|:--------------:|
| SSL 2.0 |     1995     |  2  |   ~~In Use~~   | - |
| SSL 3.0 |     1996     |  2  |   ~~In Use~~   | 0x0300 |
| TLS 1.0 |     1999     |  2  |   ~~In Use~~   | 0x0301 |
| TLS 1.1 |     2006     |  2  |   ~~In Use~~   | 0x0302 |
| **TLS 1.2** |     2008     |  2  |     In Use     | 0x0303 |
| **TLS 1.3** |     2018     |  1  |     In Use     | 0x0304 |


# TLS
Every TLS message starts with a **5-byte** record layer header, where **Record Layer Header (5 bytes) = *Content Type (1 byte) + TLS Version (2 bytes) + Data Length (2 bytes)***

## TLS Content Type
| Value (Dec) | Value (Hex) | Content Type | Defining RFC | Status | Description |
|---------|-----|--------------|---------------|--------|-------------|
| 20 | 0x14 | change_cipher_spec | RFC 5246 | Standard | Notifies receiver to switch to newly negotiated encryption parameters |
| 21 | 0x15 | alert | RFC 5246 | Standard | Conveys warning or fatal error messages and closure notifications |
| 22 | 0x16 | handshake | RFC 5246 | Standard | Carries TLS handshake negotiation messages |
| 23 | 0x17 | application_data | RFC 5246 | Standard | Carries encrypted application layer data (HTTP, SMTP, etc.) |
| 24 | 0x18 | heartbeat | RFC 6520 | Extension | Heartbeat protocol for keep-alive and connection liveness checks |
| 25 | 0x19 | tls12_cid | RFC 9146 | Extension | Connection identifier for TLS 1.2, mainly used in DTLS |
| 64 | 0x40 | ACK | RFC 9001 | Extension | Acknowledgment frame for DTLS 1.3 (UDP only) |
| 0-19, 26-63, 65-255 | 0x00-0x13, 0x1A-0x3F,  0x41-0xFF| Unassigned | - | Reserved | Reserved values; receipt should generate unexpected_message alert |

### ChangeCipherSpec (Content Type=0x14)
```shell
# [Record Layer Header (5 bytes)] + [ChangeCipherSpec Layer (1 byte)]
Content Type (1 byte) + TLS Version (2 bytes) + Data Length (2 bytes) + Data (1 byte)

14 03 03 00 01 01 -> 0x14: change_cipher_spec, 0x0303: TLS 1.2, 0x0001: 1 byte length, 0x01: fixed value
```

### Alert (Content Type=0x15)
```shell
# [Record Layer Header (5 bytes)] + [Aleart Layer (2 bytes)]
Content Type (1 byte) + TLS Version (2 bytes) + Data Length (2 bytes) + Alert Level (1 byte) + Alert Description (1 byte)

15 03 03 00 02 01 00 -> 0x15: alert, 0x0303: TLS 1.2, 0x0002: 1 byte length, 0x01: warning, 0x00: close_notify
```
### ApplicationData (Content Type=0x17)
```shell
# [Record Layer Header (5 bytes)] + [Application Data Layer]
Content Type (1 byte) + TLS Version (2 bytes) + Data Length (2 bytes) + Encrypted Data (x bytes)

17 03 03 00 30 -> 0x17: application_data, 0x0303: TLS 1.2, 0x0030: 48 bytes
```

### Heartbeat (Content Type=0x18)
```shell
# [Record Layer Header (5 bytes)] + [Heartbeat Layer]
Content Type (1 byte) + TLS Version (2 bytes) + Data Length (2 bytes) + Heartbeat Data (x bytes)

18 03 03 00 03 01 -> 0x18: Heartbeat, 0x0303: TLS 1.2, 0x0003: 3 bytes, 0x01: heartbeat request
```
### Handshake (Content Type=0x16)
```shell
# [Record Layer Header (5 bytes)] + [Handshake Layer]
Content Type (1 byte) + TLS Version (2 bytes) + Data Length (2 bytes) + Message Type (1 byte) + Msg Length (3 bytes) + Msg (x bytes)

16 03 01 02 00 01 00 01 FC -> 0x16: Handshake, 0x0301: TLS 1.0, 0x0200: 512 bytes, 0x01: Client Hello, 0x0001FC: 508 bytes
```

| Value (Dec) | Value (Hex) | Message Type | TLS 1.2 Support | TLS 1.3 Support | Description |
|:-----------:|:-----------:|:-------------|:---------------:|:---------------:|:------------|
| 0 | 0x00 | hello_request | ✓ | ✗ | Server request to restart handshake (deprecated) |
| 1 | 0x01 | client_hello | ✓ | ✓ | Client initiates handshake |
| 2 | 0x02 | server_hello | ✓ | ✓ | Server responds to client_hello |
| 3 | 0x03 | hello_verify_request | ✓ (DTLS only) | ✗ | Hello verification request (DTLS) |
| 4 | 0x04 | new_session_ticket | ✓ | ✓ | Server sends new session ticket |
| 5 | 0x05 | end_of_early_data | ✗ | ✓ | End of 0-RTT early data |
| 6 | 0x06 | hello_retry_request | ✗ | ✓ | Hello retry request (TLS 1.3) |
| 7 | 0x07 | encrypted_extensions | ✗ | ✓ | Encrypted extensions message |
| 8 | 0x08 | certificate | ✓ | ✓ | Certificate chain transmission |
| 9 | 0x09 | server_key_exchange | ✓ | ✗ | Server key exchange parameters |
| 10 | 0x0A | certificate_request | ✓ | ✓ | Request for client certificate (mTLS) |
| 11 | 0x0B | server_hello_done | ✓ | ✗ | Server hello completion |
| 12 | 0x0C | certificate_verify | ✓ | ✓ | Proof of certificate ownership |
| 13 | 0x0D | client_key_exchange | ✓ | ✗ | Client key exchange parameters |
| 14 | 0x0E | finished | ✓ | ✓ | Handshake verification completion |
| 15 | 0x0F | certificate_url | Optional | Optional | Certificate URL extension (RFC 6066) |
| 16 | 0x10 | certificate_status | Optional | Optional | Certificate status (e.g., OCSP stapling) |
| 17 | 0x11 | supplemental_data | Optional | Optional | Supplemental data (RFC 4680) |
| 18 | 0x12 | key_update | ✗ | ✓ | Key update for rekeying |
| 19 | 0x13 | message_hash | ✗ | ✓ | Message hash (TLS 1.3 post-handshake auth) |
| 20 | 0x14 | compressed_certificate | ✗ | ✓ | Compressed certificate (RFC 8879) |
| 21-63 | 0x15-0x3F | reserved | - | - | Reserved for previously assigned values |
| 64-223 | 0x40-0xDF | private use | - | - | Reserved for private use |
| 224-255 | 0xE0-0xFF | experimental | - | - | Reserved for experimental purposes |

***DTLS** (Datagram Transport Layer Security) is designed for UDP-like protocol.*


#### Handshake Protocol
```shell
TLS 1.2 (2008)                                  TLS 1.3 (2018)
│                                               │
├─ → client_hello                               ├─ → client_hello
├─ ← server_hello                               ├─ ← server_hello
├─ ← certificate                                ├─ ← encrypted_extensions
├─ ← server_key_exchange (include a signature)  ├─ ← certificate
├─ ← certificate_request (only mTLS)            ├─ ← certificate_verify
├─ ← server_hello_done                          ├─ ← finished
├─ → certificate (only mTLS)                    ├─ → certificate
├─ → client_key_exchange                        ├─ → certificate_verify
├─ → certificate_verify (only mTLS)             ├─ → finished
├─ → finished                                   └─ → data
├─ ← finished       
└─ ← data        
```
