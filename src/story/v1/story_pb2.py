# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: story/v1/story.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14story/v1/story.proto\x12\x08story.v1\"F\n\x06Target\x12\x10\n\x08username\x18\x01 \x01(\t\x12*\n\tfrequency\x18\x02 \x01(\x0e\x32\x17.story.v1.PollFrequency\"D\n\x10SubscribeRequest\x12\x0e\n\x06\x63lient\x18\x01 \x01(\x03\x12 \n\x06target\x18\x02 \x01(\x0b\x32\x10.story.v1.Target\"\'\n\x11SubscribeResponse\x12\x12\n\nerror_code\x18\x01 \x01(\x05\"6\n\x12UnsubscribeRequest\x12\x0e\n\x06\x63lient\x18\x01 \x01(\x03\x12\x10\n\x08username\x18\x02 \x01(\t\")\n\x13UnsubscribeResponse\x12\x12\n\nerror_code\x18\x01 \x01(\x05\"\'\n\tTimestamp\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x0c\n\x04time\x18\x02 \x01(\t\"<\n\x05Story\x12&\n\ttimestamp\x18\x01 \x01(\x0b\x32\x13.story.v1.Timestamp\x12\x0b\n\x03uri\x18\x02 \x01(\t\">\n\x1aGetAvailableStoriesRequest\x12\x0e\n\x06\x63lient\x18\x01 \x01(\x03\x12\x10\n\x08username\x18\x02 \x01(\t\"S\n\x1bGetAvailableStoriesResponse\x12 \n\x07stories\x18\x01 \x03(\x0b\x32\x0f.story.v1.Story\x12\x12\n\nerror_code\x18\x02 \x01(\x05\")\n\x17GetClientTargetsRequest\x12\x0e\n\x06\x63lient\x18\x01 \x01(\x03\"Q\n\x18GetClientTargetsResponse\x12!\n\x07targets\x18\x01 \x03(\x0b\x32\x10.story.v1.Target\x12\x12\n\nerror_code\x18\x02 \x01(\x05*K\n\rPollFrequency\x12\x08\n\x04RARE\x10\x00\x12\n\n\x06MEDIUM\x10\x01\x12\x08\n\x04\x46\x41ST\x10\x02\x12\r\n\tVERY_FAST\x10\x03\x12\x0b\n\x07QUANTUM\x10\x04\x32\xdf\x02\n\x0cStoryService\x12\x44\n\tSubscribe\x12\x1a.story.v1.SubscribeRequest\x1a\x1b.story.v1.SubscribeResponse\x12J\n\x0bUnsubscribe\x12\x1c.story.v1.UnsubscribeRequest\x1a\x1d.story.v1.UnsubscribeResponse\x12\x62\n\x13GetAvailableStories\x12$.story.v1.GetAvailableStoriesRequest\x1a%.story.v1.GetAvailableStoriesResponse\x12Y\n\x10GetClientTargets\x12!.story.v1.GetClientTargetsRequest\x1a\".story.v1.GetClientTargetsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'story.v1.story_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_POLLFREQUENCY']._serialized_start=694
  _globals['_POLLFREQUENCY']._serialized_end=769
  _globals['_TARGET']._serialized_start=34
  _globals['_TARGET']._serialized_end=104
  _globals['_SUBSCRIBEREQUEST']._serialized_start=106
  _globals['_SUBSCRIBEREQUEST']._serialized_end=174
  _globals['_SUBSCRIBERESPONSE']._serialized_start=176
  _globals['_SUBSCRIBERESPONSE']._serialized_end=215
  _globals['_UNSUBSCRIBEREQUEST']._serialized_start=217
  _globals['_UNSUBSCRIBEREQUEST']._serialized_end=271
  _globals['_UNSUBSCRIBERESPONSE']._serialized_start=273
  _globals['_UNSUBSCRIBERESPONSE']._serialized_end=314
  _globals['_TIMESTAMP']._serialized_start=316
  _globals['_TIMESTAMP']._serialized_end=355
  _globals['_STORY']._serialized_start=357
  _globals['_STORY']._serialized_end=417
  _globals['_GETAVAILABLESTORIESREQUEST']._serialized_start=419
  _globals['_GETAVAILABLESTORIESREQUEST']._serialized_end=481
  _globals['_GETAVAILABLESTORIESRESPONSE']._serialized_start=483
  _globals['_GETAVAILABLESTORIESRESPONSE']._serialized_end=566
  _globals['_GETCLIENTTARGETSREQUEST']._serialized_start=568
  _globals['_GETCLIENTTARGETSREQUEST']._serialized_end=609
  _globals['_GETCLIENTTARGETSRESPONSE']._serialized_start=611
  _globals['_GETCLIENTTARGETSRESPONSE']._serialized_end=692
  _globals['_STORYSERVICE']._serialized_start=772
  _globals['_STORYSERVICE']._serialized_end=1123
# @@protoc_insertion_point(module_scope)
