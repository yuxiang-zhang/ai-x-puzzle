class State:
    MAX_MOVES = 31

    @property
    def config(self):
        return self._config

    @property
    def from_state(self):
        return self._from_state

    @from_state.setter
    def from_state(self, state):
        self._from_state = state

    @property
    def path_cost(self):
        return self._path_cost

    @path_cost.setter
    def path_cost(self, cost):
        self._path_cost = cost

    def __init__(self, init_config:tuple, cost=MAX_MOVES, from_state=None):
        if len(init_config) != 8:
            raise Exception('Bad length for an 8-puzzle')
        self._config = list(init_config)
        self._path_cost = cost
        self._from_state = from_state

    def __hash__(self):
        val = tuple(self.config)
        key = hash(val)
        return key

    def __eq__(self, other):
        if isinstance(other, State):
            return hash(self) == hash(other)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, State):
            return hash(tuple(self._config)) < hash(tuple(other._config))
        return NotImplemented

    def __str__(self):
        return ' '.join(map(str, self.config[:4])) + '\n' + ' '.join(map(str, self.config[4:]))