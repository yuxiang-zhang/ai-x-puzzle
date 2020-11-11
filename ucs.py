# from queue import PriorityQueue
import heapq
import unittest
from enum import Enum

class Puzzle8:

    Move = Enum('Move', ('Horizontal', 'Vertical', 'Wrapping', 'Diagonal'))

    goal1_hash = hash((1, 2, 3, 4, 5, 6, 7, 0))
    goal2_hash = hash((1, 3, 5, 7, 2, 4, 6, 0))

    dict_conf = {goal1_hash:[1, 2, 3, 4, 5, 6, 7, 0], goal2_hash:[1, 3, 5, 7, 2, 4, 6, 0]}

    def __init__(self, start_config):
        assert(len(start_config) == 8)
        self.config = list(start_config)
        self.open_list = []
        self.closed_list = {}

    def __hash__(self):
        return hash(tuple(self.config))

    def __eq__(self, other):
        if isinstance(other, Puzzle8):
            return tuple(self.config) == tuple(other.config)
        return NotImplemented

    def is_goal(self):
        return self.__hash__() == Puzzle8.goal1_hash or self.__hash__() == Puzzle8.goal2_hash

    def get_next_conf(self, blank, move):
        conf = list(self.config)
        conf[blank], conf[move] = conf[move], conf[blank]
        key = hash(tuple(conf))
        if key not in self.dict_conf:
            self.dict_conf[key] = conf
        return key

    def move(self, move_type, blank):
        cost = 0
        swap_pos = []
        ans = {}
        if move_type == self.Move.Horizontal:
            cost = 1
            if blank not in [0, 4]:
                swap_pos.append(blank - 1)
            if blank not in [3, 7]:
                swap_pos.append(blank + 1)
        elif move_type == self.Move.Vertical:
            cost = 1
            swap_pos.append(blank + 4 if blank < 4 else blank - 4)
        elif move_type == self.Move.Wrapping:
            cost = 2
            if blank in [0, 4]:
                swap_pos.append(blank + 3)
            else:
                swap_pos.append(blank - 3)
        elif move_type == self.Move.Diagonal:
            cost = 3
            if blank == 0:
                swap_pos.extend([5, 7])
            elif blank == 3:
                swap_pos.extend([4,6])
            elif blank == 4:
                swap_pos.extend([1,3])
            elif blank == 7:
                swap_pos.extend([0, 2])

        for i in swap_pos:
            next_conf_key = self.get_next_conf(blank, i)
            ans[cost] = next_conf_key
        return ans

    def successor(self):
        blank = self.config.index(0)
        if self.config.index(0) in [0, 3, 4, 7]:
            # corner moves
            next_confs = self.move(self.Move.Wrapping, blank)
            for next_cost, next_conf in next_confs.items():
                if next_conf not in self.closed_list:
                    heapq.heappush(self.open_list)
                    # for i, (cost, conf_pair) in enumerate(self.open_list): #check if already in open_list
                    #     if next_conf == conf_pair[0]:
                    #         if next_cost < cost: # if cost is less, update cost
                    #             self.open_list[i] = (next_cost, conf_pair)
                    #             heapq.heapify(self.open_list)
                    #         break
            self.move(self.Move.Diagonal, blank)
            pass
        self.move()
        # regular moves

        pass


class TestPuzzle(unittest.TestCase):

    def test_goal(self):
        self.assertTrue(Puzzle8([1, 3, 5, 7, 2, 4, 6, 0]).is_goal())
        self.assertFalse(Puzzle8([4, 2, 3, 1, 5, 6, 7, 0]).is_goal())

    pass

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