from __future__ import annotations
from abc import ABC, abstractmethod

class UserCardState(ABC):
    """
    The base UserCardState class.
    Implements status: [active, deactive]
    """

    def __init__(self, context) -> None:
        self.user_card = context
        
    @abstractmethod
    def activate_card(self) -> None:
        pass

    @abstractmethod
    def deactivate_card(self) -> None:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        return ''

"""
Define UserCard states
"""

class UserCardActive(UserCardState):
    def activate_card(self) -> None:
        print("The card is already activated")
    
    def deactivate_card(self) -> None:
        self.user_card.transition_to(UserCardDeactive)
        print("Card deactivated")

    def __repr__(self) -> str:
        return "active"

class UserCardDeactive(UserCardState):
    def activate_card(self) -> None:
        self.transition_to(UserCardActive)
        print("Card activated")

    def deactivate_card(self) -> None:
        print("The card is already deactivated")
    
    def __repr__(self) -> str:
        return "deactive"
