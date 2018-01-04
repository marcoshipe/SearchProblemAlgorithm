import abc
from enum import Enum, auto
from typing import NamedTuple, List, Union, TypeVar, Generic


class State(abc.ABC):
    @abc.abstractmethod
    def __eq__(self, other):
        pass


State_T = TypeVar('State_T', bound=State)


class Node(Generic[State_T]):
    def __init__(self, state: State_T, path: List[str], cost: int):
        self.state: State_T = state
        self.path: List[str] = path
        self.cost: int = cost


class Solution(NamedTuple):
    has_solution: bool
    path: Union[List[str], None]


class FoundSolution(Enum):
    YES = auto()
    NO = auto()
    NO_YET = auto()


class PartialSolution(NamedTuple):
    found_solution: FoundSolution
    path: Union[List[str], None]
