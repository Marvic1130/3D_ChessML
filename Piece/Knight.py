from Enum.Color import Color
from Piece import Piece


class Knight(Piece):
    def __init__(self, id_: int, color: Color, x: int, y: int):
        super().__init__(id_, color, x, y)

    def valid_move_list(self, target: Piece = None):
        # 나이트의 이동 규칙을 구현합니다.
        moves = []

        potential_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                           (-2, -1), (-1, -2), (1, -2), (2, -1)]

        for dx, dy in potential_moves:
            new_x = self.x + dx
            new_y = self.y + dy

            if -1 < new_x < 8 and -1 < new_y < 8:
                moves.append((new_x, new_y))

        return moves

    def is_valid_move(self, x: int = None, y: int = None, target: Piece = None):
        # 이동이 유효한지 확인합니다.
        return (x, y) in self.valid_move_list()

    def move(self, x: int, y: int):

        if self.is_valid_move(x=x, y=y):
            self.x = x
            self.y = y

    def attack(self, target: Piece):
        # 적군을 공격합니다.
        if target is not None and target.color != self.color and (target.x, target.y) in self.valid_move_list():
            target.live = False
