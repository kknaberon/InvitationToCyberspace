"""3x3カードバトルのルール処理。"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import Iterable

from .cards import Card


# 盤面は3x3なので、マス数は9です。
BOARD_SIZE = 9

# 1行あたりのマス数です。positionから上下左右を計算するときに使います。
BOARD_WIDTH = 3


class Owner(str, Enum):
    """カードの所有者を表します。青がプレイヤー、赤がCPUです。"""

    # BLUE: プレイヤー側の色です。
    BLUE = "blue"

    # RED: 相手CPU側の色です。
    RED = "red"

    @property
    def opponent(self) -> "Owner":
        """自分とは反対側のプレイヤーを返します。"""

        return Owner.RED if self is Owner.BLUE else Owner.BLUE


@dataclass(frozen=True, slots=True)
class PlacedCard:
    """盤面に置かれているカードと、その現在の所有者。"""

    # card: 盤面に置かれたカードそのものです。
    card: Card

    # owner: このカードが現在どちらの色かを表します。捕獲されると変わります。
    owner: Owner


@dataclass(frozen=True, slots=True)
class Move:
    """1手分の行動。どの手札を、どのマスへ置くかを表します。"""

    # owner: この手を打つプレイヤーです。現在のturnと一致している必要があります。
    owner: Owner

    # hand_index: 手札リストの何番目のカードを出すかです。重複カード対策でIDではなく番号を使います。
    hand_index: int

    # position: 0から8の盤面位置です。左上が0、右下が8です。
    position: int


@dataclass(frozen=True, slots=True)
class BattleState:
    """カードバトルの現在状態。

    このクラスは「手を打つたびに新しい状態を返す」作りにしています。
    AI実験で過去状態を残したり、CSVへ状態を保存したりしやすくするためです。
    """

    # board: 9マス分の盤面です。Noneは空きマス、PlacedCardは配置済みカードです。
    board: tuple[PlacedCard | None, ...]

    # blue_hand: プレイヤー側の残り手札です。
    blue_hand: tuple[Card, ...]

    # red_hand: CPU側の残り手札です。
    red_hand: tuple[Card, ...]

    # turn: 次に手を打つプレイヤーです。
    turn: Owner

    # first_player: 先攻がどちらだったかです。後攻ボーナスの判定に使います。
    first_player: Owner

    @classmethod
    def start(
        cls,
        blue_hand: Iterable[Card],
        red_hand: Iterable[Card],
        first_player: Owner | None = None,
        rng: random.Random | None = None,
    ) -> "BattleState":
        """初期状態を作ります。先攻未指定ならランダムに決めます。"""

        # rng: 先攻ランダム決定を再現可能にするための乱数生成器です。
        rng = rng or random.Random()

        # first_player: 指定がなければ青/赤からランダムに選びます。
        first_player = first_player or rng.choice([Owner.BLUE, Owner.RED])

        # blue_cards/red_cards: Iterableで渡された手札を、変更されないtupleに固定します。
        blue_cards = tuple(blue_hand)
        red_cards = tuple(red_hand)

        # 企画書どおり、両者は5枚ずつ手札を持って開始します。
        if len(blue_cards) != 5 or len(red_cards) != 5:
            raise ValueError("Both players must start with exactly 5 cards")

        # boardは9マスすべて空の状態で開始します。
        return cls(
            board=(None,) * BOARD_SIZE,
            blue_hand=blue_cards,
            red_hand=red_cards,
            turn=first_player,
            first_player=first_player,
        )

    @property
    def second_player(self) -> Owner:
        """後攻プレイヤーを返します。"""

        return self.first_player.opponent

    @property
    def move_count(self) -> int:
        """現在までに盤面へ置かれたカード枚数を数えます。"""

        # Noneではないマスが、すでにカードで埋まっているマスです。
        return sum(cell is not None for cell in self.board)

    @property
    def is_over(self) -> bool:
        """盤面9マスがすべて埋まったかどうかを返します。"""

        return self.move_count == BOARD_SIZE

    def legal_moves(self) -> list[Move]:
        """現在の手番プレイヤーが選べる全合法手を返します。"""

        # ゲーム終了後は置ける場所がないため、合法手もありません。
        if self.is_over:
            return []

        # hand: 現在の手番プレイヤーの残り手札です。
        hand = self.hand_for_owner(self.turn)

        # empty_positions: まだカードが置かれていないマス番号一覧です。
        empty_positions = [index for index, cell in enumerate(self.board) if cell is None]

        # 手札の各カードと空きマスの全組み合わせが合法手になります。
        return [
            Move(self.turn, hand_index, position)
            for hand_index in range(len(hand))
            for position in empty_positions
        ]

    def random_legal_move(self, rng: random.Random | None = None) -> Move:
        """合法手の中からランダムに1手を選びます。Phase2のランダムAIでも使えます。"""

        rng = rng or random.Random()

        # moves: 現在選択可能な手の一覧です。
        moves = self.legal_moves()
        if not moves:
            raise ValueError("No legal moves are available")
        return rng.choice(moves)

    def hand_for_owner(self, owner: Owner) -> tuple[Card, ...]:
        """指定したプレイヤーの残り手札を返します。"""

        return self.blue_hand if owner is Owner.BLUE else self.red_hand

    def apply_move(self, move: Move) -> "BattleState":
        """1手を適用して、次のBattleStateを返します。"""

        # 終了済みのゲームには、これ以上カードを置けません。
        if self.is_over:
            raise ValueError("Battle is already over")

        # 手番でないプレイヤーが動こうとした場合はエラーにします。
        if move.owner is not self.turn:
            raise ValueError(f"It is {self.turn.value}'s turn, not {move.owner.value}'s")

        # positionは0から8までの盤面位置だけ許可します。
        if move.position < 0 or move.position >= BOARD_SIZE:
            raise ValueError(f"Position must be between 0 and 8, got {move.position}")

        # すでにカードがあるマスには置けません。
        if self.board[move.position] is not None:
            raise ValueError(f"Position {move.position} is already occupied")

        # hand: 現在動くプレイヤーの手札を、popできるよう一時的にlistへ変換します。
        hand = list(self.hand_for_owner(move.owner))

        # hand_indexは現在の手札範囲内である必要があります。
        if move.hand_index < 0 or move.hand_index >= len(hand):
            raise ValueError(f"Invalid hand index: {move.hand_index}")

        # card: 今回盤面に出すカードです。出したカードは手札から取り除きます。
        card = hand.pop(move.hand_index)

        # board: immutableなtupleから、更新用のlistに変換します。
        board = list(self.board)

        # 指定マスにカードを置きます。この時点では置いた本人の色です。
        board[move.position] = PlacedCard(card=card, owner=move.owner)

        # 隣接する相手カードと数値比較し、勝てる方向のカードを捕獲します。
        self._capture_neighbors(board, move.position, card, move.owner)

        # 動いた側だけ手札が1枚減るため、青/赤のどちらを更新するか分岐します。
        if move.owner is Owner.BLUE:
            blue_hand = tuple(hand)
            red_hand = self.red_hand
        else:
            blue_hand = self.blue_hand
            red_hand = tuple(hand)

        # 次の手番は必ず相手側です。
        return BattleState(
            board=tuple(board),
            blue_hand=blue_hand,
            red_hand=red_hand,
            turn=move.owner.opponent,
            first_player=self.first_player,
        )

    def score(self) -> dict[Owner, int]:
        """現在の青/赤の得点を数えます。終了時は後攻の未使用手札も加点します。"""

        # scores: 青と赤それぞれの枚数カウントです。
        scores = {Owner.BLUE: 0, Owner.RED: 0}

        # 盤面上のカードは、現在の所有者の点として数えます。
        for cell in self.board:
            if cell is not None:
                scores[cell.owner] += 1

        # 企画書どおり、後攻の盤面に出していない手札も最終枚数に含めます。
        # ゲーム途中で呼んでも一貫した値を返すため、常にこのルールを適用します。
        scores[self.second_player] += len(self.hand_for_owner(self.second_player))
        return scores

    def winner(self) -> Owner | None:
        """ゲーム終了後、勝者を返します。同点ならNoneです。"""

        # 盤面が埋まる前は勝敗未確定なので、呼び出しミスとしてエラーにします。
        if not self.is_over:
            raise ValueError("Winner is only available after the board is full")

        # scores: 後攻未使用手札を含めた最終スコアです。
        scores = self.score()
        if scores[Owner.BLUE] > scores[Owner.RED]:
            return Owner.BLUE
        if scores[Owner.RED] > scores[Owner.BLUE]:
            return Owner.RED
        return None

    @staticmethod
    def _capture_neighbors(
        board: list[PlacedCard | None],
        position: int,
        card: Card,
        owner: Owner,
    ) -> None:
        """置いたカードの上下左右を調べ、勝てる相手カードを捕獲します。"""

        # neighbor: 置いたカードから見た隣接マス情報です。
        for neighbor in _neighbors(position):
            # placed: 隣接マスに置かれているカードです。空きマスなら比較しません。
            placed = board[neighbor.position]
            if placed is None or placed.owner is owner:
                continue

            # attack_value: 今置いたカードの、隣接カードに接している面の数値です。
            attack_value = card.value_for_side(neighbor.own_side)

            # defense_value: 隣接する相手カードの、こちらに接している面の数値です。
            defense_value = placed.card.value_for_side(neighbor.neighbor_side)

            # 企画書どおり「自分の数値 > 相手の数値」の場合だけ捕獲します。
            if attack_value > defense_value:
                board[neighbor.position] = PlacedCard(card=placed.card, owner=owner)


@dataclass(frozen=True, slots=True)
class Neighbor:
    """あるマスから見た隣接マスと、比較する方向の組み合わせ。"""

    # position: 隣接マスの盤面位置です。
    position: int

    # own_side: 今置いたカード側で比較に使う方向です。
    own_side: str

    # neighbor_side: 隣接カード側で比較に使う方向です。
    neighbor_side: str


def play_random_battle(
    blue_hand: Iterable[Card],
    red_hand: Iterable[Card],
    first_player: Owner | None = None,
    rng: random.Random | None = None,
) -> BattleState:
    """両者ランダム行動で、バトルを最後まで進めます。"""

    # rng: ランダムな先攻決定や手選択を再現するための乱数生成器です。
    rng = rng or random.Random()

    # state: 現在のバトル状態です。apply_moveするたびに新しい状態へ差し替えます。
    state = BattleState.start(
        blue_hand=blue_hand,
        red_hand=red_hand,
        first_player=first_player,
        rng=rng,
    )

    # 盤面が9マス埋まるまで、合法手をランダムに選んで適用します。
    while not state.is_over:
        state = state.apply_move(state.random_legal_move(rng))
    return state


def _neighbors(position: int) -> list[Neighbor]:
    """指定マスの上下左右にある隣接マス情報を返します。"""

    # row/col: positionを3x3盤面の行・列に変換したものです。
    row, col = divmod(position, BOARD_WIDTH)

    # neighbors: 存在する隣接マスだけを追加していきます。盤面外は追加しません。
    neighbors: list[Neighbor] = []

    # 上にマスがある場合、今置いたカードのtopと、上カードのbottomを比較します。
    if row > 0:
        neighbors.append(Neighbor(position - BOARD_WIDTH, "top", "bottom"))

    # 右にマスがある場合、今置いたカードのrightと、右カードのleftを比較します。
    if col < BOARD_WIDTH - 1:
        neighbors.append(Neighbor(position + 1, "right", "left"))

    # 下にマスがある場合、今置いたカードのbottomと、下カードのtopを比較します。
    if row < BOARD_WIDTH - 1:
        neighbors.append(Neighbor(position + BOARD_WIDTH, "bottom", "top"))

    # 左にマスがある場合、今置いたカードのleftと、左カードのrightを比較します。
    if col > 0:
        neighbors.append(Neighbor(position - 1, "left", "right"))
    return neighbors
