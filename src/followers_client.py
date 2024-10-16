import grpc
from follower.v1 import follower_pb2_grpc
from follower.v1 import follower_pb2

import logging

# python3 -m grpc_tools.protoc -I/home/mark-ssd/code/mdb/src/sight-service/src/service/server/follower/proto/ --python_out=. --grpc_python_out=. /home/mark-ssd/code/mdb/src/sight-service/src/service/server/follower/proto/follower/v1/follower.proto

class FollowerClient:
  def __init__(self, address, port) -> None:
    self.channel = grpc.insecure_channel(f'{address}:{port}')
    self.stub = follower_pb2_grpc.FollowerServiceStub(self.channel)

  def subscribe(self, client_id, target_username, follower_track, following_track, frequency):
    logging.info(
      f'Subscribe request, client:{client_id}, username: {target_username}, follower: {follower_track}, following: {following_track}, frequency: {frequency}')
    request_target = follower_pb2.Target(
      username = target_username,
      followers = follower_track,
      following = following_track,
      frequency = frequency)
    request = follower_pb2.SubscribeRequest(
      client = client_id,
      target = request_target)

    response = self.stub.Subscribe(request)
    return response.error_code

  def unsubscribe(self, client_id, target_username):
    logging.info(f'Unsubscribe request, client_id: {client_id}, username: {target_username}')
    request = follower_pb2.UnsubscribeRequest(
      client = client_id,
      username = target_username)

    response = self.stub.Unsubscribe(request)
    return response.error_code

  def get_followers(self,
    client_id,
    target_username,
    from_time, from_date,
    to_time, to_date):
    logging.info(
      f'Get followers request, client_id: {client_id}, username: {target_username}, from: {from_time}-{from_date}, to: {to_time}-{to_date}')
    from_timestamp = follower_pb2.Timestamp(
      date = from_date,
      time = from_time
    )
    to_timestamp = follower_pb2.Timestamp(
      date = to_date,
      time = to_time
    )

    request = follower_pb2.GetFollowersRequest(**{
      'client': client_id,
      'username': target_username,
      'from': from_timestamp,
      'to': to_timestamp
    })

    response = self.stub.GetFollowers(request)
    return response # all, subscribed, unsubscribed

  def get_following(self,
    client_id,
    target_username,
    from_time, from_date,
    to_time, to_date):
    logging.info(
      f'Get following request, client_id: {client_id}, username: {target_username}, from: {from_time}-{from_date}, to: {to_time}-{to_date}')
    from_timestamp = follower_pb2.Timestamp(
      date = from_date,
      time = from_time
    )
    to_timestamp = follower_pb2.Timestamp(
      date = to_date,
      time = to_time
    )

    request = follower_pb2.GetFollowingRequest(**{
      'client': client_id,
      'username': target_username,
      'from': from_timestamp,
      'to': to_timestamp
    })

    response = self.stub.GetFollowing(request)
    return response # all, subscribed, unsubscribed

  def get_client_targets(self, client_id):
    request = follower_pb2.GetClientTargetsRequest(
      client = client_id)

    response = self.stub.GetClientTargets(request)
    return response.targets

if(__name__ == "__main__"):
  import time
  client = FollowerClient('127.0.0.1', 44444)

  client.subscribe(0, 'misha1488', True, False)
  time.sleep(1)
  client.subscribe(0, 'aloxach', True, True)
  time.sleep(1)
  client.subscribe(0, 'R1b3riA', True, True)
  time.sleep(1)
  client.subscribe(0, 'badega', False, True)
  time.sleep(1)
  client.subscribe(1, 'k137sd', False, False)
  time.sleep(1)

  followers = client.get_followers(1, 'k137sd', '20:00', '01.01.2000', '20:00', '01.01.2025')
  print('------------------------------------------------> FOLLOWERS:')
  for follower in followers.all:
    print(follower)

  following = client.get_following(1, 'k137sd', '20:00', '01.01.2000', '20:00', '01.01.2025')
  print('------------------------------------------------> FOLLOWING:')
  for follower in following.all:
    print(follower)

  targets_0 = client.get_client_targets(0)
  print('------------------------------------------------> TARGETS CLIENT #0 (B):')
  print(targets_0)

  targets_1 = client.get_client_targets(1)
  print('------------------------------------------------> TARGETS CLIENT #1 (B):')
  print(targets_1)

  client.unsubscribe(0, 'misha1488')
  time.sleep(1)
  client.unsubscribe(0, 'aloxach')
  time.sleep(1)
  client.unsubscribe(0, 'R1b3riA')
  time.sleep(1)
  client.unsubscribe(0, 'badega')
  time.sleep(1)
  client.unsubscribe(1, 'k137sd')
  time.sleep(1)

  targets_0 = client.get_client_targets(0)
  print('------------------------------------------------> TARGETS CLIENT #0 (A):')
  print(targets_0)

  targets_1 = client.get_client_targets(1)
  print('------------------------------------------------> TARGETS CLIENT #1 (A):')
  print(targets_1)
