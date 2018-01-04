import abc
from typing import Collection, List

from .Structures import Node


class FrontierMode(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def create_frontier() -> Collection[Node]:
        pass

    @staticmethod
    @abc.abstractmethod
    def select_node(frontier: Collection[Node]) -> Node:
        pass

    @staticmethod
    @abc.abstractmethod
    def add_neighbors_to_frontier(frontier: Collection[Node], neighbors: List[Node]):
        pass


class FrontierModeDFS(FrontierMode):
    @staticmethod
    def create_frontier() -> List[Node]:
        return []

    @staticmethod
    def select_node(frontier: List[Node]):
        return frontier.pop()

    @staticmethod
    def add_neighbors_to_frontier(frontier: List[Node], neighbors: List[Node]):
        frontier.extend(neighbors)
