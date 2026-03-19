from abc import ABC, abstractmethod

from app.services import CollectedItem


class BaseCollector(ABC):
    name: str = "base"
    source_type: str = "base"
    base_url: str | None = None

    @abstractmethod
    def collect(self) -> list[CollectedItem]:
        raise NotImplementedError
