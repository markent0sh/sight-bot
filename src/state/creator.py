import os
import sys
import logging

import state.main as base_state
import state.settings as settings_state
import state.instagram as ig_state
import state.instagram_story as ig_story_state
import state.instagram_follower as ig_follower_state

sys.path.append(
  os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../'))

from fsm import State, StateType

def create_state(state_type : StateType) -> State:
  state = None

  if(0):
    pass
  elif(StateType.eSightMain is state_type):
    state = base_state.setup_sight_main_state()
  elif(StateType.eInstagramMain is state_type):
    state = ig_state.setup_instagram_main_state()
  elif(StateType.eInstagramStoriesMain is state_type):
    state = ig_story_state.setup_instagram_stories_main_state()
  elif(StateType.eInstagramStoriesRemoveTarget is state_type):
    state = ig_story_state.setup_instagram_stories_remove_target_state()
  elif(StateType.eInstagramStoriesGetTargetData is state_type):
    state = ig_story_state.setup_instagram_stories_get_target_data_state()
  elif(StateType.eInstagramStoriesSetNewTarget is state_type):
    state = ig_story_state.setup_instagram_stories_set_new_target_state()
  elif(StateType.eInstagramStoriesSetNewTargetFrequency is state_type):
    state = ig_story_state.setup_instagram_stories_set_new_target_frequency_state()
  elif(StateType.eInstagramStoriesHelp is state_type):
    state = ig_story_state.setup_instagram_stories_help_state()
  elif(StateType.eInstagramFollowersHelp is state_type):
    state = ig_follower_state.setup_instagram_followers_help_state()
  elif(StateType.eInstagramFollowersMain is state_type):
    state = ig_follower_state.setup_instagram_followers_main_state()
  elif(StateType.eInstagramFollowersRemoveTarget is state_type):
    state = ig_follower_state.setup_instagram_followers_remove_target_state()
  elif(StateType.eInstagramFollowersModifyTarget is state_type):
    state = ig_follower_state.setup_instagram_followers_modify_target_state()
  elif(StateType.eInstagramFollowersGetTargetData is state_type):
    state = ig_follower_state.setup_instagram_followers_get_target_data_state()
  elif(StateType.eInstagramFollowersSetNewTarget is state_type):
    state = ig_follower_state.setup_instagram_followers_set_new_target_state()
  elif(StateType.eInstagramFollowersSetNewTargetFrequency is state_type):
    state = ig_follower_state.setup_instagram_followers_set_new_target_frequency_state()
  elif(StateType.eSettingsMain is state_type):
    state = settings_state.setup_settings_main_state()
  elif(StateType.eSettingsLanguageMain is state_type):
    state = settings_state.setup_settings_lang_main_state()
  elif(StateType.eSettingsNotifyMain is state_type):
    state = settings_state.setup_settings_notify_main_state()
  elif(StateType.eSettingsReferralsMain is state_type):
    state = settings_state.setup_settings_referral_main_state()
  elif(StateType.eSettingsReferralsConnect is state_type):
    state = settings_state.setup_settings_referral_connect_state()
  elif(StateType.eBalanceMain is state_type):
    state = settings_state.setup_settings_balance_main_state()
  elif(StateType.eBalanceDepositMain is state_type):
    state = settings_state.setup_settings_balance_deposit_main_state()
  else:
    logging.error(f'create_state error, not found state creator for ID: {state_type}')

  return state
