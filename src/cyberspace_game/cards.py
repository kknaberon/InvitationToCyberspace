"""カード定義と、毎回同じ結果になるカードプール生成処理。"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable


# グレードごとの「上下左右すべての数値」の目標平均値。
# 0個一致と4個一致はWeb版の難易度調整に合わせて少し寄せています。
TARGET_GRADE_AVERAGES: dict[int, float] = {
    0: 3.5,
    1: 4.2,
    2: 5.4,
    3: 6.8,
    4: 7.2,
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
    # グレード0: 80か所の平均 3.5
    ("G0-01", "薄闇/鍵音", 0, 9, 2, 2, 1),
    ("G0-02", "駅裏/白息", 0, 1, 9, 2, 2),
    ("G0-03", "湿った/切符", 0, 2, 1, 9, 2),
    ("G0-04", "消灯/路地", 0, 2, 2, 1, 9),
    ("G0-05", "深夜/改札", 0, 6, 3, 3, 2),
    ("G0-06", "古傷/写真", 0, 2, 6, 3, 3),
    ("G0-07", "雨傘/忘れ物", 0, 3, 2, 6, 3),
    ("G0-08", "黒電話/呼出", 0, 3, 3, 2, 6),
    ("G0-09", "段差/影", 0, 4, 4, 3, 3),
    ("G0-10", "作業灯/火花", 0, 5, 3, 3, 3),
    ("G0-11", "赤信号/無音", 0, 3, 5, 3, 3),
    ("G0-12", "終電/遅延", 0, 3, 3, 5, 3),
    ("G0-13", "袖口/血痕", 0, 3, 3, 3, 5),
    ("G0-14", "鍵束/鈍色", 0, 5, 2, 5, 2),
    ("G0-15", "非常口/青灯", 0, 2, 5, 2, 5),
    ("G0-16", "地下道/靴音", 0, 7, 2, 3, 2),
    ("G0-17", "空室/番号", 0, 2, 7, 2, 3),
    ("G0-18", "窓際/冷気", 0, 3, 2, 7, 2),
    ("G0-19", "手紙/封印", 0, 2, 3, 2, 7),
    ("G0-20", "遠雷/予感", 0, 4, 4, 3, 3),

    # グレード1: 80か所の平均 4.2
    ("G1-01", "夜勤/警告", 1, 8, 3, 3, 3),
    ("G1-02", "廃線/灯り", 1, 3, 8, 3, 3),
    ("G1-03", "追跡/足音", 1, 3, 3, 8, 3),
    ("G1-04", "暗証/手帳", 1, 3, 3, 3, 8),
    ("G1-05", "白線/停止", 1, 6, 4, 4, 3),
    ("G1-06", "裏口/合図", 1, 3, 6, 4, 4),
    ("G1-07", "焦げ跡/工具", 1, 4, 3, 6, 4),
    ("G1-08", "録音/雑音", 1, 4, 4, 3, 6),
    ("G1-09", "保留音/迷路", 1, 5, 5, 4, 3),
    ("G1-10", "密室/換気", 1, 3, 5, 5, 4),
    ("G1-11", "制服/視線", 1, 4, 3, 5, 5),
    ("G1-12", "残響/階段", 1, 5, 4, 3, 5),
    ("G1-13", "番号札/裏面", 1, 7, 2, 5, 3),
    ("G1-14", "細工/針金", 1, 3, 7, 2, 5),
    ("G1-15", "真夜中/改札", 1, 5, 3, 7, 2),
    ("G1-16", "冷汗/予定", 1, 2, 5, 3, 7),
    ("G1-17", "仮眠/夢見", 1, 4, 4, 4, 4),
    ("G1-18", "未読/通知", 1, 7, 3, 3, 3),
    ("G1-19", "街灯/点滅", 1, 3, 7, 3, 3),
    ("G1-20", "始発/沈黙", 1, 3, 3, 7, 3),

    # グレード2: 80か所の平均 5.4
    ("G2-01", "監視/カメラ", 2, 9, 5, 4, 4),
    ("G2-02", "深層/ログ", 2, 4, 9, 5, 4),
    ("G2-03", "切断/回線", 2, 4, 4, 9, 5),
    ("G2-04", "青白い/画面", 2, 5, 4, 4, 9),
    ("G2-05", "指紋/照合", 2, 7, 6, 5, 4),
    ("G2-06", "警笛/遠く", 2, 4, 7, 6, 5),
    ("G2-07", "非常線/突破", 2, 5, 4, 7, 6),
    ("G2-08", "現場/証言", 2, 6, 5, 4, 7),
    ("G2-09", "隠し/階段", 2, 8, 3, 8, 3),
    ("G2-10", "照明/落下", 2, 3, 8, 3, 8),
    ("G2-11", "合鍵/裏返", 2, 6, 6, 5, 5),
    ("G2-12", "微熱/診断", 2, 10, 4, 4, 4),
    ("G2-13", "無人駅/時計", 2, 6, 5, 5, 5),
    ("G2-14", "路線図/赤丸", 2, 8, 5, 4, 4),
    ("G2-15", "硝子/亀裂", 2, 4, 8, 5, 4),
    ("G2-16", "電光/掲示", 2, 4, 4, 8, 5),
    ("G2-17", "黒服/会釈", 2, 5, 4, 4, 8),
    ("G2-18", "留守電/再生", 2, 7, 7, 4, 3),
    ("G2-19", "境界/標識", 2, 3, 7, 7, 4),
    ("G2-20", "記録/消去", 2, 4, 3, 7, 7),

    # グレード3: 80か所の平均 6.8
    ("G3-01", "逃走/経路", 3, 10, 7, 6, 5),
    ("G3-02", "偽装/書類", 3, 5, 10, 7, 6),
    ("G3-03", "金属音/接近", 3, 6, 5, 10, 7),
    ("G3-04", "逆光/人影", 3, 7, 6, 5, 10),
    ("G3-05", "施錠/解除", 3, 9, 7, 6, 5),
    ("G3-06", "白煙/非常", 3, 5, 9, 7, 6),
    ("G3-07", "制御室/赤灯", 3, 6, 5, 9, 7),
    ("G3-08", "臨時便/空席", 3, 7, 6, 5, 9),
    ("G3-09", "暗室/現像", 3, 8, 8, 6, 5),
    ("G3-10", "送信/失敗", 3, 5, 8, 8, 6),
    ("G3-11", "振動/床下", 3, 6, 5, 8, 8),
    ("G3-12", "証拠/封筒", 3, 8, 6, 5, 8),
    ("G3-13", "無線/応答", 3, 10, 4, 9, 4),
    ("G3-14", "沈む/ホーム", 3, 4, 10, 4, 9),
    ("G3-15", "逃げ道/消失", 3, 9, 4, 10, 4),
    ("G3-16", "鍵穴/発光", 3, 4, 9, 4, 10),
    ("G3-17", "監査/報告", 3, 7, 7, 7, 6),
    ("G3-18", "歪んだ/鏡", 3, 6, 7, 7, 7),
    ("G3-19", "黒幕/近く", 3, 8, 7, 6, 6),
    ("G3-20", "終点/裏側", 3, 6, 8, 7, 6),

    # グレード4: 80か所の平均 7.2
    ("G4-01", "電脳/門扉", 4, 9, 8, 7, 5),
    ("G4-02", "虚空/改札", 4, 5, 9, 8, 7),
    ("G4-03", "断罪/時刻", 4, 7, 5, 9, 8),
    ("G4-04", "危険/領域", 4, 8, 7, 5, 9),
    ("G4-05", "極夜/非常線", 4, 9, 9, 6, 5),
    ("G4-06", "残酷/信号", 4, 5, 9, 9, 6),
    ("G4-07", "制圧/コード", 4, 6, 5, 9, 9),
    ("G4-08", "冷徹/追跡", 4, 9, 6, 5, 9),
    ("G4-09", "無音/急行", 4, 8, 8, 7, 6),
    ("G4-10", "閉鎖/区画", 4, 6, 8, 8, 7),
    ("G4-11", "真相/直前", 4, 7, 6, 8, 8),
    ("G4-12", "漆黒/階層", 4, 8, 7, 6, 8),
    ("G4-13", "逆転/証明", 4, 9, 7, 9, 4),
    ("G4-14", "閃光/切札", 4, 4, 9, 7, 9),
    ("G4-15", "限界/突破", 4, 9, 4, 9, 7),
    ("G4-16", "密告/回路", 4, 7, 9, 4, 9),
    ("G4-17", "災厄/番号", 4, 7, 7, 7, 7),
    ("G4-18", "最後/改札", 4, 9, 8, 6, 5),
    ("G4-19", "完全/包囲", 4, 5, 9, 8, 6),
    ("G4-20", "醒める/夢", 4, 6, 5, 9, 8),
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
