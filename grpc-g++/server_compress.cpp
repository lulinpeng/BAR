#include <grpcpp/grpcpp.h>
#include <grpcpp/security/server_credentials.h>

#include <iostream>

#include "hello.grpc.pb.h"
#include "utils.h"
using namespace std;
using hello::Greeter;
using hello::HelloReply;
using hello::HelloRequest;

bool enable_response_compression = false;

class GreeterServiceImpl : public Greeter::Service {
  grpc::Status SayHello(grpc::ServerContext *context, const HelloRequest *request, HelloReply *reply) override {
    cout << "client addr: " << context->peer() << endl;

    if (enable_response_compression) {
      context->set_compression_algorithm(GRPC_COMPRESS_GZIP);
      context->set_compression_level(GRPC_COMPRESS_LEVEL_MED);
      cout << "server enables GRPC compression only for response" << endl;
    }

    cout << "<- " << request->name().size() << " bytes" << endl;
    string msg = "hello" + request->name();
    reply->set_message(msg);
    cout << "-> " << msg.size() << " bytes" << endl;
    return grpc::Status::OK;
  }
};

int main(int argc, char *argv[]) {
  Utils::Config config;
  config.parse_args(argc, argv);
  cout << "i am server, running on " << config.address << ":" << config.port << endl;
  config.Print();

  if (config.enable_compression) enable_response_compression = true;

  GreeterServiceImpl service;
  auto creds = grpc::InsecureServerCredentials();
  grpc::ServerBuilder builder;
  builder.AddListeningPort(config.address + ":" + config.port, creds);
  builder.RegisterService(&service);
  unique_ptr<grpc::Server> server(builder.BuildAndStart());
  server->Wait();

  return 0;
}
