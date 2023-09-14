class ChessPiece:
    def __init__(self, color, piece_id):
        self.color = color
        self.piece_id = piece_id


class Pawn(ChessPiece):
    def __init__(self, color, piece_id):
        super().__init__(color, piece_id)
        self.symbol = 'P' if color == 'white' else 'p'
        self.first_move = False


class Rook(ChessPiece):
    def __init__(self, color, piece_id):
        super().__init__(color, piece_id)
        self.symbol = 'R' if color == 'white' else 'r'
        self.first_move = False


class Bishop(ChessPiece):
    def __init__(self, color, piece_id):
        super().__init__(color, piece_id)
        self.symbol = 'B' if color == 'white' else 'b'


class Knight(ChessPiece):
    def __init__(self, color, piece_id):
        super().__init__(color, piece_id)
        self.symbol = 'N' if color == 'white' else 'n'


class Queen(ChessPiece):
    def __init__(self, color, piece_id):
        super().__init__(color, piece_id)
        self.symbol = 'Q' if color == 'white' else 'q'
        self.first_move = False


class King(ChessPiece):
    def __init__(self, color, piece_id):
        super().__init__(color, piece_id)
        self.symbol = 'K' if color == 'white' else 'k'
        self.first_move = False
