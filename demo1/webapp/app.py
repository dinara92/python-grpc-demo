from flask import Flask, Response

from google.protobuf.json_format import MessageToJson
from client_wrapper import ServiceClient

import sys
sys.path.insert(0,'/home/dinara/work/grpc-users/python-grpc-demo/demo1/grpc-services/protos/gen-py')
import users_pb2_grpc as users_service
import users_types_pb2 as users_messages

app = Flask(__name__)
app.config['users'] = ServiceClient(users_service, 'UsersStub', 'localhost', 50051)

@app.route('/users/')
def users_get():
    request = users_messages.GetUsersRequest(
        user=[users_messages.User(username="alexa", user_id=1),
              users_messages.User(username="christie", user_id=1)]
    )
    def get_user():
        response = app.config['users'].GetUsers(request)
        for resp in response:
            yield MessageToJson(resp)
    return Response(get_user(), content_type='application/json')

if __name__ == '__main__':
    app.run()
