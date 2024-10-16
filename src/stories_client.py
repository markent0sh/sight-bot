import grpc
from story.v1 import story_pb2_grpc
from story.v1 import story_pb2

import logging

# python3 -m grpc_tools.protoc -I/home/mark-ssd/code/mdb/src/sight-service/src/service/server/story/proto/ --python_out=. --grpc_python_out=. /home/mark-ssd/code/mdb/src/sight-service/src/service/server/story/proto/story/v1/story.proto

class StoryClient:
  def __init__(self, address, port) -> None:
    self.channel = grpc.insecure_channel(f'{address}:{port}')
    self.stub = story_pb2_grpc.StoryServiceStub(self.channel)

  def subscribe(self, client_id, target_username, frequency):
    logging.info(f'Subscribe request, client_id: {client_id}, username: {target_username}, frequency: {frequency}')
    request_target = story_pb2.Target(
      username = target_username,
      frequency = frequency)
    request = story_pb2.SubscribeRequest(
      client = client_id,
      target = request_target)

    response = self.stub.Subscribe(request)
    return response.error_code

  def unsubscribe(self, client_id, target_username):
    logging.info(f'Unsubscribe request, client_id: {client_id}, username: {target_username}')
    request = story_pb2.UnsubscribeRequest(
      client=client_id,
      username=target_username)

    response = self.stub.Unsubscribe(request)
    return response.error_code

  def get_available_stories(self, client_id, target_username):
    logging.info(f'Get Stories request, client_id: {client_id}, username: {target_username}')
    request = story_pb2.GetAvailableStoriesRequest(
      client=client_id,
      username=target_username)

    response = self.stub.GetAvailableStories(request)
    return response.stories

  def get_client_targets(self, client_id):
    logging.info(f'Get Targets request, client_id: {client_id}')
    request = story_pb2.GetClientTargetsRequest(
      client=client_id)

    response = self.stub.GetClientTargets(request)
    return response.targets

if __name__ == "__main__":
  import time

  client = StoryClient('127.0.0.1', '33333')
  print('targets before: ', client.get_client_targets(12))

  print('sub 12', client.subscribe(12, 'miwa1488'))
  time.sleep(1)
  print('sub 12', client.subscribe(12, 'goganich'))
  time.sleep(1)
  print('sub 12', client.subscribe(12, 'k137sd'))
  time.sleep(1)
  print('sub 12', client.subscribe(12, 'OboRoNA'))
  time.sleep(1)

  print('unsub 12', client.unsubscribe(12, 'goganich'))
  time.sleep(1)

  print('targets after: ', client.get_client_targets(12))
  time.sleep(1)

  print('unsub 12', client.unsubscribe(12, 'miwa1488'))
  time.sleep(1)
  print('unsub 12', client.unsubscribe(12, 'k137sd'))
  time.sleep(1)
  print('unsub 12', client.unsubscribe(12, 'OboRoNA'))
  time.sleep(1)

  print('targets final: ', client.get_client_targets(12))
  time.sleep(1)
