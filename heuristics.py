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
    def estimate(self, config):
        return 0 if config.index(0) == 7 else 1