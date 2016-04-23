
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractBaseCrawler(metaclass=ABCMeta):
    """
    Abstract Base Class defining a site crawler
    """
    @abstractproperty
    def crawl_strategy(self):
        return NotImplementedError

    @crawl_strategy
    def set_crawl_strategy(self):
        return NotImplementedError

    @abstractmethod
    def __next___(self):
        """Moves forward
        """
        yield NotImplementedError

    @abstractmethod
    def run(self, *args, **kwargs):
        """Probably something like this
        """
        return self.command(*args, **kwargs)


