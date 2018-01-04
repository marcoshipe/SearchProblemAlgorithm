from typing import Container, List

import numpy as np

from SearchAlgorithm.Structures import State, Node
from SearchAlgorithm.FrontierMode import FrontierModeDFS
from SearchAlgorithm.VisitedMode import VisitedModeNone
from SearchAlgorithm.GenerateNeighbors import GenerateNeighbors
from SearchAlgorithm.DebugMode import DebugMode
from SearchAlgorithm.SearchAlgorithm import SearchAlgorithmIterative


class SenkuState(State):
    def __init__(self, cost: int, board: np.array):
        self.cost = cost
        self.board = board

    def __eq__(self, other):
        if self.cost != other.cost:
            return False
        return np.array_equal(self.board, other.board)


class GenerateNeighborsSenku(GenerateNeighbors):
    @staticmethod
    def generate_neighbors(
            actual_node: Node[SenkuState],
            frontier: Container[Node[SenkuState]],
            visited_states: Container[SenkuState]
    ) -> List[Node[SenkuState]]:
        neighbors = []
        for row in range(len(actual_node.state.board)):
            for column in range(len(actual_node.state.board[row])):
                if actual_node.state.board[row][column] == 'X':
                    if row >= 2 and actual_node.state.board[row - 2][column] == '-' \
                            and actual_node.state.board[row - 1][column] == 'X':
                        # Comer a arriba
                        nuevo_estado = SenkuState(actual_node.state.cost + 1, actual_node.state.board.copy())
                        nuevo_estado.board[row][column] = '-'
                        nuevo_estado.board[row - 1][column] = '-'
                        nuevo_estado.board[row - 2][column] = 'X'
                        nuevo_camino = actual_node.path[:]
                        nuevo_camino.append('[{}-{}] a [{}-{}]'.
                                            format(row, column, row - 2, column))
                        neighbors.append(Node(nuevo_estado, nuevo_camino, actual_node.cost + 1))
                    if row + 2 < len(actual_node.state.board) and actual_node.state.board[row + 2][column] == '-' \
                            and actual_node.state.board[row + 1][column] == 'X':
                        # Comer a abajo
                        nuevo_estado = SenkuState(actual_node.state.cost + 1, actual_node.state.board.copy())
                        nuevo_estado.board[row][column] = '-'
                        nuevo_estado.board[row + 1][column] = '-'
                        nuevo_estado.board[row + 2][column] = 'X'
                        nuevo_camino = actual_node.path[:]
                        nuevo_camino.append('[{}-{}] a [{}-{}]'
                                            .format(row, column, row + 2, column))
                        neighbors.append(Node(nuevo_estado, nuevo_camino, actual_node.cost + 1))
                    if column >= 2 and actual_node.state.board[row][column - 2] == '-' \
                            and actual_node.state.board[row][column - 1] == 'X':
                        # Comer a izquierda
                        nuevo_estado = SenkuState(actual_node.state.cost + 1, actual_node.state.board.copy())
                        nuevo_estado.board[row][column] = '-'
                        nuevo_estado.board[row][column - 1] = '-'
                        nuevo_estado.board[row][column - 2] = 'X'
                        nuevo_camino = actual_node.path[:]
                        nuevo_camino.append('[{}-{}] a [{}-{}]'
                                            .format(row, column, row, column - 2))
                        neighbors.append(Node(nuevo_estado, nuevo_camino, actual_node.cost + 1))
                    if column + 2 < len(actual_node.state.board[row]) \
                            and actual_node.state.board[row][column + 2] == '-' \
                            and actual_node.state.board[row][column + 1] == 'X':
                        # Comer a derecha
                        nuevo_estado = SenkuState(actual_node.state.cost + 1, actual_node.state.board.copy())
                        nuevo_estado.board[row][column] = '-'
                        nuevo_estado.board[row][column + 1] = '-'
                        nuevo_estado.board[row][column + 2] = 'X'
                        nuevo_camino = actual_node.path[:]
                        nuevo_camino.append('[{}-{}] a [{}-{}]'
                                            .format(row, column, row, column + 2))
                        neighbors.append(Node(nuevo_estado, nuevo_camino, actual_node.cost + 1))
        return neighbors


def main():
    initial_state = SenkuState(
        0,
        np.array([
            [' ', ' ', 'X', 'X', 'X', ' ', ' '],
            [' ', ' ', 'X', 'X', 'X', ' ', ' '],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', '-', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
            [' ', ' ', 'X', 'X', 'X', ' ', ' '],
            [' ', ' ', 'X', 'X', 'X', ' ', ' ']
        ])
    )
    goal_states = [
        SenkuState(
            31,
            np.array([
                [' ', ' ', '-', '-', '-', ' ', ' '],
                [' ', ' ', '-', '-', '-', ' ', ' '],
                ['-', '-', '-', '-', '-', '-', '-'],
                ['-', '-', '-', 'X', '-', '-', '-'],
                ['-', '-', '-', '-', '-', '-', '-'],
                [' ', ' ', '-', '-', '-', ' ', ' '],
                [' ', ' ', '-', '-', '-', ' ', ' ']
            ])
        )
    ]

    debug_mode = DebugMode(
        show_amount_solutions=True,
        show_amount_nodes_visited=True,
        show_max_size_frontier=True,
        show_actual_runtime=True,
        show_total_runtime=True,
        show_pretty_time=True,
        secs_amount_decimals=0,
        thousand_separator='.',
        show_every_x_solutions=0,
        show_every_x_nodes_visited=0,
        show_every_x_secs=10,
        save_file_path='SenkuSave2.p'
    )

    solution = SearchAlgorithmIterative.find_all_solutions(
        frontier_mode=FrontierModeDFS,
        visited_mode=VisitedModeNone,
        generate_neighbors=GenerateNeighborsSenku,
        debug_mode=debug_mode,
        frontier_remove_repeated=False,
        initial_state=initial_state,
        goal_states=goal_states
    )
    print(solution)


if __name__ == '__main__':
    main()
