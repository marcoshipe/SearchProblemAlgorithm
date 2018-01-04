import abc
from typing import Collection, List

from .Structures import Node, State


class GenerateNeighbors(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def generate_neighbors(
            actual_node: Node,
            frontier: Collection[Node],
            visited_states: Collection[State]
    ) -> List[Node]:
        pass
