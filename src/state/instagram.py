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

def setup_instagram_main_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramMain :: set_state')
    widget_delegate.clear_keyboard()
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_MAIN_BTN_1'), callback_data='im_stories_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_MAIN_BTN_2'), callback_data='im_followers_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_MAIN_BTN_3'), callback_data='im_likes_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
    widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_MAIN_DESC_1'))
    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramMain :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  return State(set_state, quit_state)
