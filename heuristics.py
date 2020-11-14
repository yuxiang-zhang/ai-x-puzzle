from abc import ABC, abstractmethod


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
        pass


class H2(Heuristic, ABC):
    """
    [Add description]
    """

    def __str__(self):
        return 'h2'

    def estimate(self, config):
        pass