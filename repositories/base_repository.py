# repositories/base_repository.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TypeVar, Generic

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, data: Dict[str, Any]) -> Optional[T]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def update(self, entity: T, data: Dict[str, Any]) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, uuid: str) -> bool:
        pass
