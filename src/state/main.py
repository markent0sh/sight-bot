import logging
import os
import sys

from telegram import (
  InlineKeyboardButton,
)

sys.path.append(
  os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../'))

from language.language_controller import LanguageController
from fsm import State, EventPayload, StateError
import config

def setup_sight_main_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('SightMain :: set_state')
    widget_delegate.clear_keyboard()
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'SIGHT_MAIN_BTN_1'), callback_data='sm_instagram_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'SIGHT_MAIN_BTN_2'), callback_data='sm_balance_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'SIGHT_MAIN_BTN_3'), callback_data='sm_settings_btn')])
    widget_delegate.add_row(
      [InlineKeyboardButton(
        LanguageController().get_text(widget_delegate.get_client_lang(), 'SIGHT_MAIN_BTN_4'),
        url=config.NEWS_GROUP_URL,
        callback_data='news_btn')])
    widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'SIGHT_MAIN_DESC_1'))
    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('SightMain :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  return State(set_state, quit_state)
