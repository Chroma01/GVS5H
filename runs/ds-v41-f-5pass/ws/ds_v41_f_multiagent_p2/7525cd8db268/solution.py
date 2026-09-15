from typing import List
import random


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)

        # Bucket each normalized pair (a, b), a < b, by its larger endpoint b.
        buckets = [[] for _ in range(n + 1)]
        for i, (x, y) in enumerate(conflictingPairs):
            a, b = (x, y) if x < y else (y, x)
            buckets[b].append((a, i))

        best_a = 0        # largest active lower endpoint
        best_cnt = 0      # how many pairs share best_a
        best_owner = -1   # an id of a pair achieving best_a
        second_a = 0      # largest active lower endpoint strictly below best_a
        base = 0          # valid subarrays with ALL pairs present
        gain = [0] * m    # extra count obtainable by removing each pair

        for r in range(1, n + 1):
            # Activate pairs whose larger endpoint is exactly r.
            for a, i in buckets[r]:
                if a > best_a:
                    second_a = best_a
                    best_a = a
                    best_cnt = 1
                    best_owner = i
                elif a == best_a:
                    best_cnt += 1
                elif a > second_a:
                    second_a = a

            base += r - best_a

            # Count can only rise at r if a single pair is the unique bottleneck.
            if best_cnt == 1:
                gain[best_owner] += best_a - second_a

        return base + max(gain)


# ---------------- verification harness (not part of the submitted class) ----------------

def brute(n: int, pairs: List[List[int]]) -> int:
    """Independent brute force: try each removal, enumerate every subarray."""
    m = len(pairs)
    norm = [(min(x, y), max(x, y)) for (x, y) in pairs]
    best = 0
    for k in range(m):
        rem = [norm[j] for j in range(m) if j != k]
        cnt = 0
        for l in range(1, n + 1):
            for r in range(l, n + 1):
                ok = True
                for (a, b) in rem:
                    if l <= a and r >= b:   # both a and b inside [l, r]
                        ok = False
                        break
                if ok:
                    cnt += 1
        best = max(best, cnt)
    return best


if __name__ == "__main__":
    sol = Solution()

    # Provided examples
    e1 = sol.maxSubarrays(4, [[2, 3], [1, 4]])
    e2 = sol.maxSubarrays(5, [[1, 2], [2, 5], [3, 5]])
    print("Example 1:", e1, "expected 9", "PASS" if e1 == 9 else "FAIL")
    print("Example 2:", e2, "expected 12", "PASS" if e2 == 12 else "FAIL")

    # Hand-picked edge cases
    checks = [
        (3, [[1, 2], [1, 3]]),
        (2, [[1, 2]]),
        (4, [[4, 3], [1, 2], [2, 4]]),
        (2, [[2, 1]]),
        (5, [[1, 5]]),
    ]
    for n, p in checks:
        got, exp = sol.maxSubarrays(n, p), brute(n, p)
        print(f"edge n={n} pairs={p}: got={got} brute={exp}",
              "PASS" if got == exp else "FAIL")

    # Randomized cross-check vs brute force
    random.seed(12345)
    mism = 0
    for t in range(20000):
        n = random.randint(2, 8)
        m = random.randint(1, min(2 * n, 6))
        pairs = []
        style = random.random()
        for _ in range(m):
            if pairs and style < 0.3:
                pairs.append(list(random.choice(pairs)))          # duplicates
            elif pairs and style < 0.5:
                x, y = random.choice(pairs)
                pairs.append([y, x])                              # reversed dup
            else:
                a = random.randint(1, n)
                b = random.randint(1, n)
                while b == a:
                    b = random.randint(1, n)
                pairs.append([a, b])
        got, exp = sol.maxSubarrays(n, pairs), brute(n, pairs)
        if got != exp:
            mism += 1
            print("MISMATCH", n, pairs, "got", got, "expected", exp)
            if mism > 5:
                break
    print("random cross-check:", "PASS" if mism == 0 else "FAIL", "mismatches=", mism)