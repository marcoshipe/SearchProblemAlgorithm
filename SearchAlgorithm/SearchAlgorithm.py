import abc
from typing import Collection, Type, List

from .Structures import State, Solution, PartialSolution, Node, FoundSolution
from .GenerateNeighbors import GenerateNeighbors
from .FrontierMode import FrontierMode
from .VisitedMode import VisitedMode
from .DebugMode import DebugMode


class SearchAlgorithm(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def find_solution(
            frontier_mode: Type[FrontierMode],
            visited_mode: Type[VisitedMode],
            generate_neighbors: Type[GenerateNeighbors],
            frontier_remove_repeated: bool,
            initial_state: State,
            goal_states: Collection[State]
    ) -> Solution:
        """ Find a solution to a Search Problem

        :param frontier_remove_repeated:
        :param generate_neighbors:
        :param visited_mode:
        :param frontier_mode:
        :param initial_state: The state in which the problem start
        :param goal_states: All the possible states that are valid solution to the problem
        :return: Return if the problem has a solution, and the path to the first solution found
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def find_all_solutions(
            frontier_mode: Type[FrontierMode],
            visited_mode: Type[VisitedMode],
            generate_neighbors: Type[GenerateNeighbors],
            debug_mode: DebugMode,
            frontier_remove_repeated: bool,
            initial_state: State,
            goal_states: Collection[State]
    ) -> int:
        pass

    @staticmethod
    def _find_solution_iteration(
            frontier_mode: Type[FrontierMode],
            visited_mode: Type[VisitedMode],
            generate_neighbors: Type[GenerateNeighbors],
            frontier_remove_repeated: bool,
            frontier: Collection[Node],
            visited_states: Collection[State],
            goal_states: Collection[State]
    ) -> PartialSolution:
        if not frontier:
            return PartialSolution(FoundSolution.NO, None)
        actual_node = frontier_mode.select_node(frontier)
        if SearchAlgorithm.is_goal(actual_node.state, goal_states):
            return PartialSolution(FoundSolution.YES, actual_node.path)
        else:
            visited_mode.add_visited(visited_states, actual_node.state)
            neighbors = generate_neighbors.generate_neighbors(actual_node, frontier, visited_states)
            if frontier_remove_repeated:
                SearchAlgorithm.remove_repeated_neighbors(neighbors, frontier, visited_states)
            frontier_mode.add_neighbors_to_frontier(frontier, neighbors)
            return PartialSolution(FoundSolution.NO_YET, None)

    @staticmethod
    def is_goal(actual_state: State, goal_states: Collection[State]) -> bool:
        return actual_state in goal_states

    @staticmethod
    def remove_repeated_neighbors(
            neighbors: List[Node],
            frontier: Collection[Node],
            visited_states: Collection[State]
    ) -> None:
        neighbors[:] = [neighbor for neighbor in neighbors if neighbor not in frontier and
                        neighbor.state not in visited_states]


class SearchAlgorithmIterative(SearchAlgorithm):
    @staticmethod
    def find_all_solutions(
        frontier_mode: Type[FrontierMode],
        visited_mode: Type[VisitedMode],
        generate_neighbors: Type[GenerateNeighbors],
        debug_mode: DebugMode,
        frontier_remove_repeated: bool,
        initial_state: State,
        goal_states: Collection[State]
    ) -> int:
        frontier = debug_mode.initialization(initial_state, frontier_mode)
        visited_states = visited_mode.create_visited()
        partial_solution = PartialSolution(FoundSolution.NO_YET, None)
        while not debug_mode.is_stop() and \
                (partial_solution.found_solution == FoundSolution.NO_YET or
                 partial_solution.found_solution == FoundSolution.YES):
            partial_solution = SearchAlgorithm._find_solution_iteration(
                frontier_mode, visited_mode, generate_neighbors, frontier_remove_repeated,
                frontier, visited_states, goal_states)
            debug_mode.after_iteration(len(frontier), partial_solution)
        amount_solutions = debug_mode.finalization(frontier)
        return amount_solutions

    @staticmethod
    def find_solution(
            frontier_mode: Type[FrontierMode],
            visited_mode: Type[VisitedMode],
            generate_neighbors: Type[GenerateNeighbors],
            frontier_remove_repeated: bool,
            initial_state: State,
            goal_states: Collection[State]
    ) -> Solution:
        initial_node = Node(initial_state, [], 0)
        frontier = frontier_mode.create_frontier()
        frontier_mode.add_neighbors_to_frontier(frontier, [initial_node])
        visited_states = visited_mode.create_visited()
        partial_solution = PartialSolution(FoundSolution.NO_YET, None)
        while partial_solution.found_solution == FoundSolution.NO_YET:
            partial_solution = SearchAlgorithm._find_solution_iteration(
                frontier_mode, visited_mode, generate_neighbors, frontier_remove_repeated,
                frontier, visited_states, goal_states)
        if partial_solution.found_solution == FoundSolution.YES:
            partial_solution.path.reverse()
        return Solution(partial_solution.found_solution == FoundSolution.YES, partial_solution.path)
