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
    if (status.ok()) return rep.message();
    else
      return "RPC error: " + status.error_message();
  }

private:
  unique_ptr<Greeter::Stub> stub_;
};

int main(int argc, char **argv) {
  cout << "i am client" << endl;
  Utils::Config config;
  config.parse_args(argc, argv);
  config.Print();
  auto creds = grpc::InsecureChannelCredentials();

  shared_ptr<grpc::Channel> channel;
  if (config.enable_compression) {
    grpc::ChannelArguments args;
    args.SetCompressionAlgorithm(GRPC_COMPRESS_GZIP);
    args.SetInt(GRPC_COMPRESSION_CHANNEL_DEFAULT_LEVEL, GRPC_COMPRESS_LEVEL_MED);
    channel = grpc::CreateCustomChannel(config.address + ":" + config.port, creds, args);
    cout << "client enables gPRC compression only for request" << endl;
  } else channel = grpc::CreateChannel(config.address + ":" + config.port, creds);

  GreeterClient client(channel);
  string name = "jack";
  for (uint32_t i = 4; i < 1024 * 1024; i++) name += "jack";
  cout << "-> " << name.size() << " bytes" << endl;
  string response = client.SayHello(name);
  cout << "<- " << response.size() << " bytes" << endl;
  return 0;
}
