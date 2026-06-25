"""カード定義と、毎回同じ結果になるカードプール生成処理。"""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Iterable


# グレードごとの「上下左右すべての数値」の目標平均値。
# 企画書にある 0個一致=3.0、4個一致=8.2 などの強さ調整はここで管理します。
TARGET_GRADE_AVERAGES: dict[int, float] = {
    0: 3.0,
    1: 4.2,
    2: 5.4,
    3: 6.8,
    4: 8.2,
}

# 1グレードは20枚、1枚につき上下左右4値なので、平均計算の対象は80個です。
CARD_VALUES_PER_GRADE = 20 * 4


@dataclass(frozen=True, slots=True)
class Card:
    """上下左右に数値を持つ、トリプルトライアド風のカード。"""

    # card_id: プログラム上でカードを区別するためのIDです。
    card_id: str

    # name: 画面やCLIに表示するカード名です。あとで日本語名に差し替えできます。
    name: str

    # grade: 数当て結果に対応するカードの強さ帯です。0から4までを使います。
    grade: int

    # top/right/bottom/left: それぞれカードの上・右・下・左に書かれる数値です。
    top: int
    right: int
    bottom: int
    left: int

    def __post_init__(self) -> None:
        """カード生成直後に、グレードと数値範囲が正しいか確認します。"""

        # 未定義のグレードが混ざると、手札配布や平均計算が壊れるため弾きます。
        if self.grade not in TARGET_GRADE_AVERAGES:
            raise ValueError(f"Unsupported card grade: {self.grade}")

        # カードの各方向の数値は、企画書どおり1から10の範囲だけ許可します。
        for label, value in self.values_by_side().items():
            if value < 1 or value > 10:
                raise ValueError(f"{label} value must be between 1 and 10: {value}")

    def values_by_side(self) -> dict[str, int]:
        """方向名から数値を引ける辞書にして返します。"""

        return {
            "top": self.top,
            "right": self.right,
            "bottom": self.bottom,
            "left": self.left,
        }

    def value_for_side(self, side: str) -> int:
        """'top' などの方向名を指定して、その方向の数値を取得します。"""

        try:
            return self.values_by_side()[side]
        except KeyError as exc:
            raise ValueError(f"Unknown side: {side}") from exc


@dataclass(frozen=True, slots=True)
class CardPool:
    """100枚すべてのカードと、手札を引くための便利処理をまとめたクラス。"""

    # cards: グレード0から4まで、各20枚ずつ入った全カード一覧です。
    cards: tuple[Card, ...]

    def __post_init__(self) -> None:
        """カードプールが企画書どおりの枚数構成か確認します。"""

        # 全体枚数は 5グレード * 20枚 = 100枚で固定です。
        if len(self.cards) != 100:
            raise ValueError(f"Card pool must contain 100 cards, got {len(self.cards)}")

        # グレードごとの枚数も、必ず20枚ずつあることを保証します。
        for grade in TARGET_GRADE_AVERAGES:
            count = len(self.cards_for_grade(grade))
            if count != 20:
                raise ValueError(f"Grade {grade} must contain 20 cards, got {count}")

    def cards_for_grade(self, grade: int) -> tuple[Card, ...]:
        """指定したグレードのカード20枚だけを取り出します。"""

        if grade not in TARGET_GRADE_AVERAGES:
            raise ValueError(f"Unsupported card grade: {grade}")
        return tuple(card for card in self.cards if card.grade == grade)

    def average_for_grade(self, grade: int) -> float:
        """指定グレードの上下左右80個の数値平均を計算します。"""

        # values: 指定グレード20枚分の top/right/bottom/left を平らに並べたリストです。
        values = _flatten_values(self.cards_for_grade(grade))
        return sum(values) / len(values)

    def average_all_values(self) -> float:
        """全100枚、400個の方向数値の平均を計算します。CPU期待値の確認に使えます。"""

        # values: 全カード100枚分の top/right/bottom/left を平らに並べたリストです。
        values = _flatten_values(self.cards)
        return sum(values) / len(values)

    def draw_player_hand(
        self,
        grade: int,
        rng: random.Random | None = None,
        count: int = 5,
    ) -> list[Card]:
        """プレイヤー用に、指定グレードのカードから5枚引きます。重複ありです。"""

        # rng: 乱数生成器です。テストやAI実験で同じ結果を再現したいときにseedを渡します。
        rng = rng or random.Random()

        # grade_cards: 数当て結果のグレードに対応する20枚だけを候補にします。
        grade_cards = self.cards_for_grade(grade)
        return [rng.choice(grade_cards) for _ in range(count)]

    def draw_cpu_hand(
        self,
        rng: random.Random | None = None,
        count: int = 5,
    ) -> list[Card]:
        """CPU用に、全100枚から5枚引きます。ここでは重複なしです。"""

        # rng.sample は同じカードを2回選ばないため、CPU手札は5枚すべて別カードになります。
        rng = rng or random.Random()
        return rng.sample(list(self.cards), count)


def build_default_card_pool(seed: int = 2026) -> CardPool:
    """目標平均値どおりの100枚カードプールを作ります。"""

    # cards: 最終的にCardPoolへ渡す100枚分のカードリストです。
    cards: list[Card] = []

    # grade: 0から4のカードグレードです。
    # target_average: そのグレードの80個の方向数値が目指す平均値です。
    for grade, target_average in TARGET_GRADE_AVERAGES.items():
        # values: 20枚 * 4方向 = 80個分の数値です。
        # seed + grade にしておくと、グレードごとに違う並びを安定生成できます。
        values = _build_grade_values(target_average, random.Random(seed + grade))

        # index: グレード内で何枚目のカードかを表します。0始まりなので表示時は+1します。
        for index in range(20):
            # 80個の数値を4個ずつ切り出して、1枚のカードにします。
            top, right, bottom, left = values[index * 4 : index * 4 + 4]
            cards.append(
                Card(
                    card_id=f"G{grade}-{index + 1:02d}",
                    name=f"Grade {grade} Card {index + 1:02d}",
                    grade=grade,
                    top=top,
                    right=right,
                    bottom=bottom,
                    left=left,
                )
            )
    return CardPool(tuple(cards))


def _build_grade_values(target_average: float, rng: random.Random) -> list[int]:
    """1グレード80個分の方向数値を、指定平均ぴったりになるよう生成します。"""

    # target_sum: 80個の数値を全部足したときに目指す合計値です。
    # 例: 平均3.0なら 3.0 * 80 = 240 になります。
    target_sum = round(target_average * CARD_VALUES_PER_GRADE)

    # base: まず全マスに置く基準値です。平均4.2なら、最初は全部4にします。
    base = math.floor(target_average)

    # values: 1グレード内の「方向数値80個」を表します。まだカード単位には分けていません。
    values = [base] * CARD_VALUES_PER_GRADE

    # remainder: 目標合計に届かせるため、baseから+1する個数です。
    # 平均4.2なら 336 - (4 * 80) = 16 個を5にします。
    remainder = target_sum - (base * CARD_VALUES_PER_GRADE)
    for index in rng.sample(range(CARD_VALUES_PER_GRADE), remainder):
        values[index] += 1

    # 合計値は変えずに、強い方向と弱い方向の偏りを作ります。
    # これにより「平均は弱いが上だけ9」みたいなカード個性が出ます。
    for _ in range(240):
        # high_index: 数値を上げる場所、low_index: 同じ分だけ数値を下げる場所です。
        high_index, low_index = rng.sample(range(CARD_VALUES_PER_GRADE), 2)

        # max_delta: 1から10の範囲を超えず、かつ1回で極端に動かしすぎない上限です。
        max_delta = min(10 - values[high_index], values[low_index] - 1, 3)
        if max_delta <= 0:
            continue

        # delta: high側へ移す点数です。low側から同じ点数を引くので合計は変わりません。
        delta = rng.randint(1, max_delta)
        values[high_index] += delta
        values[low_index] -= delta

    # カード化したときの並びが単調にならないよう、最後に順番だけ混ぜます。
    rng.shuffle(values)

    # 念のため、偏り作成後も目標合計が守られているか確認します。
    if sum(values) != target_sum:
        raise RuntimeError("Card generation failed to preserve target average")
    return values


def _flatten_values(cards: Iterable[Card]) -> list[int]:
    """カード一覧から、上下左右の数値だけを1本のリストにして返します。"""

    # values: 平均値計算のために、カードの方向数値を順番に追加していくリストです。
    values: list[int] = []
    for card in cards:
        values.extend((card.top, card.right, card.bottom, card.left))
    return values
