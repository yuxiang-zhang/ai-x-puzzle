import logging
from abc import ABC, abstractmethod
from queue import PriorityQueue
from time import time
from heuristics import Heuristic, H0

logging_disabled = False

class SearchStrategy(ABC):
    def __init__(self, h_func:Heuristic = H0()):
        # heuristic function
        self._heuristic = h_func
        # pq sorted by f(n)
        self._open_list = PriorityQueue()
        # visited_state -> parent_state
        self._closed_list = {}
        # logger to be defined in subclasses
        logging.basicConfig(filename='out/dump.log', filemode='w', format='%(message)s', level='INFO')
        self._search_logger = logging.getLogger()
        self._sol_logger = logging.getLogger()
        self._runtime = 0
        super().__init__()

    @abstractmethod
    def evaluation_function(self, new_state):
        """Evaluation function to be used to get/estimate the cost for a path. """
        pass

    @abstractmethod
    def search(self, puzzle):
        """Core search strategy to be used to get the solution. """
        pass

    def update_open_list(self, successors):
        """
        Insert computed successors one by one into the open_list.
        When inserting, don't check if the state already in open_list, directly put in open_list;
        for duplicates, check in closed list whenever popping from open list.
        :return:
        """
        for to_state in successors:
            if to_state not in self._closed_list:
                self._open_list.put((sum(self.evaluation_function(to_state)), to_state))

    def get_best_next_state(self, curr_state):
        """Pop next minimal cost state from open list"""
        while self._open_list.not_empty:
            cost, state = self._open_list.get()
            if state not in self._closed_list:
                self._closed_list[state] = curr_state
                search_file_entry = ' '.join(map(str, (cost, *self.evaluation_function(state), state)))
                self._search_logger.info(search_file_entry)
                return cost, state
        return None # empty open list

    def retrieve_solution(self, last_state):
        state = last_state
        cost = state.path_cost
        stack = []
        while state.from_state is not None:
            sol_file_entry = ' '.join(map(str, (state.last_moved_tile, state.path_cost - state.from_state.path_cost, state)))
            stack.append(sol_file_entry)
            state = state.from_state

        sol_file_entry = ' '.join(map(str, (state.last_moved_tile, state.path_cost, state)))
        stack.append(sol_file_entry)

        while stack:
            self._sol_logger.info(stack.pop())
        self._sol_logger.info('{} {}'.format(cost, self._runtime))


class UCS(SearchStrategy, ABC):
    def __init__(self, h_func:Heuristic = H0(), puzzle_num=0):
        super().__init__(h_func)
        if not logging_disabled:
            filename = 'out/{}_{}_'.format(puzzle_num, str(self))
            self._search_logger = logging.getLogger('.'.join(map(str, ['search', self, puzzle_num])))
            self._search_logger.addHandler(logging.FileHandler(filename + 'search.txt', 'w'))
            self._sol_logger = logging.getLogger('.'.join(map(str, ['sol', self, puzzle_num])))
            self._sol_logger.addHandler(logging.FileHandler(filename + 'solution.txt', 'w'))

    def __str__(self):
        return 'ucs'

    def evaluation_function(self, new_state):
        return new_state.path_cost, 0

    def search(self, puzzle):
        start_time = time()
        self._open_list.put((0, puzzle.state))
        while self._open_list:
            _, puzzle.state = self.get_best_next_state(puzzle.state)
            if puzzle.is_goal():
                self._runtime = time() - start_time
                break
            self.update_open_list(puzzle.state)
        pass

class GBFS(SearchStrategy, ABC):
    def __init__(self, h_func:Heuristic = H0(), puzzle_num=0):
        super().__init__(h_func)
        if not logging_disabled:
            filename = 'out/{}_{}_'.format(puzzle_num, str(self))
            self._search_logger = logging.getLogger('.'.join(map(str, ['search', self, puzzle_num])))
            self._search_logger.addHandler(logging.FileHandler(filename + 'search.txt', 'w'))
            self._sol_logger = logging.getLogger('.'.join(map(str, ['sol', self, puzzle_num])))
            self._sol_logger.addHandler(logging.FileHandler(filename + 'solution.txt', 'w'))

    def __str__(self):
        return 'gbfs-' + str(self._heuristic)

    def evaluation_function(self, new_state):
        return 0, self._heuristic.estimate(new_state.config)

    def search(self, puzzle):
        pass


class AStar(SearchStrategy, ABC):
    def __init__(self, h_func:Heuristic = H0(), puzzle_num=0):
        super().__init__(h_func)
        if not logging_disabled:
            filename = 'out/{}_{}_'.format(puzzle_num, str(self))
            self._search_logger = logging.getLogger('.'.join(map(str, ['search', self, puzzle_num])))
            self._search_logger.addHandler(logging.FileHandler(filename + 'search.txt', 'w'))
            self._sol_logger = logging.getLogger('.'.join(map(str, ['sol', self, puzzle_num])))
            self._sol_logger.addHandler(logging.FileHandler(filename + 'solution.txt', 'w'))

    def __str__(self):
        return 'astar-' + str(self._heuristic)

    def evaluation_function(self, new_state):
        return new_state.path_cost, self._heuristic.estimate(new_state.config)

    def search(self, puzzle):
        pass