import heapq
import unittest
import puzzle
import searchstrat
from state import State


class TestPuzzle(unittest.TestCase):

    def test_goal(self):
        self.assertTrue(puzzle.Puzzle8([1, 3, 5, 7, 2, 4, 6, 0]).is_goal())
        self.assertFalse(puzzle.Puzzle8([4, 2, 3, 1, 5, 6, 7, 0]).is_goal())

    def test_update_open_list_with_successor_function(self):
        game = puzzle.Puzzle8([4, 2, 3, 1, 5, 6, 7, 0])
        strat = searchstrat.UniformCost(game=game)
        strat.update_open_list()
        init_state = State((4, 2, 3, 1, 5, 6, 7, 0))
        successors = [(1, State((4, 2, 3, 0, 5, 6, 7, 1), 1, init_state)),
                      (1, State((4, 2, 3, 1, 5, 6, 0, 7), 1, init_state)),
                      (2, State((4, 2, 3, 1, 0, 6, 7, 5), 2, init_state)),
                      (3, State((0, 2, 3, 1, 5, 6, 7, 4), 3, init_state)),
                      (3, State((4, 2, 0, 1, 5, 6, 7, 3), 3, init_state))]
        while successors:
            self.assertEqual(heapq.heappop(successors)[-1], strat.get_best_next_state())


if __name__ == '__main__':
    unittest.main()