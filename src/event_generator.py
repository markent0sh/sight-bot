from enum import Enum
import logging
import threading
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from mongo.subscription import SubscritionDB, SubscriptionDocument
import config
import stories_client
import followers_client

def _get_current_utc_date_time():
  """
  Returns the current UTC date and time formatted as 'HH:MM' and 'DD.MM.YY'.

  Returns:
    tuple: Contains two strings (date, time)
  """
  current_utc_datetime = datetime.utcnow()
  date_str = current_utc_datetime.strftime("%d.%m.%Y")
  time_str = current_utc_datetime.strftime("%H:%M")
  return date_str, time_str

def _adjust_datetime(date_str: str, time_str: str):
  datetime_format = "%d.%m.%Y %H:%M"
  current_datetime = datetime.strptime(f"{date_str} {time_str}", datetime_format)
  modified_datetime = current_datetime - timedelta(hours=1)
  return modified_datetime.strftime("%d.%m.%Y"), modified_datetime.strftime("%H:%M")

def _has_week_passed(date, time):
  input_datetime = datetime.strptime(date + ' ' + time, "%d.%m.%Y %H:%M")
  week_ago = datetime.now() - relativedelta(weeks=1)
  return input_datetime < week_ago

def _merge_followers_timestamp(timestamp) -> str:
  return timestamp.time + timestamp.date

class EventPayload:
  def __init__(self) -> None:
    self.target_username : str = ''
    self.subscription : SubscriptionDocument = SubscriptionDocument(
      0, '', '', 0, '', '', True, True)
    self.date : str = ''
    self.time : str = ''

class EventType(Enum):
  eNewStories = 0,
  eNewFollowers = 1,
  eNewFollowing = 2,
  eSubscriptionOverdue = 3

class EventGenerator(object):
  _instance = None

  def __new__(cls):

    if not cls._instance:
      cls._instance = super(EventGenerator, cls).__new__(cls)

    return cls._instance

  def __init__(self) -> None:

    if 'callbacks_' not in self.__dict__:
      self.callbacks_ = {}
      self.usernames = []
      self.username_mutex_ = threading.Lock()
      self.running_ = False
      self.thread_ = threading.Thread(target = self._run_polling)
      self.callback_mutex_ = threading.Lock()
      self.stories_client_ = stories_client.StoryClient(
        config.STORY_SERVER_ADDRESS,
        config.STORY_SERVER_PORT)
      self.follower_client_ = followers_client.FollowerClient(
        config.FOLLOWER_SERVER_ADDRESS,
        config.FOLLOWER_SERVER_PORT)
      self.subscriptions_db_client_ = SubscritionDB()
      self.last_story_id = {}
      self.last_follower_sub_id = {}
      self.last_follower_un_id = {}
      self.last_following_sub_id = {}
      self.last_following_un_id = {}
      self.event_loop_ = None
      self.thread_.start()

  def __del__(self):
    self.running_ = False
    self.thread_.join()

  def subscribe(self, client_id, username, callback):
    with self.callback_mutex_:
      self.callbacks_[client_id] = callback

    with self.username_mutex_:

      if username not in self.usernames:
        self.usernames.append(username)
        logging.warning(f'>>> username: {username}')

  def set_event_loop(self, event_loop):
    if None is self.event_loop_:
      self.event_loop_ = event_loop

  def _run_polling(self):
    if(True == self.running_):
      logging.warning('>>> Already running')
      return

    self.running_ = True

    while(True == self.running_):

      if None is self.event_loop_:
        logging.warning('>>> Event loop is not set yet')
        time.sleep(config.POLLING_DELAY)
        continue

      try:
        usernames = []
        with self.username_mutex_:
          usernames = self.usernames

        callbacks = {}
        with self.callback_mutex_:
          callbacks = self.callbacks_

        for username in usernames:
          try:
            event = None
            event_payload = EventPayload()
            event_payload.target_username = username

            client_id = -1
            to_date, to_time = _get_current_utc_date_time()
            from_date, from_time = _adjust_datetime(to_date, to_time)

            stories = self.stories_client_.get_available_stories(client_id, username)

            if(len(stories) > 0 and stories[len(stories) - 1].uri != self.last_story_id.get(username)):
              event = EventType.eNewStories
              self.last_story_id[username] = stories[len(stories) - 1].uri

              for id in callbacks:
                self.event_loop_.create_task(callbacks[id](event, event_payload))

            followers = self.follower_client_.get_followers(
              client_id, username,
              from_time, from_date,
              to_time, to_date)
            subscribed = followers.subscribed
            unsubscribed = followers.unsubscribed

            if(len(subscribed) > 0 and
               _merge_followers_timestamp(subscribed[len(subscribed) - 1].timestamp) != self.last_follower_sub_id.get(username)):
              event = EventType.eNewFollowers
              self.last_follower_sub_id[username] = _merge_followers_timestamp(subscribed[len(subscribed) - 1].timestamp)
              subscribed = None

              for id in callbacks:
                self.event_loop_.create_task(callbacks[id](event, event_payload))

            if(None != subscribed): # To not send two notifications on one poll
              if(len(unsubscribed) > 0 and
                 _merge_followers_timestamp(unsubscribed[len(unsubscribed) - 1].timestamp) != self.last_follower_un_id.get(username)):
                event = EventType.eNewFollowers
                self.last_follower_un_id[username] = _merge_followers_timestamp(unsubscribed[len(unsubscribed) - 1].timestamp)

                for id in callbacks:
                  self.event_loop_.create_task(callbacks[id](event, event_payload))

            following = self.follower_client_.get_following(
              client_id, username,
              from_time, from_date,
              to_time, to_date)
            subscribed = following.subscribed
            unsubscribed = following.unsubscribed

            if(len(subscribed) > 0 and
               _merge_followers_timestamp(subscribed[len(subscribed) - 1].timestamp) != self.last_following_sub_id.get(username)):
              event = EventType.eNewFollowing
              self.last_following_sub_id[username] = _merge_followers_timestamp(subscribed[len(subscribed) - 1].timestamp)
              subscribed = None

              for id in callbacks:
                self.event_loop_.create_task(callbacks[id](event, event_payload))

            if(None != subscribed): # To not send two notifications on one poll
              if(len(unsubscribed) > 0 and
                 _merge_followers_timestamp(unsubscribed[len(unsubscribed) - 1].timestamp) != self.last_following_un_id.get(username)):
                event = EventType.eNewFollowing
                self.last_following_un_id[username] = _merge_followers_timestamp(unsubscribed[len(unsubscribed) - 1].timestamp)

                for id in callbacks:
                  self.event_loop_.create_task(callbacks[id](event, event_payload))
          except Exception as error:
            logging.error(f'>>> Exception during service event polling for username: {username}, error: {str(error)}')
            continue

        for uid in callbacks:
          try:
            subscriptions = self.subscriptions_db_client_.get_all_subscriptions(uid)

            for subscription in subscriptions:

              if True is _has_week_passed(subscription.date_, subscription.time_) and True is subscription.active_:
                date_str, time_str = _get_current_utc_date_time()
                event = EventType.eSubscriptionOverdue
                event_payload = EventPayload()
                event_payload.subscription = subscription
                event_payload.date = date_str
                event_payload.time = time_str
                self.event_loop_.create_task(callbacks[uid](event, event_payload))
          except Exception as error:
            logging.error(f'>>> Exception during subscription event polling for UID: {uid}, error: {str(error)}')
            continue

      except Exception as error:
        logging.error(f'>>> Exception during event polling, error: {str(error)}')

      time.sleep(config.POLLING_DELAY)

    logging.info(f'>>> exiting polling thread, status: {self.running_}')
