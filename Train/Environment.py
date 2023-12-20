import chess
import numpy as np


class ChessEnvironment:
    def __init__(self):
        self.board = chess.Board()

    def reset(self):
        self.board.reset()
        return self.get_state()

    def step(self, action):
        move = chess.Move.from_uci(action)

        reward = 0
        done = False

        if move in self.board.legal_moves:
            self.board.push(move)

            if self.board.is_checkmate():
                reward = 1 if self.board.turn else -1
                done = True
            elif self.board.is_stalemate() or \
                    self.board.is_insufficient_material() or \
                    self.board.can_claim_draw() or \
                    self.board.can_claim_fifty_moves():
                reward = 0
                done = True

            else:
                reward = 0

        else:
            # illegal move penalty
            reward = -1

        return self.get_state(), reward, done

    def get_state(self):
        # Initialize a zero array of shape (8, 8, 13)
        state = np.zeros((8, 8, 13), dtype=int)

        # For each square on the board
        for i in range(64):
            piece = self.board.piece_at(i)

            if piece is not None:
                # Get the piece color (0 for white and 1 for black)
                color = int(piece.color)

                # Get the piece type (from chess.PAWN to chess.KING maps to indices from 0 to 5)
                piece_type = piece.piece_type - 1

                # Update the state array with the piece information
                state[i // 8][i % 8][color * 6 + piece_type] = 1

            else:
                # If there's no piece at this square then mark it as empty
                state[i // 8][i % 8][12] = 1

        return state

