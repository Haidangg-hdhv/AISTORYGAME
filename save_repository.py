from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.models import GameState


class BaseSaveRepository(ABC):
    @abstractmethod
    def save(self, game_state: GameState) -> None:
        raise NotImplementedError

    @abstractmethod
    def load(self, session_id: str) -> GameState:
        raise NotImplementedError

    @abstractmethod
    def exists(self, session_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, session_id: str) -> None:
        raise NotImplementedError

    # ---> ĐÂY LÀ ĐOẠN MỚI THÊM VÀO <---
    @abstractmethod
    def get_sessions_by_user(self, user_id: str) -> list[dict]:
        raise NotImplementedError