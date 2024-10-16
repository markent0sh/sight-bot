from language.language_controller import LanguageType
import logging

class LanguageState(object):
  _instance = None

  def __new__(cls):

    if not cls._instance:
      cls._instance = super(LanguageState, cls).__new__(cls)

    return cls._instance

  def __init__(self) -> None:

    if 'users_' not in self.__dict__:
      self.users_ = {}

  def update_language(self, user_id : int, language : str):

    if(0):
      pass
    elif('russian' == language):
      self.users_[user_id] = LanguageType.eRussian
    elif('english' == language):
      self.users_[user_id] = LanguageType.eEnglish
    else:
      logging.warning(f'Unknown language ({language}) passed for user {user_id}')
      self.users_[user_id] = LanguageType.eRussian

    logging.info(f'>>>> user: {user_id} language set to {language}')

  def get_language(self, user_id : int):
    language = self.users_.get(user_id)

    if None is language:
      language = LanguageType.eRussian

    return language

def main():
  controller = LanguageState()

if __name__ == "__main__":
  logging.basicConfig(
    level = logging.INFO,
    format = '%(name)s - %(levelname)s - %(message)s')

  main()
