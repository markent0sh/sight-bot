import logging
import asyncio

import stories_client
import followers_client
import crypto_payments
import event_generator
import config

from mongo.subscription import SubscritionDB, SubscriptionDocument
from mongo.user import UserDB
from mongo.invoice import InvoiceDB, InvoiceDocument

from fsm import StateEvent, EventPayload
from language.language_controller import LanguageController
from language.language_state import LanguageState

class ControlMessage:
  def __init__(self) -> None:
    self.keyboard = None
    self.media = None
    self.follower_info_in = None
    self.follower_info_out = None
    self.follower_image = None
    self.follower_pdf = None
    self.text = "None"
    self.message_id = -1
    self.user_id = -1
    self.message_id_updater = None
    self.event_callback_updater = None

class BotWidget:
  def __init__(self, control_update_callback, send_message_callback, message_id, client_id, chat_id) -> None:
    self.control_update_callback_ = control_update_callback
    self.send_message_callback_ = send_message_callback
    self.event_callback_ = None
    self.message_id_ = message_id
    self.client_id_ = client_id
    self.chat_id_ = chat_id
    self.keyboard_ = []
    self.media_ = []
    self.follower_info_in_ = []
    self.follower_info_out_ = []
    self.follower_image_ = None
    self.follower_pdf_ = None
    self.text_ = "None"
    self.stories_client = stories_client.StoryClient(
      config.STORY_SERVER_ADDRESS,
      config.STORY_SERVER_PORT)
    self.follower_client_ = followers_client.FollowerClient(
      config.FOLLOWER_SERVER_ADDRESS,
      config.FOLLOWER_SERVER_PORT)
    self.crypto_client_ = crypto_payments.CryptoClient(
      config.CRYPTO_API_TOKEN)
    self.user_db_client_ = UserDB()
    self.invoice_db_client_ = InvoiceDB()
    self.subscriptions_db_client_ = SubscritionDB()

    self.cached_story_target_list_ = []
    self.cached_followers_target_list_ = []

    targets = self.get_client_targets_story()
    for target in targets:
      event_generator.EventGenerator().subscribe(self.client_id_, target.username, self._notify_callback)

    targets = self.get_client_targets_follower()
    for target in targets:
      event_generator.EventGenerator().subscribe(self.client_id_, target.username, self._notify_callback)

  def set_message_id(self, message_id):
    self.message_id_ = message_id

  def set_event_callback(self, event_callback):
    self.event_callback_ = event_callback

  def fire_event(self, event : StateEvent, payload : EventPayload = EventPayload()):
    self.event_callback_(event, payload)

  def get_client_id(self):
    return self.client_id_

  def get_client_lang(self):
    return LanguageState().get_language(self.client_id_)

  def add_row(self, button_row):
    self.keyboard_.append(button_row)

  def clear_keyboard(self):
    self.keyboard_.clear()

  def set_text(self, text):
    self.text_ = text

  def add_media(self, media):
    self.media_.append(media)

  def clear_media(self):
    self.media_.clear()

  def add_follower_info_in(self, follower):
    self.follower_info_in_.append(follower)

  def clear_follower_info_in(self):
    self.follower_info_in_.clear()

  def add_follower_image(self, image):
    self.follower_image_ = image

  def add_follower_pdf(self, pdf):
    self.follower_pdf_ = pdf

  def clear_follower_pdf(self):
    self.follower_pdf_ = None

  def clear_follower_image(self):
    self.follower_image_ = None

  def add_follower_info_out(self, follower):
    self.follower_info_out_.append(follower)

  def clear_follower_info_out(self):
    self.follower_info_out_.clear()

  def trigger_update(self):
    try:
      message = ControlMessage()
      message.keyboard = self.keyboard_
      message.text = self.text_
      message.message_id = self.message_id_
      message.media = self.media_
      message.follower_info_in = self.follower_info_in_
      message.follower_info_out = self.follower_info_out_
      message.follower_image = self.follower_image_
      message.follower_pdf = self.follower_pdf_
      message.user_id = self.client_id_
      message.event_callback_updater = self.set_event_callback
      message.message_id_updater = self.set_message_id

      asyncio.create_task(self.control_update_callback_(message))
    except Exception as error:
      logging.error(f'BotWidget :: trigger update failed, error: {error.__str__()}')

  def get_cached_story_targets(self):
    return self.cached_story_target_list_

  def get_client_targets_story(self):
    self.cached_story_target_list_ = self.stories_client.get_client_targets(self.client_id_)
    return self.cached_story_target_list_

  def get_available_stories_story(self, target_username):
    return self.stories_client.get_available_stories(self.client_id_, target_username)

  def unsubscribe_story(self, target_username):
    return self.stories_client.unsubscribe(self.client_id_, target_username)

  def subscribe_story(self, target_username, frequency):
    event_generator.EventGenerator().subscribe(self.client_id_, target_username, self._notify_callback)
    return self.stories_client.subscribe(self.client_id_, target_username, frequency)

  def get_cached_followers_targets(self):
    return self.cached_followers_target_list_

  def get_client_targets_follower(self):
    self.cached_followers_target_list_ = self.follower_client_.get_client_targets(self.client_id_)
    return self.cached_followers_target_list_

  def get_followers_follower(self,
    target_username,
    from_time, from_date,
    to_time, to_date):
    return self.follower_client_.get_followers(
      self.client_id_,
      target_username,
      from_time, from_date,
      to_time, to_date)

  def get_following_follower(self,
    target_username,
    from_time, from_date,
    to_time, to_date):
    return self.follower_client_.get_following(
      self.client_id_,
      target_username,
      from_time, from_date,
      to_time, to_date)

  def unsubscribe_follower(self, target_username):
    return self.follower_client_.unsubscribe(self.client_id_, target_username)

  def subscribe_follower(self,
    target_username,
    follower_track,
    following_track,
    frequency):
    event_generator.EventGenerator().subscribe(self.client_id_, target_username, self._notify_callback)
    return self.follower_client_.subscribe(
      self.client_id_,
      target_username,
      follower_track,
      following_track,
      frequency)

  def create_crypto_invoice(self, amount : float):
    return self.crypto_client_.create_invoice(amount)

  def delete_crypto_invoice(self, invoice_id):
    return self.crypto_client_.delete_invoice(invoice_id)

  def write_crypto_invoice(self, invoice_id):
    return self.invoice_db_client_.create_invoice(InvoiceDocument(self.client_id_, invoice_id))

  def create_subscription(self, target, date, time, service, frequency = 0):
    return self.subscriptions_db_client_.create_subscription(
      SubscriptionDocument(
        self.client_id_,
        target,
        service,
        frequency,
        date,
        time,
        False,
        True))

  def get_active_subscription(self, target, service):
    return self.subscriptions_db_client_.get_active_subscription(
      self.client_id_,
      target,
      service)

  def update_subscription_datetime(self, target, service, date, time):
    self.subscriptions_db_client_.update_subscription_datetime(
      self.client_id_,
      target,
      service,
      date,
      time)

  def update_subscription_overdue(self, target, service, update):
    self.subscriptions_db_client_.update_subscription_overdue(
      self.client_id_,
      target,
      service,
      update)

  def update_subscription_active(self, target, service, update):
    self.subscriptions_db_client_.update_subscription_active(
      self.client_id_,
      target,
      service,
      update)

  def get_user(self, user_id : int = None):

    if None is user_id:
      user_id = self.client_id_

    return self.user_db_client_.get_user(user_id)

  def update_beneficiary(self, update : int):
    self.user_db_client_.update_beneficiary(self.client_id_, update)

  def update_welcome(self, update : bool):
    self.user_db_client_.update_welcome(self.client_id_, update)

  def update_language(self, update : str):
    self.user_db_client_.update_language(self.client_id_, update)

  def update_user_balance(self, update : float):
    self.user_db_client_.update_user_balance(self.client_id_, update)

  def update_stories_notify(self, update : bool):
    self.user_db_client_.update_stories_notify(self.client_id_, update)

  def update_followers_notify(self, update : bool):
    self.user_db_client_.update_followers_notify(self.client_id_, update)

  def update_referrals(self, user_id : int, update : list):
    self.user_db_client_.update_referrals(user_id, update)

  async def _notify_callback(self, event : event_generator.EventType, payload : event_generator.EventPayload):
    user = self.get_user()

    if(None is user):
      logging.error(f'Unable to read user from DB')
    elif(event_generator.EventType.eNewStories is event):

      if(True is user.stories_notify_):
          targets = self.cached_story_target_list_
          for target in targets:

            if target.username == payload.target_username:
              try:
                await self.send_message_callback_(LanguageController().get_text(self.get_client_lang(), 'NOTIFY_DESC_1', target.username), self.chat_id_)
              except Exception as error:
                logging.error(f'Unable to send story notify for client: {self.client_id_}, target: {target.username}, error: {str(error)}')

              break

    elif(event_generator.EventType.eNewFollowers is event):

      if(True is user.followers_notify_):
        targets = self.cached_followers_target_list_
        for target in targets:

          if target.username == payload.target_username and True is target.followers:
            try:
              await self.send_message_callback_(LanguageController().get_text(self.get_client_lang(), 'NOTIFY_DESC_2', target.username), self.chat_id_)
            except Exception as error:
              logging.error(f'Unable to send followers notify for client: {self.client_id_}, target: {target.username}, error: {str(error)}')

            break

    elif(event_generator.EventType.eNewFollowing is event):

      if(True is user.followers_notify_):
        targets = self.cached_followers_target_list_
        for target in targets:

          if target.username == payload.target_username and True is target.following:
            try:
              await self.send_message_callback_(LanguageController().get_text(self.get_client_lang(), 'NOTIFY_DESC_2', target.username), self.chat_id_)
            except Exception as error:
              logging.error(f'Unable to send following notify for client: {self.client_id_}, target: {target.username}, error: {str(error)}')

            break

    elif(event_generator.EventType.eSubscriptionOverdue is event):
      renew_price = 0
      service = payload.subscription.service_
      target = payload.subscription.target_username_

      if(0):
        pass
      elif('story' == service):
        renew_price = config.STORY_TARGET_PRICES.get(payload.subscription.frequency_)
      elif('follower' == service):
        renew_price = config.FOLLOWER_TARGET_PRICES.get(payload.subscription.frequency_)
      else:
        logging.error(
          f'Unknown subscription service received for user {self.client_id_}, [service: {service}, target: {target}, payload: {payload}]')
        renew_price = None

      if None is not renew_price:

        if(renew_price <= user.balance_):
          self.update_user_balance(user.balance_ - renew_price)
          self.update_subscription_datetime(target, service, payload.date, payload.time)
          self.update_subscription_overdue(target, service, False)
          logging.info(
            f'Renewed subscription for user {self.client_id_}, [service: {service}, target: {target}, payload: {payload}]')
        else:
          try:
            self.update_subscription_overdue(target, service, True)
            await self.send_message_callback_(
              LanguageController().get_text(self.get_client_lang(), 'NOTIFY_DESC_3', payload.subscription.target_username_), self.chat_id_)
          except Exception as error:
            logging.error(f'Unable to send renew notify for client: {self.client_id_}, target: {target.username}, error: {str(error)}')
      else:
        logging.error(
          f'Unable to get price for renewal: [{payload.subscription.user_id_}, {payload.subscription.service_}, {payload.subscription.target_username_}]')

    else:
      logging.error(f'Unknown event ID: {event}')
