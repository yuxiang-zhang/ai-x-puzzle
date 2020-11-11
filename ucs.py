# from queue import PriorityQueue
import heapq
import unittest
from enum import Enum

class Puzzle8:

    Move = Enum('Move', ('Horizontal', 'Vertical', 'Wrapping', 'Diagonal'))

    goal1_hash = hash((1, 2, 3, 4, 5, 6, 7, 0))
    goal2_hash = hash((1, 3, 5, 7, 2, 4, 6, 0))

    dict_conf = {goal1_hash:(1, 2, 3, 4, 5, 6, 7, 0), goal2_hash:(1, 3, 5, 7, 2, 4, 6, 0)}

    def __init__(self, start_config:iter):
        if len(start_config) != 8:
            raise Exception('Bad length for an 8-puzzle')
        self.config = list(start_config)
        self.open_list = []
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
        ans = {}

        # Regular moves
        # Horizontal
        cost = 1
        if blank not in [0, 4]:
            moves[cost].append(blank - 1)
        if blank not in [3, 7]:
            moves[cost].append(blank + 1)

        # Vertical
        moves[cost].append(blank + 4 if blank < 4 else blank - 4)

        # Corner moves
        if self.config.index(0) in [0, 3, 4, 7]:
            # Wrapping
            cost = 2
            if blank in [0, 4]:
                moves[cost].append(blank + 3)
            else:
                moves[cost].append(blank - 3)
            # Diagonal
            cost = 3
            if blank == 0:
                moves[cost].extend([5, 7])
            elif blank == 3:
                moves[cost].extend([4, 6])
            elif blank == 4:
                moves[cost].extend([1, 3])
            elif blank == 7:
                moves[cost].extend([0, 2])

        for cost, tiles in moves.items():
            for tile in tiles:
                ans[self.hash_next_conf(blank, tile)] = cost

        return ans

    def successor(self):
        blank = self.config.index(0)
        successors = self.move(blank)

        for new_conf_hash, cost in successors.items():
            if new_conf_hash not in self.closed_list:
                heapq.heappush(self.open_list, (cost, tuple((new_conf_hash, self.__hash__()))))
                #check if already in open_list
                # for i, (cost, conf_pair) in enumerate(self.open_list):
                #     if next_conf == conf_pair[0]:
                #         if next_cost < cost: # if cost is less, update cost
                #             self.open_list[i] = (next_cost, conf_pair)
                #             heapq.heapify(self.open_list)
                #         break

    def __str__(self):
        return ' '.join(map(str, self.config[:4])) + '\n' + ' '.join(map(str, self.config[4:]))


class TestPuzzle(unittest.TestCase):

    def test_goal(self):
        self.assertTrue(Puzzle8([1, 3, 5, 7, 2, 4, 6, 0]).is_goal())
        self.assertFalse(Puzzle8([4, 2, 3, 1, 5, 6, 7, 0]).is_goal())

    def test_successor(self):
        puzzle = Puzzle8([4, 2, 3, 1, 5, 6, 7, 0])
        puzzle.successor()
        initial_hash = hash((4, 2, 3, 1, 5, 6, 7, 0))
        successors = [(1, (hash((4, 2, 3, 0, 5, 6, 7, 1)), initial_hash)),
                      (1, (hash((4, 2, 3, 1, 5, 6, 0, 7)), initial_hash)),
                      (2, (hash((4, 2, 3, 1, 0, 6, 7, 5)), initial_hash)),
                      (3, (hash((0, 2, 3, 1, 5, 6, 7, 4)), initial_hash)),
                      (3, (hash((4, 2, 0, 1, 5, 6, 7, 3)), initial_hash))]
        while puzzle.open_list:
            self.assertEqual(heapq.heappop(successors), heapq.heappop(puzzle.open_list))

# open_list = PriorityQueue()
# open_list.put()
# #                closed_list[closed_list[e]] visited_state_hash ->
# open_list = []
# heapq.heapify(open_list)
# heapq.heappush(open_list, (1, 'first write spec'))
# heapq.heappush(open_list, (3, 'create tests'))
# heapq.heappush(open_list, (1, 'second write spec'))
# heapq.heappush(open_list, (5, (hash, hash)))
# heapq.heappush(open_list, (7, 'release product'))
# heapq.heappush(open_list, (1, 'third write spec'))
#
# for i in range(len(open_list)):
#     print(heapq.heappop(open_list))
# print(hash(((1),(2))))



if __name__ == '__main__':
    unittest.main()