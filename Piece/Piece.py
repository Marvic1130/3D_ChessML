import json
from abc import ABC, abstractmethod
from Enum import Color


class Piece(ABC):
    def __init__(self, id_: int, color: Color, x: int, y: int):
        self.id = id_
        self.color = color
        self.x = x
        self.y = y
        self.live = True

    @abstractmethod
    def valid_move_list(self):
        pass

    @abstractmethod
    def is_valid_move(self):
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
