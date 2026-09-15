import sys
from functools import lru_cache
from itertools import product


def closed_form(n, a):
    odd = sum(x & 1 for x in a)

    if n == 1:
        return "Fennec"
    if n == 2:
        return "Snuke"
    if n == 3:
        return "Fennec" if odd > 0 else "Snuke"

    return "Fennec" if odd % 2 == 1 else "Snuke"


def brute_winner(n, a):
    """Exact memoized DP for small validation only."""
    start = tuple(sorted(a))

    @lru_cache(maxsize=None)
    def win(unclaimed, pool):
        if not unclaimed:
            return False

        # Spend one already-available token.
        if pool > 0 and not win(unclaimed, pool - 1):
            return True

        # Claim a new index. Equal values are indistinguishable.
        seen = set()
        for i, v in enumerate(unclaimed):
            if v in seen:
                continue
            seen.add(v)
            nxt = unclaimed[:i] + unclaimed[i + 1:]
            if not win(nxt, pool + v - 1):
                return True

        return False

    return win(start, 0)


def validate():
    # Samples.
    assert closed_form(3, [1, 9, 2]) == "Fennec"
    assert closed_form(2, [25, 29]) == "Snuke"
    assert closed_form(6, [1, 9, 2, 25, 2, 9]) == "Snuke"

    assert brute_winner(3, [1, 9, 2]) is True
    assert brute_winner(2, [25, 29]) is False
    assert brute_winner(6, [1, 9, 2, 25, 2, 9]) is False

    # Exhaustive small checks, including different magnitudes with same parity.
    for n in range(1, 5):
        for vals in product(range(1, 5), repeat=n):
            expected = "Fennec" if brute_winner(n, list(vals)) else "Snuke"
            got = closed_form(n, list(vals))
            if got != expected:
                raise AssertionError((n, vals, got, expected))

    # A few extra small checks for N >= 4.
    for vals in product(range(1, 3), repeat=5):
        expected = "Fennec" if brute_winner(5, list(vals)) else "Snuke"
        got = closed_form(5, list(vals))
        if got != expected:
            raise AssertionError((5, vals, got, expected))

    # Parity-invariance spot checks.
    for base in [(1, 2, 2, 2), (3, 2, 2, 2), (1, 4, 4, 4), (3, 4, 4, 4)]:
        assert closed_form(4, list(base)) == closed_form(4, [x + 2 for x in base])


def main():
    # Run with: python program.py --validate
    if "--validate" in sys.argv:
        validate()
        return

    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    print(closed_form(n, a))


if __name__ == "__main__":
    main()