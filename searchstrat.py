from abc import ABC, abstractmethod
from queue import PriorityQueue
from heuristics import Heuristic, H0
from puzzle import Puzzle8

class SearchStrategy(ABC):

    def __init__(self, h_func:Heuristic = H0, game:Puzzle8=None):
        self._game = game
        # heuristic function
        self._heuristic = h_func
        # pq sorted by f(n)
        self._open_list = PriorityQueue()
        self._open_dict = {}
        # visited_state_hash -> parent_state_hash
        self._closed_list = {}
        super().__init__()

    @abstractmethod
    def evaluation_function(self, new_state):
        pass

    @abstractmethod
    def search(self):
        pass

    def update_open_list(self, successors, from_state):
        for to_state in successors:
            key = hash(to_state)
            if key not in self._closed_list:
                if key not in self._open_dict:
                    self._open_dict[key] = to_state
                    self._open_list.put((self.evaluation_function(to_state), to_state))
                elif self._open_dict[key].path_cost > to_state.path_cost:
                        self._open_dict[key].from_state = self._game.state
                        self._open_dict[key].path_cost = to_state.path_cost


    def get_best_next(self):
        return self._open_list.get()[-1]


class UniformCost(SearchStrategy, ABC):

    def evaluation_function(self, new_state):
        return new_state.path_cost

    def search(self):
        pass

class GBFS(SearchStrategy, ABC):

    def evaluation_function(self, new_state):
        return self._heuristic.estimate(new_state.config)

    def search(self):
        pass


class AlgoA(SearchStrategy, ABC):

    def evaluation_function(self, new_state):
        return new_state.path_cost + self._heuristic.estimate(new_state.config)

    def search(self):
        pass