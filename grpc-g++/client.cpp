#include <grpcpp/grpcpp.h>
#include <grpcpp/security/credentials.h>

#include <iostream>
#include <thread>

#include "hello.grpc.pb.h"
#include "utils.h"
using namespace std;
using hello::Greeter;
using hello::HelloReply;
using hello::HelloRequest;

class GreeterClient {
 public:
  GreeterClient(shared_ptr<grpc::Channel> channel) : stub_(Greeter::NewStub(channel)) {}

  string SayHello(const string &name) {
    HelloRequest req;
    req.set_name(name);
    HelloReply rep;
    grpc::ClientContext context;
    context.set_deadline(chrono::system_clock::now() + chrono::seconds(3));
    grpc::Status status = stub_->SayHello(&context, req, &rep);
    if (status.ok())
      return rep.message();
    else
      return "RPC error: " + status.error_message();
  }

 private:
  unique_ptr<Greeter::Stub> stub_;
};

int main(int argc, char **argv) {
  cout << "i am client" << endl;
  Utils::Config config(false, false, "localhost", "50000");
  config.Print();
  config.parse_args(argc, argv);
  cout << "create inseucre channel (by default)" << endl;
  config.Print();
  auto creds = grpc::InsecureChannelCredentials();

  if (config.secure) {
    grpc::SslCredentialsOptions ssl_opts;
    cout << "set CA certificate: verify other's identity" << endl;
    ssl_opts.pem_root_certs = Utils::read_file("certs/ca.crt"); // If no root certificate is specified, the system's root certificates will be used.
    if (config.mutual_tls) {
      cout << "Mutual TLS" << endl;
      cout << "set my certificate: prove my own identity" << endl;
      ssl_opts.pem_private_key = Utils::read_file("certs/client.key");
      ssl_opts.pem_cert_chain = Utils::read_file("certs/client.crt");
    } else {
      cout << "One-Way TLS (only client verifies server)" << endl;
    }
    cout << "create secure channel with " << config.address + ":" + config.port << endl << endl;
    creds = grpc::SslCredentials(ssl_opts);
  }

  auto channel = grpc::CreateChannel(config.address + ":" + config.port, creds);
  GreeterClient client(channel);
  string name = "alice";
  cout << "-> " << name << endl;
  string response = client.SayHello(name);
  cout << "<- " << response << endl;
  return 0;
}
