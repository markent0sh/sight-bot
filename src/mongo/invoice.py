import logging
import os
import sys

import mongo.mongo_client as mongo_client

sys.path.append(
  os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../'))

import config

class InvoiceDocument:
  def __init__(self,
    user_id : int,
    invoice_id : int,
    paid : bool = False
  ):
    self.user_id_ = user_id
    self.invoice_id_ = invoice_id
    self.paid_ = paid

class InvoiceDB:
  def __init__(self) -> None:
    self.client_ = mongo_client.MongoClientWrapper(
      config.INVOICE_DB_PATH,
      config.INVOICE_COLLECTION_PATH)

  def create_invoice(self, document : InvoiceDocument):
    invoice = None

    try:
      session = self.client_.open_session()
      invoice = self.client_.create({
        'user-id' : document.user_id_,
        'invoice-id' : document.invoice_id_,
        'paid' : document.paid_}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'InvoiceDB :: Unable to create new invoice {document.invoice_id_} for user {document.user_id_}, error: {str(error)}')

    return invoice

  def get_invoice(self, invoice_id : int):
    invoice = None

    try:
      session = self.client_.open_session()
      invoice = self.client_.read({'invoice-id' : invoice_id}, session)
      self.client_.close_session(session)
    except Exception as error:
      logging.error(f'InvoiceDB :: Unable to get invoice {invoice_id}, error: {str(error)}')

    if(None is not invoice and 0 < len(invoice)):
      return InvoiceDocument(
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
      logging.error(f'InvoiceDB :: Unable to update invoice {invoice_id} paid status to {update}, error: {str(error)}')
