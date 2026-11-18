"""Undo/redo stack for instant-apply settings."""

from __future__ import annotations

from collections import deque
from copy import deepcopy

from .config import load_config, save_config


class UndoStack:
    def __init__(self, capacity: int = 50):
        self._undo: deque = deque(maxlen=capacity)
        self._redo: deque = deque(maxlen=capacity)
        self._current = load_config()

    def push(self, new_cfg: dict) -> None:
        self._undo.append(deepcopy(self._current))
        self._redo.clear()
        self._current = deepcopy(new_cfg)
        save_config(self._current)

    def undo(self) -> dict | None:
        if not self._undo:
            return None
        self._redo.append(deepcopy(self._current))
        self._current = self._undo.pop()
        save_config(self._current)
        return deepcopy(self._current)

    def redo(self) -> dict | None:
        if not self._redo:
            return None
        self._undo.append(deepcopy(self._current))
        self._current = self._redo.pop()
        save_config(self._current)
        return deepcopy(self._current)

    @property
    def can_undo(self) -> bool:
        return bool(self._undo)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo)

    @property
    def current(self) -> dict:
        return deepcopy(self._current)