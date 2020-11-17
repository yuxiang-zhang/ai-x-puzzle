from abc import ABC, abstractmethod
import math

goal1 = [1, 2, 3, 4, 5, 6, 7, 0]
goal2 = [1, 3, 5, 7, 2, 4, 6, 0]

class Heuristic(ABC):

    def __init__(self, goals:iter):
        if not goals:
            raise Exception('No goals defined for Heuristic. ')
        self._goals = goals

    @abstractmethod
    def estimate(self, config:list):
        pass

    pass


class H0(Heuristic, ABC):
    """
    A naive heuristic that simply estimates:
        0, if 0 is at bottom right corner
        1, otherwise
    """

    def __str__(self):
        return 'h0'

    def estimate(self, config:list):
        return 0 if config.index(0) == 7 else 1


class H1(Heuristic, ABC):
    """    Modified Euclidean distance    """

    def __str__(self):
        return 'h1'

    def estimate(self, config:list):
        return min(self.get_ouci_distance(config, goal1), self.get_ouci_distance(config, goal2))

    def get_ouci_distance(self, list_input: iter, list_goal):
        distance_list = []
        for i in range(len(list_input)):
            row_input = i // 4
            col_input = i % 4

            goal_index = list_goal.index(list_input[i])

            row_goal = goal_index // 4
            col_goal = goal_index % 4

            if abs(col_goal - col_input) > 2:
                dist_goal = math.floor(math.sqrt(1 + (row_input ** 2 + row_goal) ** 2))
            else:
                dist_goal = math.floor(math.sqrt((row_input - row_goal) ** 2 + (col_input - col_goal) ** 2))

            distance_list.append(dist_goal)
        return sum(distance_list)


class H2(Heuristic, ABC):
    """    Modified Manhattan distance    """

    def __str__(self):
        return 'h2'

    def estimate(self, config:list):
        return min(self.get_manh_distance(config, goal1), self.get_manh_distance(config, goal2))

    def get_manh_distance(self, list_input: iter, list_goal):
        distance_list = []
        for i in range(len(list_input)):
            row_input = i // 4
            col_input = i % 4

            goal_index = list_goal.index(list_input[i])

            row_goal = goal_index // 4
            col_goal = goal_index % 4

            if abs(col_goal - col_input) > 2:
                dist_goal = 1 + abs(row_goal - row_input)
            else:
                dist_goal = abs(row_goal - row_input) + abs(col_goal - col_input)

            distance_list.append(dist_goal)
        return sum(distance_list)


class H3(Heuristic, ABC):
    """    Gaschnig    """

    def __str__(self):
        return 'h3'

    @staticmethod
    def first_mismatch(config, goal):
        for i, x in enumerate(goal):
            if config[i] != x:
                return i

    def estimate(self, config:list):
        config = list(config)
        min_moves = 100
        for goal in self._goals:
            moves = 0
            goal_blank = goal.index(0)
            while tuple(config) != goal:
                blank = config.index(0)
                if blank == goal_blank:
                    mismatch = self.first_mismatch(config, goal)
                else:
                    mismatch = config.index(goal[blank])
                config[blank], config[mismatch] = config[mismatch], config[blank]
                moves += 1
            min_moves = min(min_moves, moves)
        return min_moves


class H4(Heuristic, ABC):
    """ Hamming Distance """

    def __str__(self):
        return 'h4'

    @staticmethod
    def count_mismatch(config:list, goal:tuple):
        cnt = 0
        for i, x in enumerate(goal):
            if x != 0 and config[i] != x:
                cnt += 1
        return cnt

    def estimate(self, config:list):
        config = list(config)
        min_moves = 100
        for goal in self._goals:
            moves = self.count_mismatch(config, goal)
            min_moves = min(min_moves, moves)
        return min_moves


class H5(Heuristic, ABC):
    """ Count Rows and Cols Disorder Distance """

    def __str__(self):
        return 'h5'

    @staticmethod
    def count_mismatch(config, goal, row, col):
        ans = [0, 0]
        for i in range(row):
            for j in range(col):
                index = j + i * col
                if config[index] != goal[index]:
                    ans[0] += 1
                    break

        for j in range(col):
            for i in range(row):
                index = j + i * col
                if config[index] != goal[index]:
                    ans[1] += 1
                    break

        ans[0] = ans[0]
        ans[1] = ans[1]
        return min(ans)

    def estimate(self, config:list):
        config = list(config)
        min_moves = 100
        for goal in self._goals:
            moves = self.count_mismatch(config, goal, 2, 4)
            min_moves = min(min_moves, moves)
        return min_moves

if __name__ == '__main__':
    h = H5([(1,2,3,4,5,6,7,0), (1,3,5,7,2,4,6,0)])

    print(h.estimate([3, 0, 1, 4, 2, 6, 5, 7]))
    print(h.estimate([6, 3, 4, 7, 1, 2, 5, 0]))
    print(h.estimate([1, 0, 3, 6, 5, 2, 7, 4]))
    print(h.estimate([1, 2, 3, 4, 5, 6, 0, 7]))