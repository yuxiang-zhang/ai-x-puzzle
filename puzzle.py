from state import State, State2D
import numpy as np

class Puzzle8:
    goal1 = State((1, 2, 3, 4, 5, 6, 7, 0))
    goal2 = State((1, 3, 5, 7, 2, 4, 6, 0))

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def __init__(self, init_config: tuple):
        if len(init_config) != 8:
            raise Exception('Bad length for an 8-puzzle')
        # initial state
        self._state = State(init_config, 0)

    def is_goal(self):
        return self._state in [Puzzle8.goal1, Puzzle8.goal2]

    def gen_config(self, blank, tile):
        conf = list(self._state.config)
        conf[blank], conf[tile] = conf[tile], conf[blank]
        return tuple(conf)

    def successor(self):
        blank = self._state.config.index(0)
        moves = {1:[], 2:[], 3:[]}

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

        successors = []
        for move_cost, tiles in moves.items():
            for tile in tiles:
                successors.append(State(self.gen_config(blank, tile),
                                        self._state.path_cost + move_cost,
                                        self._state,
                                        self._state.config[tile]))

        return successors

class Puzzle:

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def __init__(self, init_config: tuple, goals: [], shape):
        self._goals = [hash(np.array(goal).tobytes()) for goal in goals if len(goal) == len(goals[0])]
        if not self._goals:
            raise Exception('No goal was defined. ')
        # initial state
        self._state = State2D(np.array(init_config).reshape(shape), 0)

    def is_goal(self):
        return hash(self._state) in self._goals

    def gen_config(self, blank_row, blank_col, tile_row, tile_col):
        conf = self._state.config.copy()
        conf[blank_row, blank_col], conf[tile_row, tile_col] = conf[tile_row, tile_col], conf[blank_row, blank_col]
        return conf

    def successor(self):
        blank_index = np.where(self._state.config == 0)
        blank_index = blank_index[0][0], blank_index[1][0]
        moves = {1:[], 2:[], 3:[]}

        nrows, ncols = self._state.config.shape

        # Vertical or Wrapping
        if blank_index[0] != 0: #not first row
            moves[1].append((blank_index[0] - 1, blank_index[1]))
        else:
            moves[2].append((nrows - 1, blank_index[1]))
        if blank_index[0] != nrows - 1: #not last row
            moves[1].append((blank_index[0] + 1, blank_index[1]))
        else:
            moves[2].append((0, blank_index[1]))

        # Horizontal or Wrapping
        if blank_index[1] != ncols - 1: #not last col
            moves[1].append((blank_index[0], blank_index[1] + 1))
        else:
            moves[2].append((blank_index[0], 0))
        if blank_index[1] != 0: #not first col
            moves[1].append((blank_index[0], blank_index[1] - 1))
        else:
            moves[2].append((blank_index[0], ncols - 1))

        # Corner moves
        if blank_index[0] == 0 and blank_index[1] == 0:
            moves[3].append((nrows - 1, ncols - 1))
            moves[3].append((1, 1))
        elif blank_index[0] == nrows - 1 and blank_index[1] == 0:
            moves[3].append((0, ncols - 1))
            moves[3].append((nrows - 2, 1))
        elif blank_index[0] == 0 and blank_index[1] == ncols - 1:
            moves[3].append((nrows - 1, 0))
            moves[3].append((1, ncols - 2))
        else:
            moves[3].append((0, 0))
            moves[3].append((nrows - 2, ncols - 2))

        successors = []
        for move_cost, tiles in moves.items():
            for tile_index in tiles:
                successors.append(State2D(self.gen_config(*blank_index, *tile_index),
                                        self._state.path_cost + move_cost,
                                        self._state,
                                        self._state.config[tile_index[0], tile_index[1]]))

        return successors