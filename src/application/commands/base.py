from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    async def execute(self) -> str:
        pass

    @abstractmethod
    def to_raw(self) -> str:
        """
        Serialize command to raw TCP string.
        """
        pass
