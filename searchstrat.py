from abc import ABC, abstractmethod
from queue import PriorityQueue
from heuristics import Heuristic, H0
from puzzle import Puzzle8

class SearchStrategy(ABC):

    def __init__(self, h_func:Heuristic = H0, game:Puzzle8=None):
        # the puzzle to be solved
        self._game = game
        # heuristic function
        self._heuristic = h_func
        # pq sorted by f(n)
        self._open_list = PriorityQueue()
        # visited_state -> parent_state
        self._closed_list = {}
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
            key = hash(to_state)
            if key not in self._closed_list:
                self._open_list.put((self.evaluation_function(to_state), to_state))

    def get_best_next_state(self):
        """Pop next minimal cost state from open list"""
        while self._open_list.not_empty:
            state = self._open_list.get()[-1]
            if state not in self._closed_list:
                self._closed_list[state] = self._game.state
                return state
        return None # empty open list


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