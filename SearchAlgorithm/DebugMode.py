import os
import pickle
import threading

import time
from typing import Type, Collection

from .Structures import Node, State, FoundSolution
from .FrontierMode import FrontierMode

STOP = False


class DebugMode:
    def __init__(
            self,
            show_amount_solutions: bool,
            show_amount_nodes_visited: bool,
            show_max_size_frontier: bool,
            show_actual_runtime: bool,
            show_total_runtime: bool,
            show_pretty_time: bool,
            secs_amount_decimals: int,
            thousand_separator: str = '',
            show_every_x_solutions: int = 0,
            show_every_x_nodes_visited: int = 0,
            show_every_x_secs: int = 0,
            save_file_path: str = None
    ):
        self.show_amount_solutions = show_amount_solutions
        self.show_amount_nodes_visited = show_amount_nodes_visited
        self.show_max_size_frontier = show_max_size_frontier
        self.show_actual_runtime = show_actual_runtime
        self.show_total_runtime = show_total_runtime
        self.show_pretty_time = show_pretty_time
        if secs_amount_decimals == 0:
            self.time_amount_decimals = None
        else:
            self.time_amount_decimals = secs_amount_decimals
        self.thousand_separator = thousand_separator
        self.show_every_x_solutions = show_every_x_solutions
        self.show_every_x_nodes_visited = show_every_x_nodes_visited
        self.thread_show = None
        if show_every_x_secs != 0:
            self.thread_show = threading.Thread(
                target=self._show_every_x_seconds,
                args=(show_every_x_secs,))
            self.thread_show.start()
        self.save_file_path = save_file_path
        self.amount_solutions = 0
        self.max_size_frontier = 0
        self.amount_nodes_visited = 0
        self.t0_actual_runtime = 0
        self.t0_total_runtime = 0
        self.thread_quit = threading.Thread(target=self._quit_program)
        self.thread_quit.start()

    def initialization(self, initial_state: State, frontier_mode: Type[FrontierMode])\
            -> Collection[Node]:
        if os.path.isfile(self.save_file_path):
            (self.amount_solutions, self.amount_nodes_visited, frontier,
             self.max_size_frontier, self.t0_total_runtime) = \
                pickle.load(open(self.save_file_path, "rb"))
        else:
            initial_node = Node(initial_state, [], 0)
            frontier = frontier_mode.create_frontier()
            frontier_mode.add_neighbors_to_frontier(frontier, [initial_node])
        self.t0_actual_runtime = time.perf_counter()
        return frontier

    def after_iteration(self, frontier_size, partial_solution):
        showed = False
        if frontier_size > self.max_size_frontier:
            self.max_size_frontier = frontier_size
        self.amount_nodes_visited += 1
        if self.show_every_x_nodes_visited != 0 and \
                self.amount_nodes_visited % self.show_every_x_nodes_visited == 0:
            showed = True
            self._show_debug()
        if partial_solution.found_solution == FoundSolution.YES:
            self.amount_solutions += 1
            if not showed and self.show_every_x_solutions != 0 and \
                    self.amount_solutions % self.show_every_x_solutions == 0:
                self._show_debug()

    def finalization(self, frontier):
        t_actual_runtime = time.perf_counter() - self.t0_actual_runtime
        if STOP:
            data = (self.amount_solutions, self.amount_nodes_visited, frontier,
                    self.max_size_frontier, t_actual_runtime + self.t0_total_runtime)
            pickle.dump(data, open(self.save_file_path, "wb"))
        self._show_debug()
        if self.thread_show:
            self.thread_show.join()
        self.thread_quit.join()
        return self.amount_solutions

    @staticmethod
    def is_stop():
        return STOP

    def _show_every_x_seconds(self, secs):
        while STOP is False:
            time.sleep(secs)
            self._show_debug()

    @staticmethod
    def _quit_program():
        global STOP
        while STOP is False:
            inp = input("PRESS 'A' KEY AND ENTER TO EXIT THE PROGRAM\n")
            if inp is 'a':
                STOP = True

    def _show_debug(self):
        if self.show_amount_solutions:
            print('amount solutions: ' +
                  format(self.amount_solutions, ',').replace(',', self.thousand_separator))
        if self.show_amount_nodes_visited:
            print('amount nodes visited: ' +
                  format(self.amount_nodes_visited, ',').replace(',', self.thousand_separator))
        if self.show_max_size_frontier:
            print('frontier max size: ' +
                  format(self.max_size_frontier, ',').replace(',', self.thousand_separator))
        if self.show_actual_runtime:
            time_float = time.perf_counter() - self.t0_actual_runtime
            print('actual runtime: ' + self._format_time(time_float))
        if self.show_total_runtime:
            time_float = time.perf_counter() - self.t0_actual_runtime + self.t0_total_runtime
            print('total runtime: ' + self._format_time(time_float))
        print()

    def _format_time(self, time_int):
        if not self.show_pretty_time:
            time_r = round(time_int, self.time_amount_decimals)
            return format(time_r, ',').replace(',', self.thousand_separator) + ' secs'
        time_str = ''
        secs = round(time_int % 60, self.time_amount_decimals)
        if time_int >= 60:
            mins = int((time_int / 60) % 60)
            if time_int >= 3600:
                hours = int((time_int / 3600) % 24)
                if time_int >= 86400:
                    days = int(time_int / 86400)
                    time_str += str(days) + ' days, '
                time_str += str(hours) + ' hours, '
            time_str += str(mins) + ' mins, '
        return time_str + str(secs) + ' secs'
