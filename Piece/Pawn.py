from Enum import Color
from Piece import Piece


class Pawn(Piece):
    def __init__(self, id_: int, color: Color, x: int, y: int):
        super().__init__(id_, color, x, y)

    def valid_move_list(self, target: Piece = None):
        # 폰의 이동 규칙을 구현합니다.
        moves = []

        if self.color == Color.WHITE:
            # 흰색 폰은 위로 이동
            if self.y == 1:
                # 첫 번째 이동일 경우 1칸 또는 2칸 전진 가능
                moves.append((self.x, self.y + 1))
                moves.append((self.x, self.y + 2))
            else:
                # 첫 번째 이동이 아닐 경우 1칸 전진 가능
                moves.append((self.x, self.y + 1))

            # 대각선으로 적군을 공격
            moves.append((self.x - 1, self.y + 1))
            moves.append((self.x + 1, self.y + 1))
        else:
            # 흑색 폰은 아래로 이동
            if self.y == 6:
                # 첫 번째 이동일 경우 1칸 또는 2칸 전진 가능
                moves.append((self.x, self.y - 1))
                moves.append((self.x, self.y - 2))
            else:
                # 첫 번째 이동이 아닐 경우 1칸 전진 가능
                moves.append((self.x, self.y - 1))

        if target is not None:
            # 대각선으로 적군을 공격
            moves.append((self.x - 1, self.y - 1))
            moves.append((self.x + 1, self.y - 1))

        return moves

    def is_valid_move(self, x: int = None, y: int = None, target: Piece = None):
        # 이동이 유효한지 확인합니다.
        if Piece is not None:
            return (target.x, target.y) in self.valid_move_list(target=target)
        else:
            return (x, y) in self.valid_move_list()

    def move(self, x: int, y: int):
        # 폰을 새로운 위치로 이동합니다.
        if self.is_valid_move(x=x, y=y):
            self.x = x
            self.y = y

    def live(self):
        # 폰의 생존 여부를 반환합니다.
        return self.live

    def attack(self, target: Piece):
        # 적군을 공격합니다. (대각선으로 이동한 경우)
        if self.is_valid_move(target=target) and self.color != target.color:
            target.live = False
