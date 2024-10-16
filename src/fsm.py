from enum import Enum
import logging

class StateType(Enum):
  eIdle = -1,
  eSightMain = 0,
  eInstagramMain = 10,
  eInstagramStoriesMain = 11,
  eInstagramStoriesRemoveTarget = 12,
  eInstagramStoriesGetTargetData = 13,
  eInstagramStoriesSetNewTarget = 14,
  eInstagramStoriesHelp = 15,
  eInstagramStoriesSetNewTargetFrequency = 16,
  eInstagramFollowersMain = 50,
  eInstagramFollowersRemoveTarget = 51,
  eInstagramFollowersModifyTarget = 52,
  eInstagramFollowersGetTargetData = 53,
  eInstagramFollowersSetNewTarget = 54,
  eInstagramFollowersHelp = 55,
  eInstagramFollowersSetNewTargetFrequency = 56,
  eBalanceMain = 100,
  eBalanceDepositMain = 101,
  eSettingsMain = 150,
  eSettingsLanguageMain = 151,
  eSettingsNotifyMain = 160,
  eSettingsReferralsMain = 170,
  eSettingsReferralsConnect = 171

class StateEvent(Enum):
  eSightMain = 0,
  eSightUserInput = 1,
  eSightUserInputRequest = 4,
  eSightNext = 2,
  eSightPrev = 3,
  eSightBack = 9999,
  eInstagramMain = 10,
  eInstagramStoriesMain = 11,
  eInstagramStoriesRemoveTarget = 12,
  eInstagramStoriesGetTargetData = 13,
  eInstagramStoriesSetNewTarget = 14,
  eInstagramStoriesRemoveTargetConf = 15,
  eInstagramStoriesHelp = 16,
  eInstagramStoriesSetNewTargetFrequency = 17,
  eInstagramFollowersMain = 50,
  eInstagramFollowersRemoveTarget = 51,
  eInstagramFollowersModifyTarget = 52,
  eInstagramFollowersGetTargetData = 53,
  eInstagramFollowersSetNewTarget = 54,
  eInstagramFollowersRemoveTargetConf = 55,
  eInstagramFollowersHelp = 56,
  eInstagramFollowersSetNewTargetFrequency = 57,
  eBalanceMain = 100,
  eBalanceDepositMain = 101,
  eSettingsMain = 150,
  eSettingsLanguageMain = 151,
  eSettingsLanguageRussian = 152,
  eSettingsLanguageEnglish = 153,
  eSettingsNotifyMain = 160,
  eSettingsNotifyToggleStories = 161,
  eSettingsNotifyToggleFollowers = 162,
  eSettingsReferralsMain = 170,
  eSettingsReferralsConnect = 171

class EventPayload:
  def __init__(self) -> None:
    self.target_username = None
    self.target_frequency = None
    self.page_offset = 0
    self.amount = None
    self.code = None
    self.follower_track = None
    self.following_track = None
    self.range = None
    self.pop_on_set = False

class StateError(Enum):
  eOK = 0,
  eNOK = 1

class State:
  def __init__(
      self,
      set_state_call = None,
      quit_state_call = None,
      pop_event_call = None,
      handle_event_call = None) -> None:
    self.set_state_call_ = set_state_call
    self.quit_state_call_ = quit_state_call
    self.pop_event_call_ = pop_event_call
    self.handle_event_call_ = handle_event_call

  def set_state(self, widget_delegate, payload : EventPayload) -> StateError:
    if None != self.set_state_call_:
      return self.set_state_call_(widget_delegate, payload)

    return StateError.eNOK

  def quit_state(self, widget_delegate) -> StateError:
    if None != self.set_state_call_:
      return self.quit_state_call_(widget_delegate)

    return StateError.eNOK

  def pop_event(self, widget_delegate, payload : EventPayload) -> StateError:
    if None != self.pop_event_call_:
      return self.pop_event_call_(widget_delegate, payload)

    return StateError.eNOK

  def handle_event(self, widget_delegate, event : StateEvent, payload : EventPayload) -> StateError:
    if None != self.handle_event_call_:
      return self.handle_event_call_(widget_delegate, event, payload)

    return StateError.eNOK

class FSM:
  def __init__(self, widget_delegate, init_state : StateType = StateType.eIdle) -> None:
    self.widget_delegate_ = widget_delegate
    self.active_state_ = self._setup_idle_state()
    self.active_state_type_ = init_state
    self.previous_states_type_ = [StateType.eSightMain]
    self._update_state(self.active_state_type_, True, EventPayload())

  def handle_internal_event(self, event : StateEvent, payload : EventPayload) -> StateError:
    logging.info(f'handle_internal_event, event: {event}')
    return self.active_state_.handle_event(self.widget_delegate_, event, payload)

  def handle_event(self, event : StateEvent, payload : EventPayload = EventPayload()) -> StateError:
    logging.info(f'handle_event, event: {event}')

    is_back = False
    state = StateType.eIdle

    if(0):
      logging.warning('Magic is real?')
    elif(StateEvent.eSightMain is event):

      if(StateType.eIdle is self.active_state_type_):
        state = StateType.eSightMain

    elif(StateEvent.eBalanceMain is event):

      if(0):
        pass
      elif(StateType.eSightMain is self.active_state_type_):
        state = StateType.eBalanceMain
      elif(StateType.eSettingsMain is self.active_state_type_):
        state = StateType.eBalanceMain
      elif(StateType.eInstagramStoriesSetNewTargetFrequency is self.active_state_type_):
        state = StateType.eBalanceMain
      elif(StateType.eInstagramFollowersSetNewTargetFrequency is self.active_state_type_):
        state = StateType.eBalanceMain
      elif(StateType.eInstagramStoriesGetTargetData is self.active_state_type_):
        state = StateType.eBalanceMain
      elif(StateType.eInstagramFollowersGetTargetData is self.active_state_type_):
        state = StateType.eBalanceMain

    elif(StateEvent.eBalanceDepositMain is event):

      if(StateType.eBalanceMain is self.active_state_type_):
        state = StateType.eBalanceDepositMain

    elif(StateEvent.eInstagramMain is event):

      if(StateType.eSightMain is self.active_state_type_):
        state = StateType.eInstagramMain

    elif(StateEvent.eInstagramStoriesMain is event):

      if(StateType.eInstagramMain is self.active_state_type_):
        state = StateType.eInstagramStoriesMain

    elif(StateEvent.eInstagramStoriesRemoveTarget is event):

      if(StateType.eInstagramStoriesMain is self.active_state_type_):
        state = StateType.eInstagramStoriesRemoveTarget

    elif(StateEvent.eInstagramStoriesGetTargetData is event):

      if(StateType.eInstagramStoriesMain is self.active_state_type_):
        state = StateType.eInstagramStoriesGetTargetData

    elif(StateEvent.eInstagramStoriesSetNewTarget is event):

      if(StateType.eInstagramStoriesMain is self.active_state_type_):
        state = StateType.eInstagramStoriesSetNewTarget

    elif(StateEvent.eInstagramStoriesSetNewTargetFrequency is event):

      if(StateType.eInstagramStoriesSetNewTarget is self.active_state_type_):
        state = StateType.eInstagramStoriesSetNewTargetFrequency

    elif(StateEvent.eInstagramFollowersMain is event):

      if(StateType.eInstagramMain is self.active_state_type_):
        state = StateType.eInstagramFollowersMain

    elif(StateEvent.eInstagramFollowersRemoveTarget is event):

      if(StateType.eInstagramFollowersMain is self.active_state_type_):
        state = StateType.eInstagramFollowersRemoveTarget

    # elif(StateEvent.eInstagramFollowersModifyTarget is event):

    #   if(StateType.eInstagramFollowersMain is self.active_state_type_):
    #     state = StateType.eInstagramFollowersModifyTarget

    elif(StateEvent.eInstagramFollowersGetTargetData is event):

      if(StateType.eInstagramFollowersMain is self.active_state_type_):
        state = StateType.eInstagramFollowersGetTargetData

    elif(StateEvent.eInstagramFollowersSetNewTarget is event):

      if(StateType.eInstagramFollowersMain is self.active_state_type_):
        state = StateType.eInstagramFollowersSetNewTarget

    elif(StateEvent.eInstagramFollowersSetNewTargetFrequency is event):

      if(StateType.eInstagramFollowersSetNewTarget is self.active_state_type_):
        state = StateType.eInstagramFollowersSetNewTargetFrequency

    elif(StateEvent.eSettingsMain is event):

      if(StateType.eSightMain is self.active_state_type_):
        state = StateType.eSettingsMain

    elif(StateEvent.eSettingsLanguageMain is event):

      if(StateType.eSettingsMain is self.active_state_type_):
        state = StateType.eSettingsLanguageMain

    elif(StateEvent.eSettingsNotifyMain is event):

      if(StateType.eSettingsMain is self.active_state_type_):
        state = StateType.eSettingsNotifyMain

    elif(StateEvent.eSettingsReferralsMain is event):

      if(StateType.eSettingsMain is self.active_state_type_):
        state = StateType.eSettingsReferralsMain

    elif(StateEvent.eSettingsReferralsConnect is event):

      if(StateType.eSettingsReferralsMain is self.active_state_type_):
        state = StateType.eSettingsReferralsConnect

    elif(StateEvent.eInstagramFollowersHelp is event):

      if(StateType.eInstagramFollowersMain is self.active_state_type_):
        state = StateType.eInstagramFollowersHelp

    elif(StateEvent.eInstagramStoriesHelp is event):

      if(StateType.eInstagramStoriesMain is self.active_state_type_):
        state = StateType.eInstagramStoriesHelp

    elif(StateEvent.eSightBack is event):

      if(len(self.previous_states_type_) > 0):
        state = self.previous_states_type_.pop()
        is_back = True

    else:
      logging.error('Unknown event')

    return self._update_state(state, is_back, payload)

  def _update_state(self, state_type : StateType, is_back : bool, payload : EventPayload) -> StateError:
    import state.creator as state_creator

    logging.info(f'state: {state_type}')
    error = StateError.eNOK

    if(StateType.eIdle is state_type):
      logging.error('Idle is not a valid state - ignoring')
      return error

    error = self.active_state_.quit_state(self.widget_delegate_)

    if(StateError.eOK != error):
      return error

    state = state_creator.create_state(state_type)

    if(None != state):
      error = state.set_state(self.widget_delegate_, payload)

      if(StateError.eOK != error):
        return error

      self.active_state_ = state

      if(False == is_back):
        self.previous_states_type_.append(self.active_state_type_)

      self.active_state_type_ = state_type
      self.active_state_.pop_event(self.widget_delegate_, payload)

    return error

  def _setup_idle_state(self) -> State:
    def set_state(widget_delegate, payload : EventPayload) -> StateError:
      logging.info('Idle :: set_state')
      return StateError.eOK

    def quit_state(widget_delegate) -> StateError:
      logging.info('Idle :: quit_state')
      return StateError.eOK

    return State(set_state, quit_state)

class StubWidget:
  def __init__(self) -> None:
    pass

  def do_something(self):
    logging.info("StubWidget::do_something")

if(__name__ == "__main__"):
  widget = StubWidget()
  fsm = FSM(widget)

  error = fsm.handle_event(StateEvent.eSightMain)
  logging.info(f'handle_event result: {error}')
