import sys

import grpc

import users_pb2_grpc as users_service
import users_types_pb2 as users_messages


def run():
    channel = grpc.insecure_channel('localhost:50051')          #create a channel to our server
    try:
        grpc.channel_ready_future(channel).result(timeout=10)   #client waits for timeout
    except grpc.FutureTimeoutError:
        sys.exit('Error connecting to server')
    else:
        stub = users_service.UsersStub(channel)                 #else create a BertSqquadStub object and pass channel as arg
        metadata = [('ip', '127.0.0.1')]
        response = stub.CreateUser(
            users_messages.CreateUserRequest(username='tom'),
            metadata=metadata,
        )
        if response:
            print("User created:", response.user.username)
        request = users_messages.GetUsersRequest(               #request is of repeated type, so it is a list
            user=[users_messages.User(username="alexa", user_id=1), #repeated User in GetUsersRequest message
                  users_messages.User(username="christie", user_id=1)]
        )
        response = stub.GetUsers(request)                       #result of GetUsers is a stream, so iterate over it
        for resp in response:
            print(resp)


if __name__ == '__main__':
    run()
