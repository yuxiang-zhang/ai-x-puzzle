from abc import ABC, abstractmethod
import heapq
from heuristics import Heuristic, H0

class SearchStrategy(ABC):

    def __init__(self, h_func:Heuristic = H0):
        # heuristic function
        self._heuristic = h_func
        # pq sorted by f(n)
        self._open_list = []
        # visited_state_hash -> parent_state_hash
        self._closed_list = {}
        super().__init__()

    @abstractmethod
    def evaluation_function(self, path_cost, new_state):
        pass

    @abstractmethod
    def search_for_goal(self, is_goal):
        pass

    def update_open_list(self, successors, old_state):
        for new_state, path_cost in successors.items():
            if new_state not in self._closed_list:
                # don't check if already in open_list, directly put in open_list;
                # for duplicates, check in closed list whenever popping from open list
                heapq.heappush(self._open_list, (self.evaluation_function(path_cost, new_state),
                                                 (new_state, old_state)
                                                 ))

    def get_best_next(self):
        return heapq.heappop(self._open_list)


class UniformCost(SearchStrategy, ABC):

    def evaluation_function(self, path_cost, new_state):
        return path_cost

    def search_for_goal(self, is_goal):
        pass


class GBFS(SearchStrategy, ABC):

    def evaluation_function(self, path_cost, new_state):
        return self._heuristic.estimate(new_state.config)

    def search_for_goal(self, is_goal):
        pass

class AlgoA(SearchStrategy, ABC):

    def evaluation_function(self, path_cost, new_state):
        return path_cost + self._heuristic.estimate(new_state.config)

    def search_for_goal(self, is_goal):
        pass