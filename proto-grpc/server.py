import grpc
from concurrent import futures
import time
import service_pb2
import service_pb2_grpc

class TestServiceServicer(service_pb2_grpc.TestServiceServicer):    
    def GetData(self, request, context):
        print(f'Get request: \n{request}')        
        return service_pb2.DataResponse(names=['bob', 'mike', 'lisa'], age=20) # response
    
    def StreamData(self, request, context):
        print(f'Get request: \n{request}')  
        chunks = [b"chunk0", b"chunk1", b"chunk2", b"chunk3"]
        for i, data in enumerate(chunks):
            if context.is_active(): # check if the client is alive
                print(f"send {i+1}/{len(chunks)} chunk for request id {request.id}")
                yield service_pb2.DataChunkResponse(chunk=data)  # response
                time.sleep(1)
            else:
                print(f"Client cancelled stream for {request.id}")
                break
        
        print(f"Completed streaming for request id {request.id}")

if __name__ == '__main__':
    # create grpc server with thread number
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # add service
    service_pb2_grpc.add_TestServiceServicer_to_server(TestServiceServicer(), server)
    
    # set ip and port
    port = 50051
    server.add_insecure_port(f'[::]:{port}')
    
    # start the server
    server.start()
    print(f"Server started on port {port}")
    time.sleep(1000)
    server.stop(0)
