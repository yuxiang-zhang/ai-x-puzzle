import unittest
from queue import PriorityQueue
import puzzle
import searchstrat
from state import State2D
import os, glob
import heuristics
import numpy as np

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
        game = puzzle.Puzzle((4, 2, 3, 1, 5, 6, 7, 0), puzzle.OldPuzzle.goals, (2, 4))
        self.assertEqual(game.state, State2D(np.array([4, 2, 3, 1, 5, 6, 7, 0])))

    def test_set_state(self):
        game = puzzle.Puzzle((4, 2, 3, 1, 5, 6, 7, 0), puzzle.OldPuzzle.goals, (2, 4))
        newgame = puzzle.Puzzle((1, 3, 5, 7, 2, 4, 6, 0), puzzle.OldPuzzle.goals, (2, 4))
        game.state = newgame.state
        self.assertEqual(game.state, newgame.state)

    def test_goal(self):
        self.assertTrue(puzzle.Puzzle((1, 3, 5, 7, 2, 4, 6, 0), puzzle.OldPuzzle.goals, (2, 4)).is_goal())
        self.assertFalse(puzzle.Puzzle((4, 2, 3, 1, 5, 6, 7, 0), puzzle.OldPuzzle.goals, (2, 4)).is_goal())

    def test_update_open_list_with_successor_function(self):
        game = puzzle.Puzzle((4, 2, 3, 1, 5, 6, 7, 0), puzzle.OldPuzzle.goals, (2, 4))
        strat = searchstrat.UCS(heuristics.H0(puzzle.OldPuzzle.goals))
        strat.update_open_list(game.successor())
        init_state = State2D(np.array([4, 2, 3, 1, 5, 6, 7, 0]), 0)
        q = PriorityQueue()
        successors = [(1, State2D(np.array([4, 2, 3, 0, 5, 6, 7, 1]), 1, init_state)),
                      (1, State2D(np.array([4, 2, 3, 1, 5, 6, 0, 7]), 1, init_state)),
                      (2, State2D(np.array([4, 2, 3, 1, 0, 6, 7, 5]), 2, init_state)),
                      (3, State2D(np.array([0, 2, 3, 1, 5, 6, 7, 4]), 3, init_state)),
                      (3, State2D(np.array([4, 2, 0, 1, 5, 6, 7, 3]), 3, init_state))]
        for s in successors:
            q.put(s)
        for _ in successors:
            self.assertEqual(q.get()[-1], strat.get_best_next_state())

    def test_state_str(self):
        self.assertRegex(str(State2D(np.array([4, 2, 3, 1, 5, 6, 7, 0]), 0)), '^(\d\s){7}\d$')

    def test_searchstrat_fail(self):
        game = puzzle.Puzzle((1, 2, 3, 4, 5, 6, 0, 7), puzzle.OldPuzzle.goals, (2, 4))
        strat = searchstrat.UCS(heuristics.H0(puzzle.OldPuzzle.goals))
        strat.setup_loggers()
        strat.search(game)
        strat.fail()
        with open('out/-1_ucs_search.txt', 'r') as f:
            self.assertEqual(f.read(), 'no solution')
        with open('out/-1_ucs_solution.txt', 'r') as f:
            self.assertEqual(f.read(), 'no solution')

    def test_gbfs_search_H1(self):
        game = puzzle.Puzzle((4, 2, 3, 1, 5, 6, 7, 0), puzzle.OldPuzzle.goals, (2, 4))
        strat = searchstrat.GBFS(heuristics.H1(puzzle.OldPuzzle.goals))
        strat.search(game)

    def test_gbfs_search_H2(self):
        game = puzzle.Puzzle((4, 2, 3, 1, 5, 6, 7, 0), puzzle.OldPuzzle.goals, (2, 4))
        strat = searchstrat.GBFS(heuristics.H2(puzzle.OldPuzzle.goals))
        strat.search(game)

if __name__ == '__main__':
    unittest.main()
