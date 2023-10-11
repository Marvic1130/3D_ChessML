import chess
import random
import math


class Node:
    def __init__(self, state: chess.Board):
        self.state = state
        self.parent = None
        self.children = []
        self.wins = 0  # 승리 횟수
        self.visits = 0  # 방문 횟수
        self.untried_moves = None


def select(node):
    if not node.untried_moves and node.children:
        # 모든 하위 노드가 확장되었을 때, UCB를 사용하여 최선의 하위 노드를 선택.
        exploration_weight = math.sqrt(2)  # 탐색 가중치
        best_child = None
        best_ucb_score = float("-inf")

        for child in node.children:
            if child.visits == 0:
                ucb = float("inf")  # 방문하지 않은 노드에 높은 우선순위 부여
            else:
                exploitation_term = child.wins / child.visits  # 이용 부분
                ucb = exploitation_term + exploration_weight * math.sqrt(math.log(node.visits) / child.visits)

            if ucb > best_ucb_score:
                best_ucb_score = ucb
                best_child = child

        return best_child  # 가장 높은 UCB 스코어를 가진 하위 노드 반환

    # 모든 하위 노드가 확장되지 않았거나 UCB가 하위 노드를 선택하지 않은 경우, 시도하지 않은 움직임을 선택.
    if not node.untried_moves:
        return None  # 모든 움직임을 시도한 경우, 선택 가능한 하위 노드가 없음

    move = random.choice(node.untried_moves)  # 랜덤으로 시도하지 않은 움직임 선택
    new_state = node.state.copy()
    new_state.push(move)
    new_node = Node(new_state)
    new_node.untried_moves = [m for m in node.untried_moves if m != move]
    new_node.parent = node
    node.children.append(new_node)
    return new_node  # 새로운 노드 반환


def expand(node):
    if not node.untried_moves:
        return

    untried_moves = node.untried_moves.copy()  # 모든 아직 시도하지 않은 움직임 복사

    for move in untried_moves:
        new_state = node.state.copy()
        new_state.push(move)
        new_node = Node(new_state)
        new_node.parent = node
        node.children.append(new_node)

    node.untried_moves = []  # 확장 후 untried_moves 초기화


def simulate(node):
    state = node.state.copy()

    while not state.is_game_over():
        legal_moves = list(state.legal_moves)
        move = random.choice(legal_moves)
        state.push(move)

    # 게임 결과를 평가. 승리(1), 패배(-1), 무승부(0).
    if state.is_checkmate():
        if state.turn == chess.WHITE:
            return -1  # 검은색(Black)이 승리
        else:
            return 1  # 흰색(White)이 승리
    else:
        return 0  # 무승부


def backpropagate(node, score):
    while node:
        node.visits += 1
        node.wins += score  # 게임 결과 업데이트.

        # 결과 반전.
        score *= -1

        node = node.parent


def ucb_score(node, epsilon=1e-6):
    if not node.visits:
        return float('inf')

    exploration_factor = math.sqrt(2)  # 탐색과 이용 사이의 균형을 조절하는 하이퍼파라미터. 조정 가능.

    exploitation_term = node.wins / node.visits  # 이용 부분

    # UCB 스코어 계산: 이용 부분 + 탐색 부분
    ucb = exploitation_term + exploration_factor * math.sqrt(math.log(node.visits + 1) / (node.visits + epsilon))

    return ucb


def mcts_search(root_state, num_iterations):
    root_node = Node(root_state)

    for _ in range(num_iterations):
        selected_node = select(root_node)

        if not selected_node:
            break  # 선택 가능한 노드가 없다면 종료

        if not selected_node.state.is_game_over():
            expand(selected_node)
            selected_node = random.choice(selected_node.children)

        result = simulate(selected_node)  # selected_node를 인수로 전달

        backpropagate(selected_node, result)

    # 가장 방문 횟수가 높은 자식 노드 중에서 선택
    best_child = max(root_node.children, key=lambda child: child.visits)

    return best_child.state  # 최선의 자식 노드 반환
