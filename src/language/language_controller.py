from enum import Enum
import json
import logging

class LanguageType(Enum):
  eEnglish = 0,
  eRussian = 1

class LanguageController(object):
  _instance = None

  def __new__(cls):

    if not cls._instance:
      cls._instance = super(LanguageController, cls).__new__(cls)

    return cls._instance

  def __init__(self) -> None:

    if 'models_path_' not in self.__dict__:
      self.models_path_ = None
      self.active_models_ = {}

  def set_models_path(self, models_path : str):
    self.models_path_ = models_path

  def set_languages(self, languages):
    self._load_models(languages)

  def _load_models(self, languages):
    try:
      for language in languages:
        new_model = None
        model_path = self._language_to_path(language)

        if None != model_path:
          with open(model_path, 'r') as file:
            new_model = json.load(file)

        self.active_models_[language] = new_model
    except Exception as error:
      logging.error(f'Unable to load language, error: {str(error)}')

  def get_text(self, language : LanguageType, text_id : str, *args) -> str:
    return_text = 'None'

    if language in self.active_models_:
      try:
        return_text = self._place_args(self.active_models_[language].get(text_id), *args)
      except Exception as error:
        logging.error(f'Unable to get text  with id: {text_id}, error: {str(error)}')

    return return_text

  def _place_args(self, template, *args):

    if None is template:
      return template

    placeholders = template.count('<var>')

    if placeholders != len(args):
      raise ValueError(f'Mismatch in placeholders, expected {placeholders} arguments, got {len(args)}')

    result = template
    for arg in args:
      result = result.replace('<var>', str(arg), 1)

    return result

  def _language_to_path(self, language : LanguageType):
    path = None
    model_name = None

    if(0):
      pass
    elif(LanguageType.eEnglish is language):
      model_name = 'english.json'
    elif(LanguageType.eRussian is language):
      model_name = 'russian.json'

    if None != model_name:

      if None != self.models_path_:

        if(self.models_path_[len(self.models_path_) - 1] != '/'):
          model_name = '/' + model_name

        path = self.models_path_ + model_name
        logging.info(f'_language_to_path: {path}')

    return path

def main():
  controller = LanguageController()
  controller.set_models_path('/home/mark-ssd/code/mdb/src/tg-bot/language/models/')
  controller.set_languages([LanguageType.eEnglish, LanguageType.eRussian])

  another_controller = LanguageController()
  msg = another_controller.get_text(LanguageType.eRussian, 'BACK_BTN')
  logging.info(f'{msg}')

if __name__ == "__main__":
  logging.basicConfig(
    level = logging.INFO,
    format = '%(name)s - %(levelname)s - %(message)s')

  main()
