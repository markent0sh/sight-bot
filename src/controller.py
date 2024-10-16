import logging
import re
import asyncio

from telegram import (
  Update,
  InlineKeyboardMarkup
)

from telegram.ext import (
  Application,
  CallbackQueryHandler,
  CommandHandler,
  ContextTypes,
  MessageHandler,
  filters
)

import fsm
import widget
import config

from mongo.user import UserDB, UserDocument

from language.language_controller import LanguageController
from language.language_state import LanguageState

from event_generator import EventGenerator

class ApplicationController:
  def __init__(self, token) -> None:
    self.application_ = Application.builder().token(token).build()
    self.application_.add_handler(CommandHandler("start", self.start_command))
    self.application_.add_handler(CommandHandler("cash", self.balance_command))
    self.application_.add_handler(CommandHandler("ig", self.instagram_command))
    self.application_.add_handler(CommandHandler("adm_sel", self.restart_command)) # Set event loop after bot restart
    self.application_.add_handler(CallbackQueryHandler(self.button_handler))
    self.application_.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))
    self.users_fsm_ = {}
    self.users_chat_ = {}
    self.restored_widgets_ = []
    self.user_db_client_ = UserDB()

  async def restart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
      EventGenerator().set_event_loop(asyncio.get_event_loop())
      self._restore_widgets()
      await update.message.reply_text('Done.')
    except Exception as error:
      logging.error(f'Unable to handle start cmd, error: {error.__str__()}')

  async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
      await self._start_from_state(fsm.StateType.eSightMain, update)
    except Exception as error:
      logging.error(f'Unable to handle start cmd, error: {error.__str__()}')

      try:
        await update.message.reply_text(LanguageController().get_text(LanguageState().get_language(update.message.from_user.id), 'AUTH_ERR_DESC_4'))
      except Exception as error:
        logging.error(f'Unable to send error to the user, error: {error.__str__()}')

  async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
      await self._start_from_state(fsm.StateType.eBalanceMain, update)
    except Exception as error:
      logging.error(f'Unable to handle balance cmd, error: {error.__str__()}')

      try:
        await update.message.reply_text(LanguageController().get_text(LanguageState().get_language(update.message.from_user.id), 'AUTH_ERR_DESC_4'))
      except Exception as error:
        logging.error(f'Unable to send error to the user, error: {error.__str__()}')

  async def instagram_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
      await self._start_from_state(fsm.StateType.eInstagramMain, update)
    except Exception as error:
      logging.error(f'Unable to handle instagtam cmd, error: {error.__str__()}')

      try:
        await update.message.reply_text(LanguageController().get_text(LanguageState().get_language(update.message.from_user.id), 'AUTH_ERR_DESC_4'))
      except Exception as error:
        logging.error(f'Unable to send error to the user, error: {error.__str__()}')

  async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_messages = self.users_fsm_.get(update.callback_query.from_user.id)

    if(None != user_messages):

      message_fsm = user_messages.get(update.callback_query.message.message_id)

      if(None != message_fsm):

        if(0):
          pass
        elif('sm_instagram_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eInstagramMain)
        elif('sm_balance_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eBalanceMain)
        elif('sm_balance_deposit_crypto_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eBalanceDepositMain)
        elif('sm_balance_deposit_amount' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.amount = self._get_amount_from_data(update.callback_query.data)
          message_fsm.handle_internal_event(fsm.StateEvent.eSightUserInput, event_payload)
        elif('sm_balance_deposit_custom_btn' == update.callback_query.data):
          message_fsm.handle_internal_event(fsm.StateEvent.eSightUserInputRequest, fsm.EventPayload())
        elif('sm_referral_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eSettingsReferralsMain)
        elif('sr_connect_referral_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eSettingsReferralsConnect)
        elif('sm_settings_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eSettingsMain)
        elif('sm_language_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eSettingsLanguageMain)
        elif('lm_russian_btn' == update.callback_query.data):
          message_fsm.handle_internal_event(fsm.StateEvent.eSettingsLanguageRussian, fsm.EventPayload())
        elif('lm_english_btn' == update.callback_query.data):
          message_fsm.handle_internal_event(fsm.StateEvent.eSettingsLanguageEnglish, fsm.EventPayload())
        elif('sm_notify_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eSettingsNotifyMain)
        elif('nm_stories_btn' == update.callback_query.data):
          message_fsm.handle_internal_event(fsm.StateEvent.eSettingsNotifyToggleStories, fsm.EventPayload())
        elif('nm_followers_btn' == update.callback_query.data):
          message_fsm.handle_internal_event(fsm.StateEvent.eSettingsNotifyToggleFollowers, fsm.EventPayload())
        elif('im_stories_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eInstagramStoriesMain)
        elif('im_followers_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eInstagramFollowersMain)
        elif('sm_target' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username = self._get_target_from_data(update.callback_query.data)
          message_fsm.handle_event(fsm.StateEvent.eInstagramStoriesGetTargetData, event_payload)
        elif('sm_remove' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username = self._get_target_from_data(update.callback_query.data)
          message_fsm.handle_event(fsm.StateEvent.eInstagramStoriesRemoveTarget, event_payload)
        elif('sr_remove' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username = self._get_target_from_data(update.callback_query.data)
          message_fsm.handle_internal_event(fsm.StateEvent.eInstagramStoriesRemoveTargetConf, event_payload)
        elif('sm_new_target_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eInstagramStoriesSetNewTarget)
        elif('ss_target' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username, event_payload.target_frequency = self._get_target_and_freq_from_data(update.callback_query.data)
          event_payload.target_frequency = int(event_payload.target_frequency)
          message_fsm.handle_internal_event(fsm.StateEvent.eSightUserInput, event_payload)
        elif('ss_balance_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eBalanceMain)
        elif('fg_balance_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eBalanceMain)
        elif('sg_balance_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eBalanceMain)
        elif('fm_target' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username = self._get_target_from_data(update.callback_query.data)
          message_fsm.handle_event(fsm.StateEvent.eInstagramFollowersGetTargetData, event_payload)
        elif('fm_modify' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username = self._get_target_from_data(update.callback_query.data)

          if('followers' in update.callback_query.data):
            event_payload.follower_track = True
          elif('following' in update.callback_query.data):
            event_payload.following_track = True

          message_fsm.handle_event(fsm.StateEvent.eInstagramFollowersModifyTarget, event_payload)
        elif('fg_followers' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username = self._get_target_from_data(update.callback_query.data)
          event_payload.follower_track = True
          message_fsm.handle_internal_event(fsm.StateEvent.eSightUserInput, event_payload)
        elif('fg_following' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username = self._get_target_from_data(update.callback_query.data)
          event_payload.following_track = True
          message_fsm.handle_internal_event(fsm.StateEvent.eSightUserInput, event_payload)
        elif('fg_target' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username, event_payload.range = self._get_target_and_range_from_data(update.callback_query.data)

          if('followers' in update.callback_query.data):
            event_payload.follower_track = True
          elif('following' in update.callback_query.data):
            event_payload.following_track = True

          message_fsm.handle_internal_event(fsm.StateEvent.eSightUserInput, event_payload)
        elif('fm_remove' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username = self._get_target_from_data(update.callback_query.data)
          message_fsm.handle_event(fsm.StateEvent.eInstagramFollowersRemoveTarget, event_payload)
        elif('fr_remove' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username = self._get_target_from_data(update.callback_query.data)
          message_fsm.handle_internal_event(fsm.StateEvent.eInstagramFollowersRemoveTargetConf, event_payload)
        elif('fm_new_target_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eInstagramFollowersSetNewTarget)
        elif('fs_target' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.target_username, event_payload.target_frequency = self._get_target_and_freq_from_data(update.callback_query.data)
          event_payload.target_frequency = int(event_payload.target_frequency)
          message_fsm.handle_internal_event(fsm.StateEvent.eSightUserInput, event_payload)
        elif('fs_balance_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eBalanceMain)
        elif('sm_help_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eInstagramStoriesHelp)
        elif('fm_help_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eInstagramFollowersHelp)
        elif('sm_next_page' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.page_offset = self._get_page_offset_from_data(update.callback_query.data)
          message_fsm.handle_internal_event(fsm.StateEvent.eSightNext, event_payload)
        elif('sm_prev_page_' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.page_offset = self._get_page_offset_from_data(update.callback_query.data)
          message_fsm.handle_internal_event(fsm.StateEvent.eSightPrev, event_payload)
        elif('fm_next_page' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.page_offset = self._get_page_offset_from_data(update.callback_query.data)
          message_fsm.handle_internal_event(fsm.StateEvent.eSightNext, event_payload)
        elif('fm_prev_page_' in update.callback_query.data):
          event_payload = fsm.EventPayload()
          event_payload.page_offset = self._get_page_offset_from_data(update.callback_query.data)
          message_fsm.handle_internal_event(fsm.StateEvent.eSightPrev, event_payload)
        elif('back_btn' == update.callback_query.data):
          message_fsm.handle_event(fsm.StateEvent.eSightBack)
        elif(
          'sm_balance_fiat_deposit_btn' == update.callback_query.data or
          'im_likes_btn' == update.callback_query.data or
          'sm_referral_btn' == update.callback_query.data):
          await update.callback_query.answer(text=LanguageController().get_text(LanguageState().get_language(update.callback_query.from_user.id), 'ANN_DESC_2'), show_alert=True)
      else:
        logging.error(
          f'Message {update.callback_query.message.message_id} for user {update.callback_query.from_user.id} not found')
    else:
      logging.error(f'User {update.callback_query.from_user.id} not found')
      await self.send_message(LanguageController().get_text(LanguageState().get_language(update.callback_query.from_user.id), 'ANN_DESC_1'), update.callback_query.message.chat.id)

    await update.callback_query.answer()

  async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_messages = self.users_fsm_.get(update.message.from_user.id)

    # TODO: im done
    if None != user_messages:
      payload = fsm.EventPayload()
      payload.target_username = update.message.text.lower()

      try:
        payload.code = int(update.message.text)
        payload.amount = float(update.message.text)
        payload.amount = payload.amount / config.DIAMOND_EXCHANGE_RATE
      except Exception as error:
        valid_username = self._validate_username(payload.target_username)

        if False is valid_username:
          payload.target_username = None

      if None is payload.target_username:
        payload.target_username = self._get_target_from_url(update.message.text)
        valid_username = self._validate_username(payload.target_username)

        if False is valid_username:
          payload.target_username = None

      for message in reversed(user_messages):
        error = user_messages[message].handle_internal_event(fsm.StateEvent.eSightUserInput, payload)

        if fsm.StateError.eOK == error:
          break

    try:
      await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    except Exception as e:
      logging.error('Failed to delete message:', e)

  async def send_message(self, text, chat_id) -> None:
    await self.application_.bot.send_message(
      chat_id = chat_id,
      text = text,
      parse_mode = 'Markdown')

  async def handle_widget_update(self, control_message : widget.ControlMessage) -> None:
    logging.info(f'handle_widget_update, message_id: {control_message.message_id}')
    updated_message = None

    if(0 < len(control_message.media)):
      await self.application_.bot.delete_message(
        chat_id = self.users_chat_[control_message.message_id],
        message_id = control_message.message_id)

      await self.application_.bot.send_photo(
        chat_id = self.users_chat_[control_message.message_id],
        caption = control_message.text,
        photo = open(config.LOGO_PHOTO_URI, 'rb'),
        parse_mode = 'Markdown')

      chunks = [control_message.media[i:i + 10] for i in range(0, len(control_message.media), 10)]
      for chunk in chunks:
        await self.application_.bot.send_media_group(
          chat_id = self.users_chat_[control_message.message_id],
          media = chunk,
          parse_mode = 'Markdown')

      updated_message = await self.application_.bot.send_photo(
        caption = control_message.text,
        chat_id = self.users_chat_[control_message.message_id],
        photo = open(config.LOGO_PHOTO_URI, 'rb'),
        parse_mode = 'Markdown')
    elif(0 < len(control_message.follower_info_in) or 0 < len(control_message.follower_info_out)):
      await self.application_.bot.delete_message(
        chat_id = self.users_chat_[control_message.message_id],
        message_id = control_message.message_id)

      if None != control_message.follower_image:
        await self.application_.bot.send_document(
          chat_id = self.users_chat_[control_message.message_id],
          caption = control_message.text,
          document = open(control_message.follower_image, 'rb'),
          parse_mode = 'Markdown')

      if None != control_message.follower_pdf:
        await self.application_.bot.send_document(
          chat_id = self.users_chat_[control_message.message_id],
          caption = control_message.text,
          document = open(control_message.follower_pdf, 'rb'),
          parse_mode = 'Markdown')

      updated_message = await self.application_.bot.send_photo(
        chat_id = self.users_chat_[control_message.message_id],
        photo = open(config.LOGO_PHOTO_URI, 'rb'),
        parse_mode = 'Markdown')
    else:
      await self.application_.bot.edit_message_caption(
        chat_id=self.users_chat_[control_message.message_id],
        message_id=control_message.message_id,
        caption=control_message.text,
        reply_markup=InlineKeyboardMarkup(control_message.keyboard),
        parse_mode = 'Markdown')

    if(None != updated_message):
      self.users_fsm_[control_message.user_id][updated_message.message_id] = self.users_fsm_[control_message.user_id][control_message.message_id]
      control_message.event_callback_updater(self.users_fsm_[control_message.user_id][updated_message.message_id].handle_event)
      del self.users_fsm_[control_message.user_id][control_message.message_id]

      control_message.message_id_updater(updated_message.message_id)
      self.users_chat_[updated_message.message_id] = self.users_chat_[control_message.message_id]
      del self.users_chat_[control_message.message_id]

      self.users_fsm_[control_message.user_id][updated_message.message_id].handle_event(fsm.StateEvent.eSightBack)

  async def _start_from_state(self, state : fsm.StateType, update : Update):

    if(update.message.from_user.id not in self.users_fsm_):
      self.users_fsm_[update.message.from_user.id] = {}

    sent_message = await update.message.reply_photo(caption=LanguageController().get_text(LanguageState().get_language(update.message.from_user.id), 'AUTH_DESC_3'), photo=open(config.LOGO_PHOTO_URI, 'rb'))

    bot_widget = widget.BotWidget(
      self.handle_widget_update,
      self.send_message,
      sent_message.message_id,
      update.message.from_user.id,
      update.effective_chat.id)
    user_data = self.user_db_client_.get_user(update.message.from_user.id)

    if(None is user_data):
      result = self.user_db_client_.create_user(
        UserDocument(
          update.message.from_user.id,
          update.effective_chat.id))

      if(None is result):
        raise Exception('Not able to register user')

      user_data = self.user_db_client_.get_user(update.message.from_user.id)

    LanguageState().update_language(user_data.user_id_, user_data.language_)
    self.users_fsm_[update.message.from_user.id][sent_message.message_id] = fsm.FSM(bot_widget, state)
    bot_widget.set_event_callback(self.users_fsm_[update.message.from_user.id][sent_message.message_id].handle_event)

    self.users_chat_[sent_message.message_id] = update.effective_chat.id

  def _restore_widgets(self):
    users = self.user_db_client_.get_all_users()

    for user in users:
      logging.info(f'RESTORED, chat-id: {user.chat_id_}, user-id: {user.user_id_}')
      self.restored_widgets_.append(widget.BotWidget(
        self.handle_widget_update,
        self.send_message,
        0,
        user.chat_id_,
        user.user_id_))
      LanguageState().update_language(user.user_id_, user.language_)

  def _get_target_from_data(self, data):
    pattern = r'(?:sm|fm|fg|fr|sr)_\w+_<(.+?)>_btn$'
    match = re.match(pattern, data)

    if match:
      target = match.group(1)
      return target

    return None

  def _get_page_offset_from_data(self, data):
    pattern = r'(?:sm|fm)_(?:next|prev)_page_(\d+)_btn'
    match = re.search(pattern, data)

    if match:
      counter = match.group(1)
      return int(counter)

    return 0

  def _get_target_and_range_from_data(self, data):
    pattern = r'fg_target_<(.+?)>_range_([a-zA-Z]+)_(?:followers|following)_btn'
    match = re.search(pattern, data)

    if match:
      return match.group(1), match.group(2)
    else:
      return None

  def _get_target_and_freq_from_data(self, data):
    pattern = r'\<([^>]*)\>.*\$(\d+)_'
    match = re.search(pattern, data)

    if match:
      return match.group(1), match.group(2)
    else:
      return None, None

  def _get_amount_from_data(self, data):
    pattern = r'(\d+)_btn'
    match = re.search(pattern, data)

    if match:
      counter = match.group(1)
      counter_float = None
      try:
        counter_float = float(counter)
      except Exception as error:
        counter_float = None
        logging.error(f'Unable to cast entered amount: {counter}')

      return counter_float

    return None

  def _get_target_from_url(self, url):
    pattern = r'instagram\.com/([^/?#&]+)'
    match = re.search(pattern, url)

    if match:
      return match.group(1)

    return None

  def _validate_username(self, username):
    try:
      if not 1 <= len(username) <= 30:
        return False
      if not re.match(r'^[a-zA-Z0-9._]+$', username):
        return False
      if '..' in username:
        return False
      if username.startswith('.') or username.endswith('.'):
        return False
    except Exception as error:
      return False

    return True

  def run(self):
    self.application_.run_polling(allowed_updates=Update.ALL_TYPES)
