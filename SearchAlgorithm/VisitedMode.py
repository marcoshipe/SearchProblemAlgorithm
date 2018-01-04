import abc
from typing import Collection, List

from .Structures import State


class VisitedMode(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def create_visited() -> Collection[State]:
        pass

    @staticmethod
    @abc.abstractmethod
    def add_visited(visited_states: Collection[State], actual_state: State) -> None:
        pass


class VisitedModeList(VisitedMode):
    @staticmethod
    def create_visited() -> List[State]:
        return []

    @staticmethod
    def add_visited(visited_states: List[State], actual_state: State) -> None:
        visited_states.append(actual_state)


class VisitedModeNone(VisitedMode):
    @staticmethod
    def create_visited() -> List:
        return []

    @staticmethod
    def add_visited(visited_states, actual_state):
        pass
