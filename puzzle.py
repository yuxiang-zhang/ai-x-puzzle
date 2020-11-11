# from queue import PriorityQueue
import heapq
from enum import Enum

class Puzzle8:

    Move = Enum('Move', ('Horizontal', 'Vertical', 'Wrapping', 'Diagonal'))

    goal1_hash = hash((1, 2, 3, 4, 5, 6, 7, 0))
    goal2_hash = hash((1, 3, 5, 7, 2, 4, 6, 0))

    dict_conf = {goal1_hash:(1, 2, 3, 4,
                             5, 6, 7, 0),
                 goal2_hash:(1, 3, 5, 7,
                             2, 4, 6, 0)}

    def __init__(self, start_config:iter):
        if len(start_config) != 8:
            raise Exception('Bad length for an 8-puzzle')
        self.config = list(start_config)
        # pq sorted by f(n)
        self.open_list = []
        # visited_state_hash -> parent_state_hash
        self.closed_list = {}

    def __hash__(self):
        key = hash(tuple(self.config))
        Puzzle8.dict_conf[key] = tuple(self.config)
        return key

    def __eq__(self, other):
        if isinstance(other, Puzzle8):
            return tuple(self.config) == tuple(other.config)
        return NotImplemented

    def is_goal(self):
        return self.__hash__() == Puzzle8.goal1_hash or self.__hash__() == Puzzle8.goal2_hash

    def hash_next_conf(self, blank, tile):
        conf = list(self.config)
        conf[blank], conf[tile] = conf[tile], conf[blank]
        key = hash(tuple(conf))
        if key not in Puzzle8.dict_conf:
            Puzzle8.dict_conf[key] = tuple(conf)
        return key

    def move(self, blank):
        moves = {1:[], 2:[], 3:[]}
        successors = {}

        # Regular moves
        cost = 1
        # Vertical
        moves[cost].append(blank ^ int('100', 2))

        # Horizontal
        moves[cost].append(blank ^ int('001', 2))
        # Horizontal or Wrapping
        if self.config.index(0) in [0, 3, 4, 7]: # if 0 is in a corner
            cost = 2
        moves[cost].append(blank ^ int('011', 2)) # then this covers Wrapping case


        # Corner moves
        cost = 3
        moves[cost].append(blank ^ int('101', 2))
        moves[cost].append(blank ^ int('111', 2))

        for cost, tiles in moves.items():
            for tile in tiles:
                successors[self.hash_next_conf(blank, tile)] = cost

        return successors

    def successor(self):
        blank = self.config.index(0)
        successors = self.move(blank)

        for new_conf_hash, cost in successors.items():
            if new_conf_hash not in self.closed_list:
                # don't check if already in open_list, directly put in open_list;
                # for duplicates, check in closed list whenever popping from open list
                heapq.heappush(self.open_list, (cost, 
                                                (new_conf_hash, self.__hash__())
                                                ))

    def __str__(self):
        return ' '.join(map(str, self.config[:4])) + '\n' + ' '.join(map(str, self.config[4:]))
