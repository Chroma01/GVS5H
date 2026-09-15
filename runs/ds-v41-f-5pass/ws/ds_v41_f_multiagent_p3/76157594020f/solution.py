class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        # Precompute maximal run lengths of equal characters.
        runs = []
        i = 0
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            runs.append(j - i)
            i = j

        def feasible(L: int) -> bool:
            if L == 1:
                # Final string must be strictly alternating: only two targets.
                mism = 0
                for k in range(n):
                    if (ord(s[k]) - 48) != (k & 1):
                        mism += 1
                return min(mism, n - mism) <= numOps

            # For L >= 2, flips go in run interiors so runs are independent.
            # A run of length r needs floor(r / (L + 1)) flips.
            flips = 0
            for r in runs:
                flips += r // (L + 1)
                if flips > numOps:
                    return False
            return True

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


# ---------------------------------------------------------------------------
# Differential testing harness: brute force vs candidate.
# ---------------------------------------------------------------------------

def longest_run(bits):
    if not bits:
        return 0
    best = cur = 1
    for i in range(1, len(bits)):
        if bits[i] == bits[i - 1]:
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 1
    return best


def brute_table(s):
    """ans[k] = min achievable longest run using AT MOST k flips."""
    n = len(s)
    base = [ord(c) - 48 for c in s]
    INF = float("inf")
    best = [INF] * (n + 1)          # best[k] = min run using EXACTLY k flips
    for mask in range(1 << n):
        k = bin(mask).count("1")
        bits = [base[i] ^ ((mask >> i) & 1) for i in range(n)]
        lr = longest_run(bits)
        if lr < best[k]:
            best[k] = lr
    res = []
    cur = INF
    for k in range(n + 1):
        if best[k] < cur:
            cur = best[k]
        res.append(cur)
    return res


def main():
    sol = Solution()
    mismatches = []
    total = 0

    for n in range(1, 10):
        for m in range(1 << n):
            s = format(m, "0{}b".format(n))
            table = brute_table(s)
            for numOps in range(n + 1):
                total += 1
                cand = sol.minLength(s, numOps)
                ref = table[numOps]
                if cand != ref:
                    mismatches.append((s, numOps, cand, ref))

    print("Total cases tested:", total)
    if mismatches:
        print("MISMATCHES FOUND:", len(mismatches))
        for s, numOps, cand, ref in mismatches[:50]:
            print("  s=%s numOps=%d candidate=%d brute=%d"
                  % (s, numOps, cand, ref))
    else:
        print("ALL MATCH: candidate == brute force over n=1..9, numOps=0..n")

    examples = [("000001", 1, 2), ("0000", 2, 1), ("0101", 0, 1)]
    for s, numOps, expected in examples:
        got = sol.minLength(s, numOps)
        tag = "OK" if got == expected else "FAIL"
        print("Example s=%r numOps=%d -> got %d expected %d [%s]"
              % (s, numOps, got, expected, tag))

    probes = ["0110", "000111", "1110111", "001100",
              "000000", "010", "0011", "0001111"]
    for s in probes:
        table = brute_table(s)
        row = []
        for numOps in range(len(s) + 1):
            cand = sol.minLength(s, numOps)
            ref = table[numOps]
            row.append((numOps, cand, ref, cand == ref))
        ok = all(r[3] for r in row)
        print("Probe s=%r all_ok=%s" % (s, ok))
        print("    " + " ".join("%d:%d/%d" % (n, c, r) for n, c, r, _ in row))


if __name__ == "__main__":
    main()