import chess
import chess.svg
import numpy as np
import config


class Node:
    def __init__(self, board):
        self.board = board
        self.edges = []

    def is_leaf(self):
        return not self.edges


class Edge:
    def __init__(self, in_node, out_node, action, prior):
        self.id = in_node.state.id + '>' + out_node.state.id
        self.inNode = in_node
        self.outNode = out_node
        self.action = action
        self.playerTurn = in_node.state.playerTurn
        self.stats = {
            'N': 0,
            'W': 0,
            'Q': 0,
            'P': prior,
        }


class MCTS:
    def __init__(self, root: Node, cpuct):
        self.root = root
        self.tree = {}
        self.cpuct = cpuct
        self.add_node(root)

    def __str__(self):
        return len(self.tree)

    def move_to_leaf(self):
        breadcrumbs = []
        current_node = self.root
        done = 0
        value = 0

        while not current_node.is_leaf():
            legal_moves = list(current_node.board.legal_moves)

            if current_node == self.root:
                epsilon = config.EPSILON
                nu = np.random.dirichlet([config.ALPHA] * len(legal_moves))
            else:
                epsilon = 0
                nu = [0] * len(legal_moves)

            Nb = 0
            for edge in current_node.edges:
                Nb += edge.stats['N']

            maxQU = -99999
            for idx, action in enumerate(legal_moves):
                edge = current_node.edges[idx]

                U = self.cpuct * (
                        (1 - epsilon) * edge.stats['P'] + epsilon * nu[idx]
                ) * (np.sqrt(Nb) / (1 + edge.stats['N']))

                Q = edge.stats['Q']

                if Q + U > maxQU:
                    maxQU = Q + U
                    simulation_action = action
                    simulation_edge = edge

            new_board = current_node.board.copy()
            new_board.push(simulation_action)
            value, done = self.evaluate_board(new_board)

            current_node = simulation_edge.outNode
            breadcrumbs.append(simulation_edge)

        return current_node, value, done, breadcrumbs

    def back_fill(self, leaf, value, breadcrumbs):
        current_player = chess.WHITE if leaf.board.turn == chess.BLACK else chess.BLACK

        for edge in breadcrumbs:
            player_turn = edge.outNode.board.turn

            if player_turn == current_player:
                direction = 1
            else:
                direction = -1

            edge.stats['N'] += 1
            edge.stats['W'] += value * direction
            edge.stats['Q'] = edge.stats['W'] / edge.stats['N']

    def add_node(self, node):
        self.tree[node.board.fen()] = node

    def evaluate_board(self, board):
        # 초기 평가 점수
        score = 0

        # 각 말의 상대적 가치 설정
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }

        # 게임 보드를 스캔하며 각 말의 상대적 가치를 계산
        for square, piece in board.piece_map().items():
            if piece.color == chess.WHITE:
                score += piece_values.get(piece.piece_type, 0)
            else:
                score -= piece_values.get(piece.piece_type, 0)

        # 게임 종료 여부 확인
        done = None
        if board.is_checkmate():
            # 체크메이트인 경우, 승패 결정
            if board.turn == chess.WHITE:
                done = -1  # 검은색 승리
                score = -np.inf
            else:
                done = 1  # 흰색 승리
                score = np.inf

        elif board.is_stalemate() or board.is_insufficient_material() or \
                board.can_claim_draw() or board.can_claim_fifty_moves() or \
                (board.halfmove_clock >= config.DRAW_HALFMOVE_CLOCK):

            done = True  # 무승부
            score = 0

        return score, done


