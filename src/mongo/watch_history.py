import logging
import os
import sys

import mongo.mongo_client as mongo_client

sys.path.append(
  os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../'))

import config

class WatchHistoryDocument:
  def __init__(self,
    user_id : int,
    target_username : str,
    last_watched_story : str,
    last_watched_follower : str,
    last_watched_following : str
  ):
    self.user_id_ = user_id
    self.target_username_ = target_username
    self.last_watched_story_ = last_watched_story
    self.last_watched_follower_ = last_watched_follower
    self.last_watched_following_ = last_watched_following

class WatchHistoryDB:
  def __init__(self) -> None:
    self.client_ = mongo_client.MongoClientWrapper(
      config.INVOICE_DB_PATH,
      config.INVOICE_COLLECTION_PATH)

  def create_invoice(self, document : WatchHistoryDocument):
    invoice = None

    try:
      session = self.client_.open_session()
      invoice = self.client_.create({
        'user-id' : document.user_id_,
        'invoice-id' : document.invoice_id_,
        'paid' : document.paid_}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'WatchHistoryDB :: Unable to create new invoice {document.invoice_id_} for user {document.user_id_}, error: {str(error)}')

    return invoice

  def get_invoice(self, invoice_id : int):
    invoice = None

    try:
      session = self.client_.open_session()
      invoice = self.client_.read({'invoice-id' : invoice_id}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'WatchHistoryDB :: Unable to get invoice {invoice_id}, error: {str(error)}')

    if(None is not invoice and 0 < len(invoice)):
      return WatchHistoryDocument(
        user_id=invoice[0].get('user-id'),
        invoice_id=invoice[0].get('invoice-id'),
        paid=invoice[0].get('paid'))

    return None

  def update_status(self,
    invoice_id : int,
    update : bool):
    try:
      session = self.client_.open_session()
      self.client_.update({'invoice-id' : invoice_id}, {'paid' : update}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'WatchHistoryDB :: Unable to update invoice {invoice_id} paid status to {update}, error: {str(error)}')
