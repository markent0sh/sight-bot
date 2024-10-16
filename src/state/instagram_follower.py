import logging
import os
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from telegram import (
  InlineKeyboardButton,
)

sys.path.append(
  os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../'))

from language.language_state import LanguageState
from language.language_controller import LanguageController
from fsm import State, EventPayload, StateError, StateEvent
import config
import stat_charts

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

def _date_time_machine(period : str, date : str):
  date_format = "%d.%m.%Y"
  current_date = datetime.strptime(date, date_format)

  if period == 'day':
    modified_date = current_date - timedelta(days=1)
  elif period == 'week':
    modified_date = current_date - timedelta(weeks=1)
  elif period == 'month':
    modified_date = current_date - relativedelta(months=1)
  elif period == 'year':
    modified_date = current_date - relativedelta(years=1)
  else:
    return None

  return modified_date.strftime(date_format)

def setup_instagram_followers_main_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersMain :: set_state')
    widget_delegate.clear_keyboard()

    kAtScreenOnce = 5
    counter = 0

    target_list = widget_delegate.get_client_targets_follower()
    for target in target_list:
      target_row = []
      target_row.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_5', target.username), callback_data=f'fm_target_<{target.username}>_btn'))
      target_row.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_2'), callback_data=f'fm_remove_<{target.username}>_btn'))
      widget_delegate.add_row(target_row)
      counter = counter + 1

      if counter == kAtScreenOnce and counter != len(target_list):
        widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_12'), callback_data=f'fm_next_page_{counter}_btn')])
        break

    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_1'), callback_data='fm_new_target_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_17'), callback_data='fm_help_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])

    subtext = ''

    if 0 < len(target_list):
      subtext = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_3')
    else:
      subtext = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_2')

    widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_1', subtext))
    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramFollowersMain :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info(f'InstagramFollowersMain :: handle_event: {event}, {payload.page_offset}')
    error = StateError.eNOK

    if(0):
      pass
    elif(StateEvent.eSightNext is event):
      widget_delegate.clear_keyboard()
      target_list = widget_delegate.get_client_targets_follower()

      kAtScreenOnce = 5
      effective_counter = 0
      counter = 0

      for target in target_list:

        if counter >= payload.page_offset:
          target_row = []
          target_row.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_5', target.username), callback_data=f'fm_target_<{target.username}>_btn'))
          target_row.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_2'), callback_data=f'fm_remove_<{target.username}>_btn'))
          widget_delegate.add_row(target_row)
          effective_counter = effective_counter + 1

        counter = counter + 1

        if counter == (payload.page_offset + kAtScreenOnce):

          if counter != len(target_list):
            widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_12'), callback_data=f'fm_next_page_{counter}_btn')])

          widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_13'), callback_data=f'fm_prev_page_{(counter - effective_counter)}_btn')])
          break
        elif counter == len(target_list):
          widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_13'), callback_data=f'fm_prev_page_{(counter - effective_counter)}_btn')])

      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_1'), callback_data='fm_new_target_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_17'), callback_data='fm_help_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      subtext = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_3')
      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_1', subtext))
      widget_delegate.trigger_update()
      error = StateError.eOK
    elif(StateEvent.eSightPrev is event):
      widget_delegate.clear_keyboard()
      target_list = widget_delegate.get_client_targets_follower()

      kAtScreenOnce = 5
      effective_counter = 0
      counter = 0

      for target in target_list:

        if counter >= (payload.page_offset - kAtScreenOnce):
          target_row = []
          target_row.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_5', target.username), callback_data=f'fm_target_<{target.username}>_btn'))
          target_row.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_2'), callback_data=f'fm_remove_<{target.username}>_btn'))
          widget_delegate.add_row(target_row)
          effective_counter = effective_counter + 1

        counter = counter + 1

        if counter == payload.page_offset:
          widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_12'), callback_data=f'fm_next_page_{counter}_btn')])

          if (counter - kAtScreenOnce) > 0:
            widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_13'), callback_data=f'fm_prev_page_{(counter - effective_counter)}_btn')])

          break

      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_1'), callback_data='fm_new_target_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_17'), callback_data='fm_help_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      subtext = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_3')
      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_1', subtext))
      widget_delegate.trigger_update()
      error = StateError.eOK

    return error

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event)

def setup_instagram_followers_remove_target_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersRemoveTarget :: set_state')
    widget_delegate.clear_keyboard()
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_14'), callback_data=f'fr_remove_<{payload.target_username}>_btn')])
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_15'), callback_data='back_btn')])
    widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_17', payload.target_username))
    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramFollowersRemoveTarget :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersRemoveTarget :: handle_event')

    if(StateEvent.eInstagramFollowersRemoveTargetConf is event):
      error_code = widget_delegate.unsubscribe_follower(payload.target_username)

      if(0 == error_code):
        widget_delegate.update_subscription_active(payload.target_username, 'follower', False)

      widget_delegate.fire_event(StateEvent.eSightBack)
      return StateError.eOK

    return StateError.eNOK

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event)

def setup_instagram_followers_modify_target_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersModifyTarget :: set_state')
    target_list = widget_delegate.get_client_targets_follower()
    for target in target_list:

      if payload.target_username == target.username:
        follower_track = target.followers
        following_track = target.following

        if None != payload.follower_track:
          follower_track = not follower_track
        elif None != payload.following_track:
          following_track = not following_track

        widget_delegate.unsubscribe_follower(payload.target_username)
        widget_delegate.subscribe_follower(payload.target_username, follower_track, following_track, target.frequency)
        return StateError.eOK

    return StateError.eNOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramFollowersModifyTarget :: quit_state')
    return StateError.eOK

  def pop_event(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersModifyTarget :: pop_event')
    widget_delegate.fire_event(StateEvent.eSightBack)
    return StateError.eOK

  return State(set_state, quit_state, pop_event)

def setup_instagram_followers_get_target_data_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersGetTargetData :: set_state')
    widget_delegate.clear_keyboard()
    subscription = widget_delegate.get_active_subscription(payload.target_username, 'follower')

    if None is not subscription and False == subscription.overdue_:
      text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_6')
      target_list = widget_delegate.get_client_targets_follower()
      for target in target_list:

        if target.username == payload.target_username:

          if True == target.followers and True == target.following:
            types = [
              InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_6'), callback_data=f'fg_followers_<{payload.target_username}>_btn'),
              InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_7'), callback_data=f'fg_following_<{payload.target_username}>_btn')]
            widget_delegate.add_row(types)
            period_text = ''

            if(0):
              pass
            elif(0 == target.frequency):
              period_text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_30')
            elif(1 == target.frequency):
              period_text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_31')
            elif(2 == target.frequency):
              period_text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_32')
            elif(3 == target.frequency):
              period_text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_33')
            elif(4 == target.frequency):
              period_text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_34')

            followers = widget_delegate.get_followers_follower(
              payload.target_username,
              '00:00', '01.01.2000',
              '00:00', '01.01.2100')

            following = widget_delegate.get_following_follower(
              payload.target_username,
              '00:00', '01.01.2000',
              '00:00', '01.01.2100')

            text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_5',
              payload.target_username, period_text,
              len(followers.all),
              len(following.all))

          elif True == target.followers:
            timeranges = []
            timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_8'), callback_data=f'fg_target_<{payload.target_username}>_range_day_followers_btn'))
            timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_9'), callback_data=f'fg_target_<{payload.target_username}>_range_week_followers_btn'))
            timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_10'), callback_data=f'fg_target_<{payload.target_username}>_range_month_followers_btn'))
            timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_11'), callback_data=f'fg_target_<{payload.target_username}>_range_year_followers_btn'))
            widget_delegate.add_row(timeranges)
          elif True == target.following:
            timeranges = []
            timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_8'), callback_data=f'fg_target_<{payload.target_username}>_range_day_following_btn'))
            timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_9'), callback_data=f'fg_target_<{payload.target_username}>_range_week_following_btn'))
            timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_10'), callback_data=f'fg_target_<{payload.target_username}>_range_month_following_btn'))
            timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_11'), callback_data=f'fg_target_<{payload.target_username}>_range_year_following_btn'))
            widget_delegate.add_row(timeranges)
          else:
            text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_7')

      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      widget_delegate.set_text(text)
    else:
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_16'), callback_data='fg_balance_btn')])
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      user = widget_delegate.get_user()
      show_balance = -0.99

      if None is not user:
        show_balance = user.balance_

      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_19', show_balance))

    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramFollowersGetTargetData :: quit_state')
    widget_delegate.clear_keyboard()
    widget_delegate.clear_follower_info_in()
    widget_delegate.clear_follower_info_out()
    widget_delegate.clear_follower_image()
    widget_delegate.clear_follower_pdf()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersGetTargetData :: handle_event')
    error = StateError.eOK

    if(StateEvent.eSightUserInput == event):

      if None != payload.range:
        from_date, from_time = _get_current_utc_date_time()
        to_date, to_time = _get_current_utc_date_time()
        from_date = _date_time_machine(payload.range, from_date)
        target_list = widget_delegate.get_client_targets_follower()

        for target in target_list:

          if target.username == payload.target_username:
            widget_delegate.clear_keyboard()
            widget_delegate.clear_follower_info_in()
            widget_delegate.clear_follower_info_out()
            text = ''

            if None != payload.follower_track:
              followers = widget_delegate.get_followers_follower(
                payload.target_username,
                from_time, from_date,
                to_time, to_date)

              chart_data = []

              if(0 < len(followers.subscribed)):
                widget_delegate.add_follower_info_in(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_9', len(followers.subscribed)))
                chunks = [followers.subscribed[i:i + 10] for i in range(0, len(followers.subscribed), 10)]
                for chunk in chunks:
                  follower_info = ''
                  for follower in chunk:
                    chart_data.append({
                      'Time': follower.timestamp.time + ' ' + follower.timestamp.date,
                      'Action': 'follow',
                      'Change': 1,
                      'Username': follower.username
                    })
                  widget_delegate.add_follower_info_in(follower_info)

              if(0 < len(followers.unsubscribed)):
                widget_delegate.add_follower_info_out(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_12', len(followers.unsubscribed)))
                chunks = [followers.unsubscribed[i:i + 10] for i in range(0, len(followers.unsubscribed), 10)]
                for chunk in chunks:
                  follower_info = ''
                  for follower in chunk:
                    chart_data.append({
                      'Time': follower.timestamp.time + ' ' + follower.timestamp.date,
                      'Action': 'unfollow',
                      'Change': -1,
                      'Username': follower.username
                    })
                  widget_delegate.add_follower_info_out(follower_info)

              if(0 < len(chart_data)):
                pdf_path = stat_charts.table_stats_range(
                  chart_data,
                  config.LOCAL_STORAGE_PATH,
                  widget_delegate.get_client_id(),
                  from_time + ' ' + from_date,
                  to_time + ' ' + to_date,
                  LanguageController().get_text(
                    widget_delegate.get_client_lang(),
                    'INSTA_FOLL_DESC_28',
                    from_time + ' ' + from_date,
                    to_time + ' ' + to_date),
                  LanguageController().get_text(
                    widget_delegate.get_client_lang(),
                    'INSTA_FOLL_DESC_9',
                    payload.target_username),
                  LanguageController().get_text(
                    widget_delegate.get_client_lang(),
                    'INSTA_FOLL_DESC_12',
                    payload.target_username),
                  LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_29'))
                subtext = LanguageController().get_text(
                  widget_delegate.get_client_lang(),
                  'INSTA_FOLL_DESC_28',
                  from_time + ' ' + from_date,
                  to_time + ' ' + to_date)
                text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_10', subtext)
                widget_delegate.add_follower_pdf(pdf_path)
              else:
                text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_11')

            elif None != payload.following_track:
              following = widget_delegate.get_following_follower(
                payload.target_username,
                from_time, from_date,
                to_time, to_date)

              chart_data = []

              if(0 < len(following.subscribed)):
                widget_delegate.add_follower_info_in(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_13', len(following.subscribed)))
                chunks = [following.subscribed[i:i + 10] for i in range(0, len(following.subscribed), 10)]
                for chunk in chunks:
                  follower_info = ''
                  for follower in chunk:
                    chart_data.append({
                      'Time': follower.timestamp.time + ' ' + follower.timestamp.date,
                      'Action': 'follow',
                      'Change': 1,
                      'Username': follower.username
                    })
                  widget_delegate.add_follower_info_in(follower_info)

              if(0 < len(following.unsubscribed)):
                widget_delegate.add_follower_info_out(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_15', len(following.unsubscribed)))
                chunks = [following.unsubscribed[i:i + 10] for i in range(0, len(following.unsubscribed), 10)]
                for chunk in chunks:
                  follower_info = ''
                  for follower in chunk:
                    chart_data.append({
                      'Time': follower.timestamp.time + ' ' + follower.timestamp.date,
                      'Action': 'unfollow',
                      'Change': -1,
                      'Username': follower.username
                    })
                  widget_delegate.add_follower_info_out(follower_info)

              if(0 < len(chart_data)):
                pdf_path = stat_charts.table_stats_range(
                  chart_data,
                  config.LOCAL_STORAGE_PATH,
                  widget_delegate.get_client_id(),
                  from_time + ' ' + from_date,
                  to_time + ' ' + to_date,
                  LanguageController().get_text(
                    widget_delegate.get_client_lang(),
                    'INSTA_FOLL_DESC_27',
                    from_time + ' ' + from_date,
                    to_time + ' ' + to_date),
                  LanguageController().get_text(
                    widget_delegate.get_client_lang(),
                    'INSTA_FOLL_DESC_13',
                    payload.target_username),
                  LanguageController().get_text(
                    widget_delegate.get_client_lang(),
                    'INSTA_FOLL_DESC_15',
                    payload.target_username),
                  LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_29'))
                subtext = LanguageController().get_text(
                  widget_delegate.get_client_lang(),
                  'INSTA_FOLL_DESC_27',
                  from_time + ' ' + from_date,
                  to_time + ' ' + to_date)
                text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_10', subtext)
                widget_delegate.add_follower_pdf(pdf_path)
              else:
                text = LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_14')

            widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
            widget_delegate.set_text(text)
            widget_delegate.trigger_update()
      else:
        widget_delegate.clear_keyboard()

        if None != payload.follower_track:
          timeranges = []
          timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_8'), callback_data=f'fg_target_<{payload.target_username}>_range_day_followers_btn'))
          timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_9'), callback_data=f'fg_target_<{payload.target_username}>_range_week_followers_btn'))
          timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_10'), callback_data=f'fg_target_<{payload.target_username}>_range_month_followers_btn'))
          timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_11'), callback_data=f'fg_target_<{payload.target_username}>_range_year_followers_btn'))
          widget_delegate.add_row(timeranges)
        elif None != payload.following_track:
          timeranges = []
          timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_8'), callback_data=f'fg_target_<{payload.target_username}>_range_day_following_btn'))
          timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_9'), callback_data=f'fg_target_<{payload.target_username}>_range_week_following_btn'))
          timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_10'), callback_data=f'fg_target_<{payload.target_username}>_range_month_following_btn'))
          timeranges.append(InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_11'), callback_data=f'fg_target_<{payload.target_username}>_range_year_following_btn'))
          widget_delegate.add_row(timeranges)

        widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
        widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_6'))
        widget_delegate.trigger_update()

    else:
      error = StateError.eNOK

    return error

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event)

def setup_instagram_followers_set_new_target_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersSetNewTarget :: set_state')

    if(False is payload.pop_on_set):
      widget_delegate.clear_keyboard()
      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_4'))
      widget_delegate.trigger_update()

    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramFollowersSetNewTarget :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersSetNewTarget :: handle_event')

    if(StateEvent.eSightUserInput == event):

      if(None is not payload.target_username):
        widget_delegate.fire_event(StateEvent.eInstagramFollowersSetNewTargetFrequency, payload)
      else:
        widget_delegate.clear_keyboard()
        widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
        widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_16'))
        widget_delegate.trigger_update()
        return StateError.eOK

    return StateError.eNOK

  def pop_event(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersSetNewTarget :: pop_event')

    if(True is payload.pop_on_set):
      widget_delegate.fire_event(StateEvent.eSightBack)

    return StateError.eOK

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event, pop_event_call=pop_event)


def setup_instagram_followers_set_new_target_frequency_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersSetNewTargetFrequency :: set_state')

    if(None is not payload.target_username):
      widget_delegate.clear_keyboard()
      options = [
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_18'), callback_data=f'fs_target_<{payload.target_username}>_freq_$0_btn'),
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_19'), callback_data=f'fs_target_<{payload.target_username}>_freq_$1_btn'),
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_20'), callback_data=f'fs_target_<{payload.target_username}>_freq_$2_btn'),
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_21'), callback_data=f'fs_target_<{payload.target_username}>_freq_$3_btn'),
        InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_22'), callback_data=f'fs_target_<{payload.target_username}>_freq_$4_btn')]
      widget_delegate.add_row(options)

      widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
      widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_8'))
      widget_delegate.trigger_update()

    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramFollowersSetNewTargetFrequency :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  def handle_event(widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersSetNewTargetFrequency :: handle_event')

    if(StateEvent.eSightUserInput == event):

      if(None is not payload.target_username and None is not payload.target_frequency):
        user = widget_delegate.get_user()

        if None is not user:

          if config.FOLLOWER_TARGET_PRICES[payload.target_frequency] <= user.balance_:
            error_code = widget_delegate.subscribe_follower(payload.target_username, True, True, payload.target_frequency)

            if 0 == error_code:
              date_str, time_str = _get_current_utc_date_time()
              widget_delegate.update_user_balance(user.balance_ - config.FOLLOWER_TARGET_PRICES[payload.target_frequency])
              widget_delegate.create_subscription(
                payload.target_username,
                date_str, time_str,
                'follower',
                payload.target_frequency)

            payload.pop_on_set = True
            widget_delegate.fire_event(StateEvent.eSightBack, payload)
          else:
            widget_delegate.clear_keyboard()
            widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_BTN_16'), callback_data='fs_balance_btn')])
            widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
            widget_delegate.set_text(
              LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_18', user.balance_, config.FOLLOWER_TARGET_PRICES[payload.target_frequency] - user.balance_))
            widget_delegate.trigger_update()

          return StateError.eOK

    return StateError.eNOK

  def pop_event(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersSetNewTargetFrequency :: pop_event')

    if(None is payload.target_username):
      widget_delegate.fire_event(StateEvent.eSightBack)

    return StateError.eOK

  return State(set_state_call=set_state, quit_state_call=quit_state, handle_event_call=handle_event, pop_event_call=pop_event)


def setup_instagram_followers_help_state() -> State:
  def set_state(widget_delegate, payload : EventPayload) -> StateError:
    logging.info('InstagramFollowersHelp :: set_state')
    widget_delegate.clear_keyboard()
    widget_delegate.add_row([InlineKeyboardButton(LanguageController().get_text(widget_delegate.get_client_lang(), 'BACK_BTN'), callback_data='back_btn')])
    widget_delegate.set_text(LanguageController().get_text(widget_delegate.get_client_lang(), 'INSTA_FOLL_DESC_20'))
    widget_delegate.trigger_update()
    return StateError.eOK

  def quit_state(widget_delegate) -> StateError:
    logging.info('InstagramFollowersHelp :: quit_state')
    widget_delegate.clear_keyboard()
    return StateError.eOK

  return State(set_state, quit_state)
