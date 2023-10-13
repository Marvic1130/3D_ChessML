import chess
import numpy as np
from Utils import config


class Node:
    def __init__(self, board):
        # Node 클래스는 게임 보드를 나타내는 노드를 생성.
        self.board = board
        self.edges = []

    def is_leaf(self):
        # 해당 노드가 리프 노드인지 확인. (자식 노드가 없는 경우 리프 노드)
        return not self.edges


class Edge:
    def __init__(self, in_node, out_node, action, prior):
        # Edge 클래스는 게임 보드 간의 움직임을 나타낸다.
        self.id = in_node.state.id + '>' + out_node.state.id  # 엣지의 고유 ID
        self.inNode = in_node  # 시작 노드
        self.outNode = out_node  # 도착 노드
        self.action = action  # 적용된 동작 (체스 움직임)
        self.playerTurn = in_node.state.playerTurn  # 움직인 플레이어
        self.stats = {
            'N': 0,  # 방문 횟수
            'W': 0,  # 이긴 횟수 또는 누적 보상
            'Q': 0,  # 평균 보상
            'P': prior,  # 사전 확률
        }


class MCTS:
    def __init__(self, root: Node, cpuct):
        self.root = root  # MCTS 트리의 루트 노드
        self.tree = {}  # 트리 구조를 저장하기 위한 딕셔너리
        self.cpuct = cpuct  # 탐색 정도 조절에 사용되는 상수
        self.add_node(root)

    def __str__(self):
        return len(self.tree)

    def move_to_leaf(self):
        # MCTS 탐색 단계에서 리프 노드까지 이동하는 함수
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

            Nb = 0  # 현재 노드의 모든 엣지의 방문 횟수 합계
            for edge in current_node.edges:
                Nb += edge.stats['N']

            maxQU = -99999  # 선택할 엣지의 가치와 불확실성의 합의 최댓값
            for idx, action in enumerate(legal_moves):
                edge = current_node.edges[idx]
                # U: 엣지 선택에 대한 불확실성, Q: 엣지 선택에 대한 가치
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

    def backpropagation(self, leaf, value, breadcrumbs):
        # 리프에서 시작하여 루트까지 이동하면서 엣지 정보를 업데이트하는 함수, 역전파
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
        # 트리에 노드를 추가하는 함수
        self.tree[node.board.fen()] = node

    def evaluate_board(self, board):
        # 게임 보드를 평가하고 승패 또는 무승부를 확인하는 함수
        score = 0  # 초기 평가 점수

        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }

        for square, piece in board.piece_map().items():
            # 게임 보드를 스캔하며 각 말의 상대적 가치를 계산
            if piece.color == chess.WHITE:
                score += piece_values.get(piece.piece_type, 0)
            else:
                score -= piece_values.get(piece.piece_type, 0)

        done = None  # 게임 종료 여부 확인 변수
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
