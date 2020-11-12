from state import State

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
                                        self._state))

        return successors