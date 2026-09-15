from typing import List
from itertools import permutations


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials (Python big ints, no overflow concerns).
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i

        used = [False] * (n + 1)
        o = (n + 1) // 2   # how many odd values exist in 1..n
        e = n // 2         # how many even values exist in 1..n

        # Valid completions for `o` remaining odd and `e` remaining even values
        # when the next slot must have parity `next_par` (1=odd, 0=even).
        def count_after(o: int, e: int, next_par: int) -> int:
            r = o + e
            if r == 0:
                return 1
            if next_par == 1:
                Orem, Erem = (r + 1) // 2, r // 2
            else:
                Orem, Erem = r // 2, (r + 1) // 2
            if o == Orem and e == Erem:
                return fact[o] * fact[e]
            return 0

        res: List[int] = []
        next_par = None  # position 0 is unconstrained

        for _ in range(n):
            chosen = None
            for v in range(1, n + 1):          # ascending value = lexicographic order
                if used[v]:
                    continue
                vp = v & 1
                if next_par is not None and vp != next_par:
                    continue

                o2 = o - 1 if vp == 1 else o
                e2 = e - 1 if vp == 0 else e
                if o2 + e2 == 0:
                    cnt = 1
                else:
                    cnt = count_after(o2, e2, 1 - vp)

                if cnt == 0:
                    continue
                if k <= cnt:                    # this branch holds the k-th one
                    chosen = v
                    break
                k -= cnt                        # skip this whole block

            if chosen is None:
                return []

            used[chosen] = True
            res.append(chosen)
            if chosen & 1:
                o -= 1
            else:
                e -= 1
            next_par = 1 - (chosen & 1)

        return res


# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------
def all_alternating(n: int) -> List[List[int]]:
    """All alternating permutations of 1..n, sorted lexicographically."""
    out = []
    for p in permutations(range(1, n + 1)):
        if all((p[i] - p[i + 1]) & 1 for i in range(n - 1)):
            out.append(list(p))
    out.sort()
    return out


def brute(n: int, k: int, table=None) -> List[int]:
    if table is None:
        table = all_alternating(n)
    return table[k - 1] if 1 <= k <= len(table) else []


def run_tests() -> bool:
    sol = Solution()
    mismatches = []

    # --- Provided examples -------------------------------------------------
    examples = [
        (4, 6, [3, 4, 1, 2]),
        (3, 2, [3, 2, 1]),
        (2, 3, []),
    ]
    for (n, k, exp) in examples:
        got = sol.permute(n, k)
        if got != exp:
            mismatches.append((n, k, exp, got))

    # --- Exhaustive brute-force comparison ---------------------------------
    for n in range(1, 9):
        table = all_alternating(n)
        total = len(table)
        for k in range(1, total + 3):   # include out-of-range k = total+1, total+2
            exp = brute(n, k, table)
            got = sol.permute(n, k)
            if got != exp:
                mismatches.append((n, k, exp, got))

    if mismatches:
        print("FAIL: %d mismatch(es) found" % len(mismatches))
        for (n, k, exp, got) in mismatches:
            print(f"  n={n}, k={k}, expected={exp}, got={got}")
        return False

    print("PASS: all provided examples and exhaustive n=1..8 checks matched.")
    return True


if __name__ == "__main__":
    run_tests()