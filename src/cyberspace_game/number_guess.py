"""4桁の数当てゲームのルール処理。"""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True, slots=True)
class NumberGuessResult:
    """数当て1回分の結果をまとめるデータクラス。"""

    # secret: キャラクター側が内部で持っている正解の4桁数字です。
    secret: str

    # guess: プレイヤーが入力した4桁数字です。
    guess: str

    # matched_digits: 同じ位置で一致した桁数です。0から4までの値になります。
    matched_digits: int

    @property
    def grade(self) -> int:
        """一致桁数を、そのままカードグレードとして返します。"""

        return self.matched_digits

    @property
    def is_exact(self) -> bool:
        """4桁すべて一致したかどうかを返します。"""

        return self.matched_digits == 4


def generate_secret(rng: random.Random | None = None) -> str:
    """0000から9999までの正解数字を4桁文字列で生成します。"""

    # rng: seed付きのRandomを渡すと、テストや実験で結果を再現できます。
    rng = rng or random.Random()

    # :04d により、7のような数値も "0007" として4桁に揃えます。
    return f"{rng.randrange(10_000):04d}"


def score_guess(secret: str, guess: str) -> int:
    """正解と入力を比べ、同じ位置で一致した桁数を数えます。"""

    # secret/guess は数値ではなく文字列として扱います。
    # そうすることで "0001" のような先頭ゼロを失わずに比較できます。
    _validate_four_digit_text(secret, "secret")
    _validate_four_digit_text(guess, "guess")

    # zipで正解と入力を左から1桁ずつ取り出し、同じなら1として合計します。
    return sum(secret_digit == guess_digit for secret_digit, guess_digit in zip(secret, guess))


def resolve_number_guess(
    guess: str,
    rng: random.Random | None = None,
    secret: str | None = None,
) -> NumberGuessResult:
    """数当てを1回解決し、正解・入力・一致桁数をまとめて返します。"""

    # guess: プレイヤー入力です。ここでは必ず4桁数字か確認します。
    _validate_four_digit_text(guess, "guess")

    # secret: テスト時は固定値を渡せます。通常プレイではランダム生成します。
    secret = secret if secret is not None else generate_secret(rng)
    _validate_four_digit_text(secret, "secret")

    # NumberGuessResultにまとめることで、あとで grade や is_exact を簡単に参照できます。
    return NumberGuessResult(
        secret=secret,
        guess=guess,
        matched_digits=score_guess(secret, guess),
    )


def _validate_four_digit_text(value: str, label: str) -> None:
    """値が4桁の数字文字列かどうかを確認します。"""

    # len(value) != 4: 桁数違いを弾きます。
    # value.isdigit(): 数字以外の文字が混ざっていないか確認します。
    if len(value) != 4 or not value.isdigit():
        raise ValueError(f"{label} must be exactly four digits, got {value!r}")
