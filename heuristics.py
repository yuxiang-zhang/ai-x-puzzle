from abc import ABC, abstractmethod
import math

goal1 = [1, 2, 3, 4, 5, 6, 7, 0]
goal2 = [1, 3, 5, 7, 2, 4, 6, 0]


def get_index(number, list):
    return list.index(number)


class Heuristic(ABC):

    @abstractmethod
    def estimate(self, config):
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

    def estimate(self, config):
        return 0 if config.index(0) == 7 else 1


class H1(Heuristic, ABC):
    """
    [Add description]
    """

    def __str__(self):
        return 'h1'

    def estimate(self, config):
        input = config
        return min(self.get_ouci_distance(input, goal1), self.get_ouci_distance(input, goal2))

    # Modified euclidean distance
    def get_ouci_distance(self, list_input, list_goal):
        distance_list = []
        for i in range(len(list_input)):
            row_input = i // 4
            col_input = i % 4

            row_goal = get_index(list_input[i], list_goal) // 4
            col_goal = get_index(list_input[i], list_goal) % 4

            if abs(col_goal - col_input) > 2:
                dist_goal = math.floor(math.sqrt(1 + (row_input ** 2 + row_goal) ** 2))
            else:
                dist_goal = math.floor(math.sqrt((row_input - row_goal) ** 2 + (col_input - col_goal) ** 2))

            distance_list.append(dist_goal)
        return sum(distance_list)


class H2(Heuristic, ABC):
    """
    [Add description]
    """

    def __str__(self):
        return 'h2'

    def estimate(self, config):
        return min(self.get_manh_distance(config, goal1), self.get_manh_distance(config, goal2))

    def get_manh_distance(self, list_input, list_goal):
        distance_list = []
        for i in range(len(list_input)):
            row_input = i // 4
            col_input = i % 4

            row_goal = get_index(list_input[i], list_goal) // 4
            col_goal = get_index(list_input[i], list_goal) % 4

            if abs(col_goal - col_input) > 2:
                dist_goal = 1 + abs(row_goal - row_input)
            else:
                dist_goal = abs(row_goal - row_input) + abs(col_goal - col_input)

            distance_list.append(dist_goal)
        return sum(distance_list)