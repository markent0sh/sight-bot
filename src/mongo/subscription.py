import logging
import os
import sys

import mongo.mongo_client as mongo_client

sys.path.append(
  os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../'))

import config

class SubscriptionDocument:
  def __init__(self,
    user_id : int,
    target_username : str,
    service : str,
    frequency : int,
    date : str,
    time : str,
    overdue : bool,
    active : bool
  ):
    self.user_id_ : int = user_id
    self.target_username_ : str = target_username
    self.service_ : str = service
    self.frequency_ : int = frequency
    self.date_ : str = date
    self.time_ : str = time
    self.overdue_ : bool = overdue
    self.active_ : bool = active

class SubscritionDB:
  def __init__(self) -> None:
    self.client_ = mongo_client.MongoClientWrapper(
      config.SUBSCRIPTIONS_DB_PATH,
      config.SUBSCRIPTIONS_COLLECTION_PATH)

  def create_subscription(self, document : SubscriptionDocument):
    subscription = None

    try:
      session = self.client_.open_session()
      subscription = self.client_.create({
        'user-id' : document.user_id_,
        'target-username' : document.target_username_,
        'service' : document.service_,
        'frequency' : document.frequency_,
        'date-time' : self._safe_merge_date_time(document.date_, document.time_),
        'overdue' : document.overdue_,
        'active' : document.active_}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'SubscritionDB :: Unable to create new subscription for user {document.user_id_}, error: {str(error)}')
      subscription = None

    return subscription

  def get_active_subscription(self, user_id : int, target : str, service : str):
    subscription = None

    try:
      session = self.client_.open_session()
      subscription = self.client_.read({
        'user-id' : user_id,
        'target-username' : target,
        'service' : service,
        'active' : True}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'SubscritionDB :: Unable to get subscription for user user {user_id}, error: {str(error)}')

    if(0 < len(subscription)):
      time, date = self._safe_split_date_time(subscription[0].get('date-time'))
      return SubscriptionDocument(
        user_id=subscription[0].get('user-id'),
        target_username=subscription[0].get('target-username'),
        service=subscription[0].get('service'),
        frequency=subscription[0].get('frequency'),
        date=date,
        time=time,
        overdue=subscription[0].get('overdue'),
        active=subscription[0].get('active'))

    return None

  def get_all_subscriptions(self, user_id : int):
    read = None

    try:
      session = self.client_.open_session()
      read = self.client_.read({'user-id' : user_id}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'SubscritionDB :: Unable to get subscription for user user {user_id}, error: {str(error)}')

    subscriptions = []

    if(0 < len(read)):
      for item in read:
        time, date = self._safe_split_date_time(item.get('date-time'))
        subscriptions.append(SubscriptionDocument(
          user_id=item.get('user-id'),
          target_username=item.get('target-username'),
          service=item.get('service'),
          frequency=item.get('frequency'),
          date=date,
          time=time,
          overdue=item.get('overdue'),
          active=item.get('active')))

    return subscriptions

  def update_subscription_datetime(self,
    user_id : int,
    target : str,
    service : str,
    update_date : str,
    update_time : str):
    try:
      session = self.client_.open_session()
      self.client_.update({
        'user-id' : user_id,
        'target-username' : target,
        'service' : service,
        'active' : True},
        {'date-time' : self._safe_merge_date_time(update_date, update_time)}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'SubscritionDB :: Unable to update user {user_id} subscription date-time to {self._safe_merge_date_time(update_date, update_time)}, error: {str(error)}')

  def update_subscription_overdue(self,
    user_id : int,
    target : str,
    service : str,
    update : bool):
    try:
      session = self.client_.open_session()
      self.client_.update({
        'user-id' : user_id,
        'target-username' : target,
        'service' : service,
        'active' : True},
        {'overdue' : update}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'SubscritionDB :: Unable to update user {user_id} subscription overdue to {update}, error: {str(error)}')

  def update_subscription_active(self,
    user_id : int,
    target : str,
    service : str,
    update : bool):
    try:
      session = self.client_.open_session()
      self.client_.update({
        'user-id' : user_id,
        'target-username' : target,
        'service' : service,
        'active' : not update},
        {'active' : update}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'SubscritionDB :: Unable to update user {user_id} subscription active to {update}, error: {str(error)}')

  def _safe_split_date_time(self, date_time : str):

    if date_time and isinstance(date_time, str):
      parts = date_time.split()

      if len(parts) >= 2:
        time_str = parts[1]
        date_str = parts[0]
        return time_str, date_str
      else:
        logging.error(f'SubscritionDB :: Unable to split date and time')
        return None, None

    else:
      logging.error(f'SubscritionDB :: Unable to split date and time')
      return None, None

  def _safe_merge_date_time(self, date : str, time : str):

    if (date and isinstance(date, str)) and (time and isinstance(time, str)):
      return date + ' ' + time
    else:
      logging.error(f'SubscritionDB :: Unable to merge date and time')
      return 'None'
