from abc import ABC, abstractmethod
from typing import Any


class BaseFetcher(ABC):
    @abstractmethod
    async def fetch(self, source: dict[str, Any]) -> list[dict[str, Any]]:
        raise NotImplementedError
