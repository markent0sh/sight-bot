import logging

import config
import controller
import language.language_controller as language
from event_generator import EventGenerator

logging.basicConfig(
  # filename = 'bot.log',
  # filemode = 'a',
  level = logging.INFO,
  format = '%(name)s - %(levelname)s - %(message)s'
)

def main() -> None:
  logging.info('Bot started')
  EventGenerator()
  language_controller = language.LanguageController()
  language_controller.set_models_path(config.LANGUAGE_MODELS_PATH)
  language_controller.set_languages([language.LanguageType.eRussian, language.LanguageType.eEnglish])

  application = controller.ApplicationController(config.TG_API_TOKEN)
  application.run()

if __name__ == "__main__":
  main()
