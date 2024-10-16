
import logging
import os
import sys
from datetime import datetime

from telegram import (
  InlineKeyboardButton,
  InputMediaPhoto,
  InputMediaVideo
)

sys.path.append(
  os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../'))

from language.language_controller import LanguageController
from fsm import State, EventPayload, StateError, StateEvent
import config

def _get_current_utc_date_time():
  """
  Returns the current UTC date and time formatted as 'HH:MM' and 'DD.MM.YY'.

  Returns:
    tuple: Contains two strings (date, time)
  """
  current_utc_datetime = datetime.utcnow()
  date_str = current_utc_datetime.strftime("%d.%m.%Y")
  time_str = current_utc_datetime.strftime("%H:%M")
  return date_str, time_str

def setup_instagram_stories_main_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramStoriesMain :: set_state')
    widget_delegate.clear_keyboard()

    kAtScreenOnce = 5
    counter = 0

    target_list = widget_delegate.get_client_targets_story()
    for target in target_list:
      widget_delegate.add_row([
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_3', target.username), callback_data=f'sm_target_<{target.username}>_btn'),
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_2'), callback_data=f'sm_remove_<{target.username}>_btn')
      ])
      counter = counter + 1

      if counter == kAtScreenOnce and counter != len(target_list):
        widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_4'), callback_data=f'sm_next_page_{counter}_btn')])
        break

    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_1'), callback_data='sm_new_target_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_9'), callback_data='sm_help_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])

    subtext = ''

    if 0 < len(target_list):
      subtext = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_3')
    else:
      subtext = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_2')

    widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_1', subtext))
    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramStoriesMain :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info(f'InstagramStoriesMain :: handle_event: {event}, {payload.page_offset}')
    error = StateError.eNOK

    if(0):
      pass
    elif(StateEvent.eSightNext is event):
      widget_delegate.clear_keyboard()
      target_list = widget_delegate.get_client_targets_story()

      kAtScreenOnce = 5
      effective_counter = 0
      counter = 0

      for target in target_list:

        if counter >= payload.page_offset:
          widget_delegate.add_row([
            InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_3', target.username), callback_data=f'sm_target_<{target.username}>_btn'),
            InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_2'), callback_data=f'sm_remove_<{target.username}>_btn')
          ])
          effective_counter = effective_counter + 1

        counter = counter + 1

        if counter == (payload.page_offset + kAtScreenOnce):

          if counter != len(target_list):
            widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_4'), callback_data=f'sm_next_page_{counter}_btn')])

          widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_5'), callback_data=f'sm_prev_page_{(counter - effective_counter)}_btn')])
          break
        elif counter == len(target_list):
          widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_5'), callback_data=f'sm_prev_page_{(counter - effective_counter)}_btn')])

      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_1'), callback_data='sm_new_target_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_9'), callback_data='sm_help_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      subtext = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_3')
      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_1', subtext))
      widget_delegate.trigger_update()
      error = StateError.eOK
    elif(StateEvent.eSightPrev is event):
      widget_delegate.clear_keyboard()
      target_list = widget_delegate.get_client_targets_story()

      kAtScreenOnce = 5
      effective_counter = 0
      counter = 0

      for target in target_list:

        if counter >= (payload.page_offset - kAtScreenOnce):
          widget_delegate.add_row([
            InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_3', target.username), callback_data=f'sm_target_<{tartarget.usernameget}>_btn'),
            InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_2'), callback_data=f'sm_remove_<{target.username}>_btn')
          ])
          effective_counter = effective_counter + 1

        counter = counter + 1

        if counter == payload.page_offset:
          widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_4'), callback_data=f'sm_next_page_{counter}_btn')])

          if (counter - kAtScreenOnce) > 0:
            widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_5'), callback_data=f'sm_prev_page_{(counter - effective_counter)}_btn')])

          break

      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_1'), callback_data='sm_new_target_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_9'), callback_data='sm_help_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      subtext = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_3')
      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_1', subtext))
      widget_delegate.trigger_update()
      error = StateError.eOK

    return error

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event)

def setup_instagram_stories_remove_target_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramStoriesRemoveTarget :: set_state')
    widget_delegate.clear_keyboard()
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_6'), callback_data=f'sr_remove_<{payload.target_username}>_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_7'), callback_data='back_btn')])
    widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_8', payload.target_username))
    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramStoriesRemoveTarget :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info('InstagramStoriesRemoveTarget :: handle_event')

    if(StateEvent.eInstagramStoriesRemoveTargetConf is event):
      error_code = widget_delegate.unsubscribe_story(payload.target_username)

      if(0 == error_code):
        widget_delegate.update_subscription_active(payload.target_username, 'story', False)

      widget_delegate.fire_event(StateEvent.eSightBack)
      return StateError.eOK

    return StateError.eNOK

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event)

def setup_instagram_stories_get_target_data_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramStoriesGetTargetData :: set_state')
    widget_delegate.clear_keyboard()

    subscription = widget_delegate.get_active_subscription(payload.target_username, 'story')

    if None is not subscription and False == subscription.overdue_:
      widget_delegate.clear_media()
      stories = widget_delegate.get_available_stories_story(payload.target_username)
      success_counter = 0
      for story in stories:
        try:
          media = None

          caption_text = LanguageController().get_text(widget_delegate.get_client_lang(),
            'INSTA_STOR_DESC_5',
            story.timestamp.time,
            story.timestamp.date)

          if('.mp4' in story.uri):
            media = InputMediaVideo(
              open(story.uri, 'rb'),
              caption_text)
          else:
            media = InputMediaPhoto(
              open(story.uri, 'rb'),
              caption_text)

          if None != media:
            widget_delegate.add_media(media)
            success_counter = success_counter + 1

        except Exception as error:
          logging.warning(f'Unable to open file {story.uri}')

      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      period_text = ''

      if(0):
        pass
      elif(0 == subscription.frequency_):
        period_text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_13')
      elif(1 == subscription.frequency_):
        period_text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_14')
      elif(2 == subscription.frequency_):
        period_text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_15')
      elif(3 == subscription.frequency_):
        period_text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_16')
      elif(4 == subscription.frequency_):
        period_text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_17')

      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_6', period_text, success_counter))
      widget_delegate.trigger_update()
    else:
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_8'), callback_data='sg_balance_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      user = widget_delegate.get_user()
      show_balance = -0.99

      if None is not user:
        show_balance = user.balance_

      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_10', show_balance))
      widget_delegate.trigger_update()

    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramStoriesGetTargetData :: quit_state')
    widget_delegate.clear_keyboard()
    widget_delegate.clear_media()
    return StateError.eOK

  return State(set_state, quit_state)

def setup_instagram_stories_set_new_target_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramStoriesSetNewTarget :: set_state')

    if(False is payload.pop_on_set):
      widget_delegate.clear_keyboard()
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_4'))
      widget_delegate.trigger_update()

    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramStoriesSetNewTarget :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info('InstagramStoriesSetNewTarget :: handle_event')

    if(StateEvent.eSightUserInput == event):

      if(None is not payload.target_username):
        widget_delegate.fire_event(StateEvent.eInstagramStoriesSetNewTargetFrequency, payload)
      else:
        widget_delegate.clear_keyboard()
        widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
        widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_7'))
        widget_delegate.trigger_update()
        return StateError.eOK

    return StateError.eNOK

  def pop_event(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramStoriesSetNewTarget :: pop_event')

    if(True is payload.pop_on_set):
      widget_delegate.fire_event(StateEvent.eSightBack)

    return StateError.eOK

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event, pop_event_call=pop_event)

def setup_instagram_stories_set_new_target_frequency_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramStoriesSetNewTargetFrequency :: set_state')

    if(None is not payload.target_username):
      widget_delegate.clear_keyboard()
      options = [
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_10'), callback_data=f'ss_target_<{payload.target_username}>_freq_$0_btn'),
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_11'), callback_data=f'ss_target_<{payload.target_username}>_freq_$1_btn'),
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_12'), callback_data=f'ss_target_<{payload.target_username}>_freq_$2_btn'),
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_13'), callback_data=f'ss_target_<{payload.target_username}>_freq_$3_btn'),
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_14'), callback_data=f'ss_target_<{payload.target_username}>_freq_$4_btn')]
      widget_delegate.add_row(options)

      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_12'))
      widget_delegate.trigger_update()

    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramStoriesSetNewTargetFrequency :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info('InstagramStoriesSetNewTargetFrequency :: handle_event')

    if(StateEvent.eSightUserInput == event):

      if(None is not payload.target_username and None is not payload.target_frequency):
        user = widget_delegate.get_user()

        if None is not user:

          if config.STORY_TARGET_PRICES[payload.target_frequency] <= user.balance_:
            error_code = widget_delegate.subscribe_story(payload.target_username, payload.target_frequency)

            if 0 == error_code:
              date_str, time_str = _get_current_utc_date_time()
              widget_delegate.update_user_balance(user.balance_ - config.STORY_TARGET_PRICES[payload.target_frequency])
              widget_delegate.create_subscription(
                payload.target_username,
                date_str, time_str,
                'story',
                payload.target_frequency)

            payload.pop_on_set = True
            widget_delegate.fire_event(StateEvent.eSightBack, payload)
          else:
            widget_delegate.clear_keyboard()
            widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_BTN_8'), callback_data='ss_balance_btn')])
            widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
            widget_delegate.set_text(
              LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_9', user.balance_, config.FOLLOWER_TARGET_PRICES[payload.target_frequency] - user.balance_))
            widget_delegate.trigger_update()

          return StateError.eOK

    return StateError.eNOK

  def pop_event(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramStoriesSetNewTargetFrequency :: pop_event')

    if(None is payload.target_username):
      widget_delegate.fire_event(StateEvent.eSightBack)

    return StateError.eOK

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event, pop_event_call=pop_event)


def setup_instagram_stories_help_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramStoriesHelp :: set_state')
    widget_delegate.clear_keyboard()
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
    widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_STOR_DESC_11'))
    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramStoriesHelp :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  return State(set_state, quit_state)
