# from queue import PriorityQueue
from searchstrat import SearchStrategy
from state import State

class Puzzle8:
    goal1 = State((1, 2, 3, 4, 5, 6, 7, 0))
    goal2 = State((1, 3, 5, 7, 2, 4, 6, 0))

    @property
    def search_strat(self):
        return self._search_strat

    @search_strat.setter
    def search_strat(self, strat):
        self._search_strat = strat

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def __init__(self, init_config:iter, search_strat:SearchStrategy):
        if len(init_config) != 8:
            raise Exception('Bad length for an 8-puzzle')
        self._search_strat = search_strat
        # initial state
        self._state = State(init_config)

    @staticmethod
    def is_goal(self, state):
        return state == Puzzle8.goal1 or state == Puzzle8.goal2

    def gen_successor(self, blank, tile):
        conf = list(self._state.config)
        conf[blank], conf[tile] = conf[tile], conf[blank]
        return State(tuple(conf))

    def successor(self):
        blank = self._state.config.index(0)
        moves = {1:[], 2:[], 3:[]}
        successors = {}

        # Regular moves
        move_cost = 1
        # Vertical
        moves[move_cost].append(blank ^ int('100', 2))

        # Horizontal
        moves[move_cost].append(blank ^ int('001', 2))
        # Horizontal or Wrapping
        if blank in [0, 3, 4, 7]: # if 0 is in a corner
            move_cost = 2
        moves[move_cost].append(blank ^ int('011', 2)) # then this covers Wrapping case

        # Corner moves
        move_cost = 3
        moves[move_cost].append(blank ^ int('101', 2))
        moves[move_cost].append(blank ^ int('111', 2))

        for move_cost, tiles in moves.items():
            for tile in tiles:
                successors[self.gen_successor(blank, tile)] = self._state.path_cost + move_cost

        return successors

    def search(self):
        self._search_strat.search_for_goal(self.successor(), self.is_goal)