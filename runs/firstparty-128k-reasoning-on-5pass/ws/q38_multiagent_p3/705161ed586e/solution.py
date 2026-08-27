_DIST_TABLE = [[abs(i - j) for j in range(26)] for i in range(26)]
_R26 = range(26)


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 10**9
        s = caption.encode()
        dist_table = _DIST_TABLE
        r26 = _R26

        # dec[i * 26 + c] stores the chosen character at position i
        # for state (current run char c, length class 3).
        dec = bytearray(n * 26)

        # F[i+1][c][1], F[i+1][c][2], F[i+1][c][3]
        f1 = [INF] * 26
        f2 = [INF] * 26
        f3 = [0] * 26

        # Reusable buffers for F[i][c][*]
        nf1 = [0] * 26
        nf2 = [0] * 26
        nf3 = [0] * 26

        # Compute F[i] for i = n-1 down to 1.
        for i in range(n - 1, 0, -1):
            dist = dist_table[s[i] - 97]

            # Best and second-best over d of dist[d] + F[i+1][d][1].
            # Ties are resolved by smaller character because d is scanned ascending
            # and only strict improvements update the best pair.
            best_cost = INF
            best_char = 0
            second_cost = INF
            second_char = 1

            for d in r26:
                v = dist[d] + f1[d] if f1[d] < INF else INF
                if v < best_cost:
                    second_cost = best_cost
                    second_char = best_char
                    best_cost = v
                    best_char = d
                elif v < second_cost:
                    second_cost = v
                    second_char = d

            idx = i * 26
            for c in r26:
                dc = dist[c]

                # Forced continuation for length classes 1 and 2.
                nf1[c] = dc + f2[c] if f2[c] < INF else INF
                cont = dc + f3[c] if f3[c] < INF else INF
                nf2[c] = cont

                # Switch minimum excluding current character c.
                if best_char != c:
                    sw_cost = best_cost
                    sw_char = best_char
                else:
                    sw_cost = second_cost
                    sw_char = second_char

                # Store the lexicographically smallest optimal next character.
                if cont < sw_cost:
                    nf3[c] = cont
                    dec[idx + c] = c
                elif sw_cost < cont:
                    nf3[c] = sw_cost
                    dec[idx + c] = sw_char
                else:
                    nf3[c] = cont
                    dec[idx + c] = c if c < sw_char else sw_char

            f1, nf1 = nf1, f1
            f2, nf2 = nf2, f2
            f3, nf3 = nf3, f3

        # Initial state: choose the first character, then state is length class 1.
        dist = dist_table[s[0] - 97]
        start_cost = INF
        start_char = 0
        for d in r26:
            v = dist[d] + f1[d] if f1[d] < INF else INF
            if v < start_cost:
                start_cost = v
                start_char = d

        if start_cost >= INF:
            return ""

        dec[0] = start_char

        # Reconstruct the lexicographically smallest optimal caption.
        ans = bytearray(n)
        c = start_char
        length_class = 1
        ans[0] = c + 97

        idx = 26  # dec index for i = 1
        for i in range(1, n):
            if length_class < 3:
                ans[i] = c + 97
                length_class += 1
            else:
                x = dec[idx + c]
                ans[i] = x + 97
                if x != c:
                    c = x
                    length_class = 1
            idx += 26

        return ans.decode()


def _generate_good_strings(n, alpha):
    res = []

    def dfs(pos, parts):
        if pos == n:
            res.append(tuple(parts))
            return
        for length in range(3, n - pos + 1):
            for ch in range(alpha):
                parts.append(ch)
                dfs(pos + length, parts)
                parts.pop()

    dfs(0, [])
    return res


def _brute_expected(vals, good_strings):
    if not good_strings:
        return ""

    best_cost = 10**9
    best = None

    for t in good_strings:
        cost = 0
        for a, b in zip(vals, t):
            cost += abs(a - b)
            if cost > best_cost:
                break

        if cost < best_cost or (cost == best_cost and (best is None or t < best)):
            best_cost = cost
            best = t

    if best is None:
        return ""
    return ''.join(chr(97 + x) for x in best)


def _run_examples(sol):
    cases = [
        ("cdcd", "cccc"),
        ("aca", "aaa"),
        ("bc", ""),
    ]
    failures = []
    for s, expected in cases:
        got = sol.minCostGoodCaption(s)
        if got != expected:
            failures.append((s, expected, got))
    return failures


def _run_brute_tests(sol):
    from itertools import product

    failures = []

    # Exhaustive small-alphabet checks.
    # Alphabet is contiguous from 'a', so medians for any fixed run stay inside it.
    for alpha, max_n in ((2, 10), (3, 8), (4, 7)):
        for n in range(1, max_n + 1):
            good = _generate_good_strings(n, alpha)
            for vals in product(range(alpha), repeat=n):
                s = ''.join(chr(97 + v) for v in vals)
                expected = _brute_expected(vals, good)
                got = sol.minCostGoodCaption(s)
                if got != expected:
                    failures.append((s, expected, got))
                    if len(failures) >= 10:
                        return failures

    return failures


def _is_good(t):
    n = len(t)
    i = 0
    while i < n:
        j = i + 1
        while j < n and t[j] == t[i]:
            j += 1
        if j - i < 3:
            return False
        i = j
    return True


def _run_benchmark(sol):
    import time

    n = 50000
    s = ''.join(chr(97 + (i * 7) % 26) for i in range(n))

    t0 = time.perf_counter()
    res = sol.minCostGoodCaption(s)
    t1 = time.perf_counter()

    ok = (len(res) == n and _is_good(res))
    cost = 0
    if ok:
        for a, b in zip(s, res):
            cost += abs(ord(a) - ord(b))

    return (t1 - t0) * 1000.0, ok, cost, len(res)


if __name__ == "__main__":
    sol = Solution()
    all_ok = True

    ex_fail = _run_examples(sol)
    if ex_fail:
        all_ok = False
        print("Examples: FAIL")
        for item in ex_fail:
            print(item)
    else:
        print("Examples: pass")

    bf_fail = _run_brute_tests(sol)
    if bf_fail:
        all_ok = False
        print("Brute force: FAIL")
        for item in bf_fail:
            print(item)
    else:
        print("Brute force: pass")

    ms, ok, cost, length = _run_benchmark(sol)
    if not ok:
        all_ok = False
        print(f"Benchmark: FAIL (len={length}, good={ok})")
    else:
        print(f"Benchmark: pass n=50000 time={ms:.1f}ms cost={cost}")

    print("OVERALL:", "PASS" if all_ok else "FAIL")