"""カード定義と、毎回同じ結果になるカードプール生成処理。"""

from __future__ import annotations

from dataclasses import dataclass
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

# カード定義の並びは以下の順番です。
# (カードID, カード名, グレード, 上, 右, 下, 左)
#
# ここを直接編集すれば、カード名や上下左右の強さを手で調整できます。
# ただし、グレードごとの平均値を企画書どおりに保ちたい場合は、
# 各グレード20枚 * 4方向 = 80個の数値平均に注意してください。
CARD_DEFINITIONS: list[tuple[str, str, int, int, int, int, int]] = [
    # グレード0: 80か所の平均 3.0
    ("G0-01", "Grade 0 Card 01", 0, 9, 1, 1, 1),
    ("G0-02", "Grade 0 Card 02", 0, 1, 9, 1, 1),
    ("G0-03", "Grade 0 Card 03", 0, 1, 1, 9, 1),
    ("G0-04", "Grade 0 Card 04", 0, 1, 1, 1, 9),
    ("G0-05", "Grade 0 Card 05", 0, 6, 2, 2, 2),
    ("G0-06", "Grade 0 Card 06", 0, 2, 6, 2, 2),
    ("G0-07", "Grade 0 Card 07", 0, 2, 2, 6, 2),
    ("G0-08", "Grade 0 Card 08", 0, 2, 2, 2, 6),
    ("G0-09", "Grade 0 Card 09", 0, 3, 3, 3, 3),
    ("G0-10", "Grade 0 Card 10", 0, 4, 3, 2, 3),
    ("G0-11", "Grade 0 Card 11", 0, 3, 4, 3, 2),
    ("G0-12", "Grade 0 Card 12", 0, 2, 3, 4, 3),
    ("G0-13", "Grade 0 Card 13", 0, 3, 2, 3, 4),
    ("G0-14", "Grade 0 Card 14", 0, 5, 1, 5, 1),
    ("G0-15", "Grade 0 Card 15", 0, 1, 5, 1, 5),
    ("G0-16", "Grade 0 Card 16", 0, 7, 1, 2, 2),
    ("G0-17", "Grade 0 Card 17", 0, 2, 7, 1, 2),
    ("G0-18", "Grade 0 Card 18", 0, 2, 2, 7, 1),
    ("G0-19", "Grade 0 Card 19", 0, 1, 2, 2, 7),
    ("G0-20", "Grade 0 Card 20", 0, 4, 4, 2, 2),

    # グレード1: 80か所の平均 4.2
    ("G1-01", "Grade 1 Card 01", 1, 8, 3, 3, 3),
    ("G1-02", "Grade 1 Card 02", 1, 3, 8, 3, 3),
    ("G1-03", "Grade 1 Card 03", 1, 3, 3, 8, 3),
    ("G1-04", "Grade 1 Card 04", 1, 3, 3, 3, 8),
    ("G1-05", "Grade 1 Card 05", 1, 6, 4, 4, 3),
    ("G1-06", "Grade 1 Card 06", 1, 3, 6, 4, 4),
    ("G1-07", "Grade 1 Card 07", 1, 4, 3, 6, 4),
    ("G1-08", "Grade 1 Card 08", 1, 4, 4, 3, 6),
    ("G1-09", "Grade 1 Card 09", 1, 5, 5, 4, 3),
    ("G1-10", "Grade 1 Card 10", 1, 3, 5, 5, 4),
    ("G1-11", "Grade 1 Card 11", 1, 4, 3, 5, 5),
    ("G1-12", "Grade 1 Card 12", 1, 5, 4, 3, 5),
    ("G1-13", "Grade 1 Card 13", 1, 7, 2, 5, 3),
    ("G1-14", "Grade 1 Card 14", 1, 3, 7, 2, 5),
    ("G1-15", "Grade 1 Card 15", 1, 5, 3, 7, 2),
    ("G1-16", "Grade 1 Card 16", 1, 2, 5, 3, 7),
    ("G1-17", "Grade 1 Card 17", 1, 4, 4, 4, 4),
    ("G1-18", "Grade 1 Card 18", 1, 7, 3, 3, 3),
    ("G1-19", "Grade 1 Card 19", 1, 3, 7, 3, 3),
    ("G1-20", "Grade 1 Card 20", 1, 3, 3, 7, 3),

    # グレード2: 80か所の平均 5.4
    ("G2-01", "Grade 2 Card 01", 2, 9, 5, 4, 4),
    ("G2-02", "Grade 2 Card 02", 2, 4, 9, 5, 4),
    ("G2-03", "Grade 2 Card 03", 2, 4, 4, 9, 5),
    ("G2-04", "Grade 2 Card 04", 2, 5, 4, 4, 9),
    ("G2-05", "Grade 2 Card 05", 2, 7, 6, 5, 4),
    ("G2-06", "Grade 2 Card 06", 2, 4, 7, 6, 5),
    ("G2-07", "Grade 2 Card 07", 2, 5, 4, 7, 6),
    ("G2-08", "Grade 2 Card 08", 2, 6, 5, 4, 7),
    ("G2-09", "Grade 2 Card 09", 2, 8, 3, 8, 3),
    ("G2-10", "Grade 2 Card 10", 2, 3, 8, 3, 8),
    ("G2-11", "Grade 2 Card 11", 2, 6, 6, 5, 5),
    ("G2-12", "Grade 2 Card 12", 2, 10, 4, 4, 4),
    ("G2-13", "Grade 2 Card 13", 2, 6, 5, 5, 5),
    ("G2-14", "Grade 2 Card 14", 2, 8, 5, 4, 4),
    ("G2-15", "Grade 2 Card 15", 2, 4, 8, 5, 4),
    ("G2-16", "Grade 2 Card 16", 2, 4, 4, 8, 5),
    ("G2-17", "Grade 2 Card 17", 2, 5, 4, 4, 8),
    ("G2-18", "Grade 2 Card 18", 2, 7, 7, 4, 3),
    ("G2-19", "Grade 2 Card 19", 2, 3, 7, 7, 4),
    ("G2-20", "Grade 2 Card 20", 2, 4, 3, 7, 7),

    # グレード3: 80か所の平均 6.8
    ("G3-01", "Grade 3 Card 01", 3, 10, 7, 6, 5),
    ("G3-02", "Grade 3 Card 02", 3, 5, 10, 7, 6),
    ("G3-03", "Grade 3 Card 03", 3, 6, 5, 10, 7),
    ("G3-04", "Grade 3 Card 04", 3, 7, 6, 5, 10),
    ("G3-05", "Grade 3 Card 05", 3, 9, 7, 6, 5),
    ("G3-06", "Grade 3 Card 06", 3, 5, 9, 7, 6),
    ("G3-07", "Grade 3 Card 07", 3, 6, 5, 9, 7),
    ("G3-08", "Grade 3 Card 08", 3, 7, 6, 5, 9),
    ("G3-09", "Grade 3 Card 09", 3, 8, 8, 6, 5),
    ("G3-10", "Grade 3 Card 10", 3, 5, 8, 8, 6),
    ("G3-11", "Grade 3 Card 11", 3, 6, 5, 8, 8),
    ("G3-12", "Grade 3 Card 12", 3, 8, 6, 5, 8),
    ("G3-13", "Grade 3 Card 13", 3, 10, 4, 9, 4),
    ("G3-14", "Grade 3 Card 14", 3, 4, 10, 4, 9),
    ("G3-15", "Grade 3 Card 15", 3, 9, 4, 10, 4),
    ("G3-16", "Grade 3 Card 16", 3, 4, 9, 4, 10),
    ("G3-17", "Grade 3 Card 17", 3, 7, 7, 7, 6),
    ("G3-18", "Grade 3 Card 18", 3, 6, 7, 7, 7),
    ("G3-19", "Grade 3 Card 19", 3, 8, 7, 6, 6),
    ("G3-20", "Grade 3 Card 20", 3, 6, 8, 7, 6),

    # グレード4: 80か所の平均 8.2
    ("G4-01", "Grade 4 Card 01", 4, 10, 9, 8, 6),
    ("G4-02", "Grade 4 Card 02", 4, 6, 10, 9, 8),
    ("G4-03", "Grade 4 Card 03", 4, 8, 6, 10, 9),
    ("G4-04", "Grade 4 Card 04", 4, 9, 8, 6, 10),
    ("G4-05", "Grade 4 Card 05", 4, 10, 10, 7, 6),
    ("G4-06", "Grade 4 Card 06", 4, 6, 10, 10, 7),
    ("G4-07", "Grade 4 Card 07", 4, 7, 6, 10, 10),
    ("G4-08", "Grade 4 Card 08", 4, 10, 7, 6, 10),
    ("G4-09", "Grade 4 Card 09", 4, 9, 9, 8, 7),
    ("G4-10", "Grade 4 Card 10", 4, 7, 9, 9, 8),
    ("G4-11", "Grade 4 Card 11", 4, 8, 7, 9, 9),
    ("G4-12", "Grade 4 Card 12", 4, 9, 8, 7, 9),
    ("G4-13", "Grade 4 Card 13", 4, 10, 8, 10, 5),
    ("G4-14", "Grade 4 Card 14", 4, 5, 10, 8, 10),
    ("G4-15", "Grade 4 Card 15", 4, 10, 5, 10, 8),
    ("G4-16", "Grade 4 Card 16", 4, 8, 10, 5, 10),
    ("G4-17", "Grade 4 Card 17", 4, 8, 8, 8, 8),
    ("G4-18", "Grade 4 Card 18", 4, 10, 9, 7, 6),
    ("G4-19", "Grade 4 Card 19", 4, 6, 10, 9, 7),
    ("G4-20", "Grade 4 Card 20", 4, 7, 6, 10, 9),
]


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
    """定数として定義した100枚カードプールを作ります。"""

    # seed: 以前の自動生成版との互換性のために引数だけ残しています。
    # 今はCARD_DEFINITIONSをそのまま使うので、値を変えてもカード内容は変わりません。
    _ = seed

    # cards: CARD_DEFINITIONSのタプルをCardクラスへ変換した100枚分のリストです。
    cards = [
        Card(
            card_id=card_id,
            name=name,
            grade=grade,
            top=top,
            right=right,
            bottom=bottom,
            left=left,
        )
        for card_id, name, grade, top, right, bottom, left in CARD_DEFINITIONS
    ]
    return CardPool(tuple(cards))


def _flatten_values(cards: Iterable[Card]) -> list[int]:
    """カード一覧から、上下左右の数値だけを1本のリストにして返します。"""

    # values: 平均値計算のために、カードの方向数値を順番に追加していくリストです。
    values: list[int] = []
    for card in cards:
        values.extend((card.top, card.right, card.bottom, card.left))
    return values
