from abc import ABC, abstractmethod
from typing import Optional

from app.services import CollectedItem


class BaseCollector(ABC):
    name: str = "base"
    source_type: str = "base"
    base_url: Optional[str] = None

    @abstractmethod
    def collect(self) -> list[CollectedItem]:
        raise NotImplementedError
