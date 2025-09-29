import grpc
import service_pb2
import service_pb2_grpc

# save protobuf instance as binary file
def save_as_bin(target, filename:str):
    with open(filename, 'wb') as f:
            f.write(target.SerializeToString())
    return

if __name__ == '__main__':
    endpoint = 'localhost:50051'
    # +++++ test GetData rpc +++++
    with grpc.insecure_channel(endpoint) as channel:
        stub = service_pb2_grpc.TestServiceStub(channel) # create grpc service stub
        request = service_pb2.DataRequest(name="alice", age = 15) # create request
        save_as_bin(request, 'request.bin') # save as bin
        try:
            response = stub.GetData(request, timeout=10) # send request
            print(f"Get response: \n{response}")
            save_as_bin(response, 'response.bin') # save as bin
        except grpc.RpcError as e:
            print(f"grpc error:{e.code()} - {e.details()}")
            
    # +++++ test StreamData rpc +++++
    with grpc.insecure_channel(endpoint) as channel:
        stub = service_pb2_grpc.TestServiceStub(channel) # create grpc service stub
        request = service_pb2.StreamRequest(id="0x1234") # create request
        try:
            response_stream = stub.StreamData(request) # send request
            for chunk in response_stream:
                print(f"recv: {chunk}")
        except grpc.RpcError as e:
            print(f"stream grpc error: {e.code()} - {e.details()}")
