import json
from abc import ABC, abstractmethod
from Enum import Color


class Piece(ABC):
    def __init__(self, id: int, color: Color, x: int, y: int):
        self.id = id
        self.color = color
        self.x = x
        self.y = y
        self.live = True

    @abstractmethod
    def validMoveList(self):
        pass

    @abstractmethod
    def isValidMove(self):
        pass

    @abstractmethod
    def move(self, x, y):
        pass

    @abstractmethod
    def live(self):
        pass

    @abstractmethod
    def attack(self, target):
        pass
