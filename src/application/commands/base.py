from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    async def execute(self) -> str:
        pass

