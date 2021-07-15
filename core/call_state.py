from abc import ABC
from django.db import models

class CallStateChoices(models.TextChoices):
    IDLE = 'IDLE'
    RECEIVING = 'RECEIVING'
    CALLING = 'CALLING'
    ONCALL = 'ONCALL'

class BaseCallerState(ABC):
    """
    Base state with all possible caller states.
    """
    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, profile) -> None:
        self._profile = profile

    
    def make_call(self, other_person) -> None:
        """
        Method to make call if both parties are available
        """
        pass

    
    def receive_call(self, other_person) -> None:
        """
        Method to recieve call if both parties are available
        """
        pass

    
    def end_call(self) -> None:
        """
        Method to end call for both parties
        """
        pass
    
    
    def accept_call(self) -> None:
        """
        Method to accept call from other party
        """
        pass

    
    def has_accepted_call(self) -> None:
        """
        Method to enter call after other party accepts
        """
        pass


class IDLE(BaseCallerState):
    def receive_call(self, other_person) -> None:
        self.profile.set_state(CallStateChoices.RECEIVING)
        self.profile.other_caller = other_person
        self.profile.save()
    
    def make_call(self, other_person) -> None:
        self.profile.set_state(CallStateChoices.CALLING)
        other_person.get_state().receive_call(self.profile)
        self.profile.other_caller = other_person
        self.profile.save()


class RECEIVING(BaseCallerState):
    def accept_call(self) -> None:
        self.profile.set_state(CallStateChoices.ONCALL)
        self.profile.other_caller.get_state().has_accepted_call()
    
    def end_call(self, other_source: bool) -> None:
        self.profile.set_state(CallStateChoices.IDLE)
        if not other_source:
            self.profile.other_caller.get_state().end_call(other_source=True)
        self.profile.other_caller = None
        self.profile.save()


class CALLING(BaseCallerState):
    def has_accepted_call(self) -> None:
        self.profile.set_state(CallStateChoices.ONCALL)
    
    def end_call(self, other_source:bool = False) -> None:
        self.profile.set_state(CallStateChoices.IDLE)
        if not other_source:
            self.profile.other_caller.get_state().end_call(other_source=True)
        self.profile.other_caller = None
        self.profile.save()


class ONCALL(BaseCallerState):    
    def end_call(self, other_source: bool) -> None:
        self.profile.set_state(CallStateChoices.IDLE)
        if not other_source:
            self.profile.other_caller.get_state().end_call(other_source=True)
        self.profile.other_caller = None
        self.profile.save()


choice_to_class = {
    CallStateChoices.IDLE: IDLE,
    CallStateChoices.RECEIVING: RECEIVING,
    CallStateChoices.CALLING: CALLING,
    CallStateChoices.ONCALL: ONCALL,
}