import json
from abc import ABC, abstractmethod
from Enum.Color import Color


class Piece(ABC):
    def __init__(self, id_: int, color: Color, x: int, y: int):
        self.__id = id_
        self.__color = color
        self.__x = x
        self.__y = y
        self.__live = True

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, new_id: int):
        if 33 > new_id > 0:
            self.__id = new_id
        else:
            raise ValueError('The ID value of the piece(piece.id) must be between 1 and 32.')

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, new_color: Color):
        if new_color == Color.WHITE or new_color == Color.BLACK:
            self.__color = new_color
        else:
            raise ValueError('The color of the piece can only be black or white.')

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, new_x: int):
        if -1 < self.__x < 8:
            self.__x = new_x
        else:
            raise ValueError('The x value of piece is between 0 and 7.')

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, new_y: int):
        if -1 < self.__y < 8:
            self.__y = new_y
        else:
            raise ValueError('The y value of piece is between 0 and 7.')

    @property
    def live(self):
        return self.__live

    @live.setter
    def live(self, new_live: bool):
        if not self.__live and new_live:
            raise RuntimeError('The dead Piece cannot be saved again.')
        else:
            self.__live = new_live

    @abstractmethod
    def valid_move_list(self, target=None):
        pass

    @abstractmethod
    def is_valid_move(self, x, y, target=None):
        pass

    @abstractmethod
    def move(self, x, y):
        pass

    @abstractmethod
    def attack(self, target):
        pass
