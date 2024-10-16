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
from language.language_state import LanguageState
from fsm import State, EventPayload, StateError, StateEvent
import config

def setup_settings_main_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('SightSettingsMain :: set_state')
    widget_delegate.clear_keyboard()
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_MAIN_BTN_1'), callback_data='sm_language_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_MAIN_BTN_2'), callback_data='sm_balance_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_MAIN_BTN_3'), callback_data='sm_referral_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_MAIN_BTN_4'), callback_data='sm_notify_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])

    user = widget_delegate.get_user()
    subtext = ''

    if None is not user:

      if True is user.welcome_:
        subtext = LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_MAIN_DESC_2')

      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_MAIN_DESC_1', widget_delegate.get_client_id(), user.balance_, subtext))
      widget_delegate.trigger_update()
      return StateError.eOK

    return StateError.eNOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('SightSettingsMain :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  return State(set_state, quit_state)

def setup_settings_lang_main_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('SightSettingsLangMain :: set_state')
    widget_delegate.clear_keyboard()
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_LANG_MAIN_BTN_1'), callback_data='lm_russian_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_LANG_MAIN_BTN_2'), callback_data='lm_english_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
    widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_LANG_MAIN_DESC_1'))
    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('SightSettingsLangMain :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info('SightSettingsLangMain :: handle_event')

    if(0):
      pass
    elif(StateEvent.eSettingsLanguageRussian is event):
      LanguageState().update_language(widget_delegate.get_client_id(), 'russian')
      widget_delegate.update_language('russian')
      widget_delegate.fire_event(StateEvent.eSightBack)
    elif(StateEvent.eSettingsLanguageEnglish is event):
      LanguageState().update_language(widget_delegate.get_client_id(), 'english')
      widget_delegate.update_language('english')
      widget_delegate.fire_event(StateEvent.eSightBack)

    return StateError.eOK

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event)

def setup_settings_notify_main_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('SightSettingsNotifyMain :: set_state')
    widget_delegate.clear_keyboard()
    user = widget_delegate.get_user()

    if None is not user:
      notify_icon = (lambda expression: '🔔' if expression else '🔕')
      inverse_notify_icon = (lambda expression: '🔕' if expression else '🔔')

      widget_delegate.add_row(
        [InlineKeyboardButton(
          LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_NOTIFY_MAIN_BTN_1', inverse_notify_icon(user.stories_notify_)), callback_data='nm_stories_btn')])
      widget_delegate.add_row(
        [InlineKeyboardButton(
          LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_NOTIFY_MAIN_BTN_2', inverse_notify_icon(user.followers_notify_)), callback_data='nm_followers_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      widget_delegate.set_text(
        LanguageController().get_text(widget_delegate.get_client_lang(),
          'SETTINGS_NOTIFY_MAIN_DESC_1',
          notify_icon(user.stories_notify_),
          notify_icon(user.followers_notify_)))

      widget_delegate.trigger_update()
      return StateError.eOK

    return StateError.eNOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('SightSettingsNotifyMain :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info('SightSettingsNotifyMain :: handle_event')
    updated = None
    user = widget_delegate.get_user()

    if(None is user):
      pass
    elif(StateEvent.eSettingsNotifyToggleStories is event):
      user.stories_notify_ = not user.stories_notify_
      widget_delegate.update_stories_notify(user.stories_notify_)
      updated = True
    elif(StateEvent.eSettingsNotifyToggleFollowers is event):
      user.followers_notify_ = not user.followers_notify_
      widget_delegate.update_followers_notify(user.followers_notify_)
      updated = True

    if None != updated:
      widget_delegate.clear_keyboard()
      notify_icon = (lambda expression: '🔔' if expression else '🔕')
      inverse_notify_icon = (lambda expression: '🔕' if expression else '🔔')

      widget_delegate.add_row(
        [InlineKeyboardButton(
          LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_NOTIFY_MAIN_BTN_1', inverse_notify_icon(user.stories_notify_)), callback_data='nm_stories_btn')])
      widget_delegate.add_row(
        [InlineKeyboardButton(
          LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_NOTIFY_MAIN_BTN_2', inverse_notify_icon(user.followers_notify_)), callback_data='nm_followers_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      widget_delegate.set_text(
        LanguageController().get_text(widget_delegate.get_client_lang(),
          'SETTINGS_NOTIFY_MAIN_DESC_1',
          notify_icon(user.stories_notify_),
          notify_icon(user.followers_notify_)))

      widget_delegate.trigger_update()
      return StateError.eOK

    return StateError.eNOK

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event)

def setup_settings_referral_main_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('SightSettingsReferralMain :: set_state')
    widget_delegate.clear_keyboard()
    subtext = ''

    user = widget_delegate.get_user()

    if None is not user:

      if 0 == user.beneficiary_:
        widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_REFERRALS_MAIN_BTN_1'), callback_data='sr_connect_referral_btn')])
        subtext = LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_REFERRALS_MAIN_DESC_2')

      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])

      referrals = user.referrals_
      bonuses = 0
      for referral in referrals.referrals_:
        bonuses = bonuses + referral['bonuses']

      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_REFERRALS_MAIN_DESC_1', len(referrals.referrals_), bonuses, user.user_id_, subtext))
      widget_delegate.trigger_update()
      return StateError.eOK

    return StateError.eNOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('SightSettingsReferralMain :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  return State(set_state_call=set_state, quit_state_call=quit_state)

def setup_settings_referral_connect_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('SightSettingsReferralConnect :: set_state')
    widget_delegate.clear_keyboard()
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
    widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_REFERRALS_CONNECT_DESC_1'))
    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('SightSettingsReferralConnect :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info(f'SightSettingsReferralConnect :: handle_event: {payload.code}')

    if(StateEvent.eSightUserInput is event):
      success = True

      if(None == payload.code):
        success = False
      else:
        me = widget_delegate.get_user()
        code_owner = widget_delegate.get_user(payload.code)

        if(None != code_owner and None != me):
          referrals = code_owner.referrals_
          referrals.append(
            user_id = me.user_id_,
            bonuses = 0)
          widget_delegate.update_referrals(code_owner.user_id_, referrals.referrals_)
          widget_delegate.update_beneficiary(code_owner.user_id_)
          widget_delegate.fire_event(StateEvent.eSightBack)
          return StateError.eOK
        else:
          success = False

      if False == success:
        widget_delegate.clear_keyboard()
        widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
        widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'SETTINGS_REFERRALS_CONNECT_DESC_2'))
        widget_delegate.trigger_update()
        return StateError.eOK

    return StateError.eNOK

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event)


def setup_settings_balance_main_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('BalanceMain :: set_state')
    widget_delegate.clear_keyboard()
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_MAIN_BTN_1'), callback_data='sm_balance_deposit_crypto_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_MAIN_BTN_2'), callback_data='sm_balance_fiat_deposit_btn')])

    user = widget_delegate.get_user()

    if None is not user:

      if 0 == user.balance_ and True is user.welcome_:
        widget_delegate.update_user_balance(config.DIAMOND_WELCOME_BONUS)
        widget_delegate.update_welcome(False)
        user.balance_ = config.DIAMOND_WELCOME_BONUS

      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_MAIN_DESC_1', user.balance_))

      widget_delegate.trigger_update()
      return StateError.eOK

    return StateError.eNOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('BalanceMain :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  return State(set_state, quit_state)

def setup_settings_balance_deposit_main_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('DepositMain :: set_state')
    widget_delegate.clear_keyboard()
    options = [# 1$ = 5V
      InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_BTN_1', 25), callback_data='sm_balance_deposit_amount_5_btn'),
      InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_BTN_1', 50), callback_data='sm_balance_deposit_amount_10_btn'),
      InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_BTN_1', 100), callback_data='sm_balance_deposit_amount_20_btn')]
    widget_delegate.add_row(options)

    options = [# 1$ = 5V
      InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_BTN_1', 250), callback_data='sm_balance_deposit_amount_50_btn'),
      InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_BTN_1', 500), callback_data='sm_balance_deposit_amount_100_btn'),
      InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_BTN_1', 1000), callback_data='sm_balance_deposit_amount_200_btn')]
    widget_delegate.add_row(options)

    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_BTN_2'), callback_data='sm_balance_deposit_custom_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
    widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_DESC_1'))
    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('DepositMain :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info('DepositMain :: handle_event')

    if(StateEvent.eSightUserInput == event):
      success = True

      if(None == payload.amount or payload.amount < config.MINIMUM_TOP_UP):
        success = False
      else:
        invoice = widget_delegate.create_crypto_invoice(payload.amount)

        if(None != invoice):
          widget_delegate.write_crypto_invoice(invoice.invoice_id)
          widget_delegate.clear_keyboard()
          widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_BTN_3'), url=invoice.bot_invoice_url, callback_data='back_btn')])
          widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
          widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_DESC_2'))
          widget_delegate.trigger_update()
          return StateError.eOK
        else:
          success = False

      if False == success:
        widget_delegate.clear_keyboard()
        widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
        widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_DESC_3'))
        widget_delegate.trigger_update()
        return StateError.eOK
    elif(StateEvent.eSightUserInputRequest == event):
      widget_delegate.clear_keyboard()
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'BALANCE_DEPOSIT_DESC_4'))
      widget_delegate.trigger_update()
      return StateError.eOK

    return StateError.eNOK

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event)
