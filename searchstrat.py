import logging
from abc import ABC, abstractmethod
from queue import PriorityQueue
from heuristics import Heuristic, H0
from puzzle import Puzzle8

logging_disabled = False

class SearchStrategy(ABC):
    def __init__(self, h_func:Heuristic = H0(), game:Puzzle8=None):
        # the puzzle to be solved
        self._game = game
        # heuristic function
        self._heuristic = h_func
        # pq sorted by f(n)
        self._open_list = PriorityQueue()
        # visited_state -> parent_state
        self._closed_list = {}
        # logger to be defined in subclasses
        logging.basicConfig(filename='out/dump.log', format='%(message)s', level='INFO')
        self._search_logger = logging.getLogger()
        super().__init__()

    @abstractmethod
    def evaluation_function(self, new_state):
        """Evaluation function to be used to get/estimate the cost for a path. """
        pass

    @abstractmethod
    def search(self):
        """Core search strategy to be used to get the solution. """
        pass

    def update_open_list(self):
        """
        Insert computed successors one by one into the open_list.
        When inserting, don't check if the state already in open_list, directly put in open_list;
        for duplicates, check in closed list whenever popping from open list.
        :return:
        """
        successors = self._game.successor()
        for to_state in successors:
            if to_state not in self._closed_list:
                self._open_list.put((sum(self.evaluation_function(to_state)), to_state))

    def get_best_next_state(self):
        """Pop next minimal cost state from open list"""
        while self._open_list.not_empty:
            cost, state = self._open_list.get()
            if state not in self._closed_list:
                self._closed_list[state] = self._game.state
                search_file_entry = ' '.join(map(str, [cost, *self.evaluation_function(state), state]))
                self._search_logger.info(search_file_entry)
                return cost, state
        return None # empty open list


class UniformCost(SearchStrategy, ABC):
    def __init__(self, h_func:Heuristic = H0(), game:Puzzle8=None, puzzle_num=0):
        super().__init__(h_func, game)
        if not logging_disabled:
            self._search_logger = logging.getLogger(str(self))
            search_filename = 'out/{}_{}_search.txt'.format(puzzle_num, str(self))
            self._search_logger.addHandler(logging.FileHandler(search_filename))

    def __str__(self):
        return 'ucs'

    def evaluation_function(self, new_state):
        return new_state.path_cost, 0

    def search(self):
        self._open_list.put(self._game.state)
        while self._open_list:
            pass
        pass

class GBFS(SearchStrategy, ABC):
    def __init__(self, h_func:Heuristic = H0(), game:Puzzle8=None, puzzle_num=0):
        super().__init__(h_func, game)
        if not logging_disabled:
            self._search_logger = logging.getLogger(str(self))
            search_filename = 'out/{}_{}_search.txt'.format(puzzle_num, str(self))
            self._search_logger.addHandler(logging.FileHandler(search_filename))

    def __str__(self):
        return 'gbfs-' + str(self._heuristic)

    def evaluation_function(self, new_state):
        return 0, self._heuristic.estimate(new_state.config)

    def search(self):
        pass


class AStar(SearchStrategy, ABC):
    def __init__(self, h_func:Heuristic = H0(), game:Puzzle8=None, puzzle_num=0):
        super().__init__(h_func, game)
        if not logging_disabled:
            self._search_logger = logging.getLogger(str(self))
            search_filename = 'out/{}_{}_search.txt'.format(puzzle_num, str(self))
            self._search_logger.addHandler(logging.FileHandler(search_filename))

    def __str__(self):
        return 'astar-' + str(self._heuristic)

    def evaluation_function(self, new_state):
        return new_state.path_cost, self._heuristic.estimate(new_state.config)

    def search(self):
        pass