from pymongo import MongoClient
import logging

class MongoClientWrapper:
  def __init__(self, database : str, collection : str) -> None:
    self.client_ = MongoClient('mongodb://localhost:27017/')
    self.db_ = self.client_[database]
    self.collection_ = self.db_[collection]

  def open_session(self):
    return self.client_.start_session()

  def close_session(self, session):
    session.end_session()

  def create(self, document, session):
    result = None

    try:
      result = self.collection_.insert_one(document, session = session)
    except Exception as error:
      logging.error(f'Unable to create document: {error.__str__()}')
      result = None

    return result

  def read(self, query, session):
    result = None

    try:
      result = list(self.collection_.find(query, session = session))
    except Exception as error:
      logging.error(f'Unable to read document: {error.__str__()}')
      result = None

    return result

  def update(self, query, document, session):
    result = None

    try:
      result = self.collection_.update_many(query, {'$set': document}, session = session)
    except Exception as error:
      logging.error(f'Unable to update document: {error.__str__()}')
      result = None

    return result

  def delete(self, query, session):
    result = None

    try:
      result = self.collection_.delete_many(query, session = session)
    except Exception as error:
      logging.error(f'Unable to delete document: {error.__str__()}')
      result = None

    return result

if __name__ == "__main__":
  logging.basicConfig(
    level = logging.INFO,
    format = '%(name)s - %(levelname)s - %(message)s'
  )

  client = MongoClientWrapper(
    'pymongo-client-test-db',
    'pymongo-client-test-collection')

  session = client.open_session()

  client.create({
    'client-id' : 'misha1448',
    'balance' : 80,
    'is_virgin' : True
  }, session)

  client.create({
    'client-id' : 'griwa',
    'balance' : 560,
    'is_virgin' : False
  }, session)

  client.create({
    'client-id' : 'snfiefnnfkjew',
    'balance' : 0,
    'is_virgin' : True
  }, session)

  logging.info('>>>>> ALL VIRGINS >>>>>>>>>>> (BEFORE)')
  read_result = client.read({'is_virgin' : True}, session)
  logging.info(f'{read_result}')

  read_result = client.read({'is_virgin' : False}, session)
  logging.info('>>>>> ALL SEX MACHINES >>>>>>>>>>> (BEFORE)')
  logging.info(f'{read_result}')

  client.update({'is_virgin' : False}, {'is_virgin' : True}, session)

  read_result = client.read({'is_virgin' : True}, session)
  logging.info('>>>>> ALL VIRGINS >>>>>>>>>>> (AFTER)')
  logging.info(f'{read_result}')

  read_result = client.read({'is_virgin' : False}, session)
  logging.info('>>>>> ALL SEX MACHINES >>>>>>>>>>> (AFTER)')
  logging.info(f'{read_result}')

  client.delete({'is_virgin' : True}, session)
  client.close_session(session)
