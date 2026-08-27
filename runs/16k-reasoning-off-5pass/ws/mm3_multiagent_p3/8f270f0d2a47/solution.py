import sys
from functools import lru_cache

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        # Precompute digit prime factor vectors for d = 1..9
        # (v2, v3, v5, v7)
        digit_vec = {
            1: (0, 0, 0, 0),
            2: (1, 0, 0, 0),
            3: (0, 1, 0, 0),
            4: (2, 0, 0, 0),
            5: (0, 0, 1, 0),
            6: (1, 1, 0, 0),
            7: (0, 0, 0, 1),
            8: (3, 0, 0, 0),
            9: (0, 2, 0, 0),
        }

        # Precompute sum requirements: for each sum 1..81, whether it's
        # 2,3,5,7-smooth and the required exponents of 2,3,5,7.
        sum_reqs = {}
        for s in range(1, 82):
            v2 = v3 = v5 = v7 = 0
            tmp = s
            for p in (2, 3, 5, 7):
                while tmp % p == 0:
                    if p == 2: v2 += 1
                    elif p == 3: v3 += 1
                    elif p == 5: v5 += 1
                    elif p == 7: v7 += 1
                    tmp //= p
            smooth = (tmp == 1)
            sum_reqs[s] = (smooth, v2, v3, v5, v7)

        # Build DP table for suffixes of length k (k from 0 to 9).
        # dp[k] maps (sum, v2, v3, v5, v7, has_zero) -> count of ways
        # to fill k digits (each 0..9) achieving that final state.
        dp = [dict() for _ in range(10)]
        # Length 0: empty suffix
        dp[0][(0, 0, 0, 0, 0, False)] = 1

        for k in range(1, 10):
            cur = dp[k]
            prev = dp[k - 1]
            for state, cnt in prev.items():
                s, v2, v3, v5, v7, hz = state
                for d in range(10):
                    if s == 0 and not hz and d == 0:
                        # Still in leading-zero state
                        nstate = (0, 0, 0, 0, 0, False)
                    else:
                        ns = s + d
                        if d == 0:
                            nstate = (ns, v2, v3, v5, v7, True)
                        else:
                            dv2, dv3, dv5, dv7 = digit_vec[d]
                            nstate = (ns, v2 + dv2, v3 + dv3,
                                      v5 + dv5, v7 + dv7, hz)
                    cur[nstate] = cur.get(nstate, 0) + cnt

        def count_upto(x: int) -> int:
            """Count beautiful numbers in [0, x]."""
            if x < 0:
                return 0
            digits = list(map(int, str(x)))
            n = len(digits)
            total = 0
            # Current state from prefix processed so far
            s = 0
            v2 = v3 = v5 = v7 = 0
            hz = False

            for i in range(n):
                d_bound = digits[i]
                for d in range(d_bound):
                    if s == 0 and not hz and d == 0:
                        ns, nv2, nv3, nv5, nv7, nhz = 0, 0, 0, 0, 0, False
                    else:
                        ns = s + d
                        if d == 0:
                            nv2, nv3, nv5, nv7, nhz = v2, v3, v5, v7, True
                        else:
                            dv2, dv3, dv5, dv7 = digit_vec[d]
                            nv2 = v2 + dv2
                            nv3 = v3 + dv3
                            nv5 = v5 + dv5
                            nv7 = v7 + dv7
                            nhz = hz
                    rem = n - 1 - i
                    total += dp[rem].get((ns, nv2, nv3, nv5, nv7, nhz), 0)

                # Update current state with the bound digit
                if s == 0 and not hz and d_bound == 0:
                    pass  # stay in (0,0,0,0,0,False)
                else:
                    s = s + d_bound
                    if d_bound == 0:
                        hz = True
                    else:
                        dv2, dv3, dv5, dv7 = digit_vec[d_bound]
                        v2 += dv2
                        v3 += dv3
                        v5 += dv5
                        v7 += dv7

            # Check the full number itself
            if s > 0:
                if hz:
                    total += 1
                else:
                    smooth, rv2, rv3, rv5, rv7 = sum_reqs[s]
                    if smooth and v2 >= rv2 and v3 >= rv3 and v5 >= rv5 and v7 >= rv7:
                        total += 1
            return total

        return count_upto(r) - count_upto(l - 1)

    def _brute_force(self, l: int, r: int) -> int:
        """Naive O(r-l+1) check for testing purposes."""
        def is_beautiful(n: int) -> bool:
            prod = 1
            summ = 0
            for ch in str(n):
                d = int(ch)
                prod *= d
                summ += d
            return summ > 0 and prod % summ == 0

        return sum(1 for n in range(l, r + 1) if is_beautiful(n))


# --- Self-test / verification routine ---
if __name__ == "__main__":
    import random
    sol = Solution()

    # Brute-force verification on small ranges (r <= 10000)
    print("Running brute-force verification (r <= 10000)...")
    for _ in range(200):
        l = random.randint(1, 9999)
        r = random.randint(l, 10000)
        dp_ans = sol.beautifulNumbers(l, r)
        brute_ans = sol._brute_force(l, r)
        if dp_ans != brute_ans:
            print(f"MISMATCH: l={l}, r={r}, dp={dp_ans}, brute={brute_ans}")
            sys.exit(1)
    print("All 200 random tests passed.")

    # Sanity check on the provided examples
    print("Example 1 (l=10, r=20):", sol.beautifulNumbers(10, 20))   # expect 2
    print("Example 2 (l=1,  r=15):", sol.beautifulNumbers(1, 15))    # expect 10

    # Larger random spot-checks (r up to 200000) – still feasible for brute
    print("Running larger spot-checks (r up to 200000)...")
    for _ in range(20):
        l = random.randint(1, 199000)
        r = random.randint(l, 200000)
        dp_ans = sol.beautifulNumbers(l, r)
        brute_ans = sol._brute_force(l, r)
        if dp_ans != brute_ans:
            print(f"MISMATCH: l={l}, r={r}, dp={dp_ans}, brute={brute_ans}")
            sys.exit(1)
    print("All larger spot-checks passed.")