import heapq
import unittest
from puzzle import Puzzle8

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


if __name__ == '__main__':
    unittest.main()