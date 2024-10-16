import logging
import os
import sys

import mongo.mongo_client as mongo_client

sys.path.append(
  os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../'))

import config

class ReferralsDocument:
  def __init__(self) -> None:
    self.referrals_ : list = []

  def append(self,
    user_id : int,
    bonuses : int):
    self.referrals_.append({
      'id' : user_id,
      'bonuses' : bonuses
    })

class UserDocument:
  def __init__(self,
    user_id : int,
    chat_id : int,
    language : str = 'russian',
    stories_notify : bool = True,
    followers_notify : bool = True,
    balance : int = 0,
    welcome : bool = True,
    beneficiary : int = 0,
    referrals : ReferralsDocument = ReferralsDocument()) -> None:
    self.user_id_ = user_id
    self.chat_id_ = chat_id
    self.language_ = language
    self.stories_notify_ = stories_notify
    self.followers_notify_ = followers_notify
    self.balance_ = balance
    self.welcome_ = welcome
    self.beneficiary_ = beneficiary
    self.referrals_ = referrals

class UserDB:
  def __init__(self) -> None:
    self.client_ = mongo_client.MongoClientWrapper(
      config.USER_DB_PATH,
      config.USER_COLLECTION_PATH)

  def create_user(self, document : UserDocument):
    user = None

    try:
      user = self.get_user(document.user_id_)

      if None is user:
        session = self.client_.open_session()
        user = self.client_.create({
          'user-id' : document.user_id_,
          'chat-id' : document.chat_id_,
          'language' : document.language_,
          'stories-notify' : document.stories_notify_,
          'followers-notify' : document.followers_notify_,
          'balance' : document.balance_,
          'welcome' : document.welcome_,
          'beneficiary' : document.beneficiary_,
          'referrals' : document.referrals_.referrals_}, session)
        self.client_.close_session(session)
      else:
        logging.warning(f'UserDB :: user with ID {document.user_id_} already exists')

    except Exception as error:
      logging.error(f'UserDB :: Unable to create new user {document.user_id_}, error: {str(error)}')

    return user

  def get_user(self, user_id : int):
    user = None

    try:
      session = self.client_.open_session()
      user = self.client_.read({'user-id' : user_id}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'UserDB :: Unable to get user {user_id}, error: {str(error)}')

    if(None is not user and 0 < len(user)):
      refs_doc = ReferralsDocument()
      referrals = user[0].get('referrals')
      for ref in referrals:
        refs_doc.append(ref.get('id'), ref.get('bonuses'))

      return UserDocument(
        user_id=user[0].get('user-id'),
        chat_id=user[0].get('chat-id'),
        language=user[0].get('language'),
        stories_notify=user[0].get('stories-notify'),
        followers_notify=user[0].get('followers-notify'),
        balance=user[0].get('balance'),
        welcome=user[0].get('welcome'),
        beneficiary=user[0].get('beneficiary'),
        referrals=refs_doc)

    return None

  def get_all_users(self):
    users = None

    try:
      session = self.client_.open_session()
      users = self.client_.read({}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'UserDB :: Unable to get all users, error: {str(error)}')

    users_docs = []

    if(None is not users):
      for user in users:
        refs_doc = ReferralsDocument()
        referrals = user.get('referrals')
        for ref in referrals:
          refs_doc.append(ref.get('id'), ref.get('bonuses'))

        users_docs.append(UserDocument(
          user_id=user.get('user-id'),
          chat_id=user.get('chat-id'),
          language=user.get('language'),
          stories_notify=user.get('stories-notify'),
          followers_notify=user.get('followers-notify'),
          balance=user.get('balance'),
          welcome=user.get('welcome'),
          beneficiary=user.get('beneficiary'),
          referrals=refs_doc))

    return users_docs

  def update_beneficiary(self,
    user_id : int,
    update : int):
    try:
      session = self.client_.open_session()
      self.client_.update(
        {'user-id' : user_id},
        {'beneficiary' : update}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'UserDB :: Unable to update user {user_id} beneficiary to {update}, error: {str(error)}')

  def update_welcome(self,
    user_id : int,
    update : bool):
    try:
      session = self.client_.open_session()
      self.client_.update(
        {'user-id' : user_id},
        {'welcome' : update}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'UserDB :: Unable to update user {user_id} welcome to {update}, error: {str(error)}')

  def update_language(self,
    user_id : int,
    update : str):
    try:
      session = self.client_.open_session()
      self.client_.update(
        {'user-id' : user_id},
        {'language' : update}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'Unable to update user {user_id} language to {update}, error: {str(error)}')

  def update_user_balance(self,
    user_id : int,
    update : float):
    try:
      session = self.client_.open_session()
      self.client_.update(
        {'user-id' : user_id},
        {'balance' : update}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'Unable to update user {user_id} balance to {update}, error: {str(error)}')

  def update_stories_notify(self,
    user_id : int,
    update : bool):
    try:
      session = self.client_.open_session()
      self.client_.update(
        {'user-id' : user_id},
        {'stories-notify' : update}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'Unable to update user {user_id} stories notify to {update}, error: {str(error)}')

  def update_followers_notify(self,
    user_id : int,
    update : bool):
    try:
      session = self.client_.open_session()
      self.client_.update(
        {'user-id' : user_id},
        {'followers-notify' : update}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'Unable to update user {user_id} followers notify to {update}, error: {str(error)}')

  def update_referrals(self,
    user_id : int,
    update : list):
    try:
      session = self.client_.open_session()
      self.client_.update(
        {'user-id' : user_id},
        {'referrals' : update}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'Unable to update user {user_id} referrals to {update}, error: {str(error)}')
