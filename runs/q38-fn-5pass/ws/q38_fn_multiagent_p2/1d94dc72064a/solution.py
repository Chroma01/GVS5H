import sys
from functools import lru_cache
from itertools import product

sys.setrecursionlimit(1_000_000)


def rule_winner(A):
    n = len(A)
    if n == 1:
        return True
    if n == 2:
        return False

    odd = sum(x & 1 for x in A)

    if n == 3:
        return odd > 0

    return (odd & 1) == 1


def exact_winner(A):
    """
    Exact minimax solver for small instances.

    State:
      mask: bitmask of unchosen indices
      p: total remaining optional moves on already chosen indices

    A move on an unchosen index removes it from mask and adds A_i - 1
    optional moves. A move on a chosen index just decreases p by 1.
    If only one unchosen index remains, the current player wins immediately
    by choosing it.
    """
    n = len(A)
    full = (1 << n) - 1
    add = [a - 1 for a in A]

    @lru_cache(maxsize=None)
    def win(mask, p):
        # If exactly one index is unchosen, choose it and win.
        if mask & (mask - 1) == 0:
            return True

        # Optional move on an already chosen index.
        if p > 0 and not win(mask, p - 1):
            return True

        # Choose one of the still unchosen indices.
        m = mask
        while m:
            lsb = m & -m
            i = lsb.bit_length() - 1
            nxt_mask = mask ^ lsb

            if not win(nxt_mask, p + add[i]):
                return True

            m ^= lsb

        return False

    return win(full, 0)


def brute_report():
    """
    Enumerate small cases, compare exact minimax results with the proposed
    parity rule, and print observed patterns.
    """
    mismatches = []
    observed = {}

    configs = []

    # Enough to expose small-N exceptions and the general parity behavior.
    for n in range(1, 7):
        max_a = 4 if n <= 5 else 3
        configs.append((n, range(1, max_a + 1)))

    # Additional checks for larger N with minimal values.
    for n in range(7, 9):
        configs.append((n, range(1, 3)))

    for n, vals in configs:
        for A in product(vals, repeat=n):
            exact = exact_winner(A)
            pred = rule_winner(A)

            if exact != pred:
                mismatches.append((A, exact, pred))

            odd = sum(x & 1 for x in A)
            observed.setdefault((n, odd), set()).add(exact)

    print("brute-force verification")

    if mismatches:
        print("counterexamples:")
        for A, exact, pred in mismatches[:50]:
            print(A, "exact", exact, "rule", pred)
        if len(mismatches) > 50:
            print("total counterexamples:", len(mismatches))
    else:
        print("no counterexamples found")

    print("observed initial winners by (N, odd_count):")
    for key in sorted(observed):
        vals = observed[key]
        if len(vals) == 1:
            print(key, "win" if next(iter(vals)) else "lose")
        else:
            print(key, "mixed", sorted(vals))


def main():
    data = sys.stdin.read().strip().split()

    # No input, or explicit brute mode: run the verification report.
    if not data:
        brute_report()
        return

    if data[0].lower() == "brute":
        brute_report()
        return

    # Normal competitive-programming mode.
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    print("Fennec" if rule_winner(A) else "Snuke")


if __name__ == "__main__":
    main()