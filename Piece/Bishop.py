from Enum import Color
from Piece import Piece


class Bishop(Piece):
    def __init__(self, id_: int, color: Color, x: int, y: int):
        super().__init__(id_, color, x, y)

    def valid_move_list(self, target: Piece = None):
        # 비숍의 이동 규칙을 구현합니다.
        moves = []

        for i in range(1, 8):
            if self.x + i < 8 and self.y + i < 8:
                moves.append((self.x + i, self.y + i))
            if self.x + i < 8 and self.y - i >= 0:
                moves.append((self.x + i, self.y - i))
            if self.x - i >= 0 and self.y + i < 8:
                moves.append((self.x - i, self.y + i))
            if self.x - i >= 0 and self.y - i >= 0:
                moves.append((self.x - i, self.y - i))

        return moves

    def is_valid_move(self, x: int = None, y: int = None, target: Piece = None):
        # 이동이 유효한지 확인합니다.
        return (x, y) in self.valid_move_list()

    def move(self, x: int, y: int):
        # 비숍을 새로운 위치로 이동합니다.
        if self.is_valid_move(x=x, y=y):
            self.x = x
            self.y = y

    def attack(self, target: Piece):
        # 적군을 공격합니다.
        if self.is_valid_move(target=target) and self.color != target.color:
            target.live = False
