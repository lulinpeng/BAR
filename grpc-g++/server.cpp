#include <grpcpp/grpcpp.h>
#include <grpcpp/security/server_credentials.h>

#include <iostream>

#include "hello.grpc.pb.h"
#include "utils.h"
using namespace std;
using hello::Greeter;
using hello::HelloReply;
using hello::HelloRequest;

class GreeterServiceImpl : public Greeter::Service {
  grpc::Status SayHello(grpc::ServerContext *context, const HelloRequest *request, HelloReply *reply) override {
    cout << "client addr: " << context->peer() << endl;

    if (context->auth_context()) {
      cout << "IsPeerAuthenticated: " << context->auth_context()->IsPeerAuthenticated() << endl;
      cout << "GetPeerIdentity Size: " << context->auth_context()->GetPeerIdentity().size() << endl;
    } else {
      cout << "WARNING: NO AUTH CONTEXT" << endl;
    }

    cout << "<- " << request->name() << endl;
    string msg = "Hello " + request->name();
    reply->set_message(msg);
    cout << "-> " << msg << endl;
    return grpc::Status::OK;
  }
};

int main(int argc, char *argv[]) {
  Utils::Config config;
  config.parse_args(argc, argv);
  cout << "i am server, running on " << config.address << ":" << config.port << endl;
  config.Print();

  GreeterServiceImpl service;
  cout << "create inseucre channel (by default)" << endl;
  auto creds = grpc::InsecureServerCredentials();
  if (config.secure) {
    grpc::SslServerCredentialsOptions ssl_opts;
    cout << "set CA certificate: verify other's identity" << endl;
    ssl_opts.pem_root_certs = Utils::read_file("certs/ca.crt");// If no root certificate is specified, the system's root certificates will be used.
    ssl_opts.client_certificate_request = GRPC_SSL_REQUEST_AND_REQUIRE_CLIENT_CERTIFICATE_AND_VERIFY;
    cout << "set my certificate: prove my own identity" << endl;
    ssl_opts.pem_key_cert_pairs.push_back({Utils::read_file("certs/server.key"), Utils::read_file("certs/server.crt")});
    if (config.mutual_tls) {
      cout << "Mutual TLS" << endl;
      ssl_opts.client_certificate_request = GRPC_SSL_REQUEST_AND_REQUIRE_CLIENT_CERTIFICATE_AND_VERIFY;
    } else {
      cout << "One-Way TLS" << endl;
      ssl_opts.client_certificate_request = GRPC_SSL_DONT_REQUEST_CLIENT_CERTIFICATE;
    }
    cout << "create seucre channel" << endl;
    creds = grpc::SslServerCredentials(ssl_opts);
  }
  cout << endl;

  grpc::ServerBuilder builder;
  builder.AddListeningPort(config.address + ":" + config.port, creds);
  builder.RegisterService(&service);
  unique_ptr<grpc::Server> server(builder.BuildAndStart());
  server->Wait();

  return 0;
}
