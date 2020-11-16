import unittest
import puzzle
import searchstrat
from state import State
import os, glob

class TestPuzzle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        for filename in glob.glob("out/-1*"):
            os.remove(filename)
        pass

    def test_get_state(self):
        game = puzzle.Puzzle8((4, 2, 3, 1, 5, 6, 7, 0))
        self.assertEqual(game.state, State((4, 2, 3, 1, 5, 6, 7, 0)))

    def test_set_state(self):
        game = puzzle.Puzzle8((4, 2, 3, 1, 5, 6, 7, 0))
        newgame = puzzle.Puzzle8((1, 3, 5, 7, 2, 4, 6, 0))
        game.state = newgame.state
        self.assertEqual(game.state, newgame.state)

    def test_goal(self):
        self.assertTrue(puzzle.Puzzle8((1, 3, 5, 7, 2, 4, 6, 0)).is_goal())
        self.assertFalse(puzzle.Puzzle8((4, 2, 3, 1, 5, 6, 7, 0)).is_goal())

    def test_gen_config(self):
        game = puzzle.Puzzle8((4, 2, 3, 1, 5, 6, 7, 0))
        self.assertEqual(game.gen_config(0, 7), tuple((0, 2, 3, 1, 5, 6, 7, 4)))

    def test_update_open_list_with_successor_function(self):
        import heapq
        game = puzzle.Puzzle8((4, 2, 3, 1, 5, 6, 7, 0))
        strat = searchstrat.AStar()
        strat.update_open_list(game.successor())
        init_state = State((4, 2, 3, 1, 5, 6, 7, 0))
        successors = [(1, State((4, 2, 3, 0, 5, 6, 7, 1), 1, init_state)),
                      (1, State((4, 2, 3, 1, 5, 6, 0, 7), 1, init_state)),
                      (2, State((4, 2, 3, 1, 0, 6, 7, 5), 2, init_state)),
                      (3, State((0, 2, 3, 1, 5, 6, 7, 4), 3, init_state)),
                      (3, State((4, 2, 0, 1, 5, 6, 7, 3), 3, init_state))]
        while successors:
            self.assertEqual(heapq.heappop(successors)[-1], strat.get_best_next_state(game.state)[-1])

    def test_state_str(self):
        self.assertRegex(str(State((4,2,3,0,5,6,7,1))), '4 2 3 0 5 6 7 1')

    def test_searchstrat_fail(self):
        game = puzzle.Puzzle8((1, 2, 3, 4, 5, 6, 0, 7))
        strat = searchstrat.UCS()
        strat.setup_loggers()
        strat.search(game)
        strat.fail()
        with open('out/-1_ucs_search.txt', 'r') as f:
            self.assertEqual(f.read(), 'no solution')
        with open('out/-1_ucs_solution.txt', 'r') as f:
            self.assertEqual(f.read(), 'no solution')

if __name__ == '__main__':
    unittest.main()
