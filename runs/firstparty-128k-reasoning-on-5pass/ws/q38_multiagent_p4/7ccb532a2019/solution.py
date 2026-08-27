import random

INF = 10**9


class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        n = len(s)
        ans = n - max(cnt)
        if ans == 0:
            return 0

        for k in range(1, 2 * n + 1):
            if k - n >= ans:
                break

            dp0 = cnt[0]
            dp1 = cnt[0] - k
            if dp1 < 0:
                dp1 = -dp1

            for i in range(1, 26):
                prev = cnt[i - 1]
                cur = cnt[i]

                best = dp0 if dp0 < dp1 else dp1
                ndp0 = best + cur

                cost1 = cur - k
                if cost1 < 0:
                    cost1 = -cost1

                deficit = k - cur
                if deficit > 0:
                    save0 = prev if prev < deficit else deficit
                    surplus1 = prev - k
                    if surplus1 > 0:
                        save1 = surplus1 if surplus1 < deficit else deficit
                    else:
                        save1 = 0
                else:
                    save0 = 0
                    save1 = 0

                v0 = dp0 + cost1 - save0
                v1 = dp1 + cost1 - save1
                ndp1 = v0 if v0 < v1 else v1

                dp0, dp1 = ndp0, ndp1

            cur_cost = dp0 if dp0 < dp1 else dp1
            if cur_cost < ans:
                ans = cur_cost
                if ans == 0:
                    return 0

        return ans


def min_cost_formula(b):
    """Closed-form exact cost for a fixed source/target difference vector b."""
    total = 0
    for v in b:
        total += v if v >= 0 else -v

    save = 0
    for i in range(25):
        surplus = b[i] if b[i] > 0 else 0
        deficit = -b[i + 1] if b[i + 1] < 0 else 0
        save += surplus if surplus < deficit else deficit

    return total - save


def min_cost_flow_line(b, n, cutoff=INF):
    """
    Exact min-cost flow DP on the 26-letter line.

    b[i] = source_count[i] - target_count[i].
    Let x_i be flow from letter i to i+1, with x_{-1}=x_{25}=0.
    Cost = sum_i x_i + |b[i] + x_{i-1} - x_i|.
    """
    if cutoff <= 0:
        return INF

    total_pos = 0
    for v in b:
        if v > 0:
            total_pos += v

    B = min(n, total_pos)
    if B == 0:
        cost = 0
        for v in b:
            cost += v if v >= 0 else -v
        return cost if cost < cutoff else INF

    dp = [INF] * (B + 1)
    dp[0] = 0

    for i in range(26):
        t = b[i]

        if i < 25:
            # suffix[p] = min_{px >= p} dp[px] + t + px
            suffix = [INF] * (B + 2)
            for px in range(B, -1, -1):
                val = dp[px]
                if val < cutoff:
                    cand = val + t + px
                    suffix[px] = cand if cand < suffix[px + 1] else suffix[px + 1]
                else:
                    suffix[px] = suffix[px + 1]

            # prefix[p] = min_{px < p} dp[px] - t - px
            prefix = [INF] * (B + 2)
            for px in range(B + 1):
                val = dp[px]
                if val < cutoff:
                    cand = val - t - px
                    prefix[px + 1] = cand if cand < prefix[px] else prefix[px]
                else:
                    prefix[px + 1] = prefix[px]

            ndp = [INF] * (B + 1)
            for x in range(B + 1):
                p = x - t
                best_val = INF

                if p <= 0:
                    best_val = suffix[0]
                elif p > B + 1:
                    if prefix[B + 1] < INF:
                        best_val = 2 * x + prefix[B + 1]
                else:
                    best_val = suffix[p]
                    if prefix[p] < INF:
                        cand = 2 * x + prefix[p]
                        if cand < best_val:
                            best_val = cand

                if best_val < cutoff:
                    ndp[x] = best_val

            dp = ndp
        else:
            # Final letter: x_25 must be 0.
            best_val = INF
            for px, val in enumerate(dp):
                if val >= cutoff:
                    continue
                diff = t + px
                if diff < 0:
                    diff = -diff
                v = val + diff
                if v < best_val and v < cutoff:
                    best_val = v
            dp = [best_val]

    return dp[0]


def brute_force(s):
    """
    Exhaustive brute force for small strings.

    Enumerates all good targets over a safe relevant alphabet:
    all letters that appear, plus their immediate next letter.
    A zero-count letter whose previous letter also has zero count can never
    be part of an optimal target, because removing it strictly reduces cost.
    """
    cnt = [0] * 26
    for ch in s:
        cnt[ord(ch) - 97] += 1

    n = len(s)
    best = n - max(cnt)
    if best == 0:
        return 0

    pos = [i for i, c in enumerate(cnt) if c > 0]
    rel = set(pos)
    for i in pos:
        if i + 1 < 26:
            rel.add(i + 1)
    rel = sorted(rel)
    r = len(rel)

    masks_by_m = [[] for _ in range(r + 1)]
    for mask in range(1 << r):
        if mask == 0:
            continue
        inds = []
        m = 0
        for j, idx in enumerate(rel):
            if mask & (1 << j):
                m += 1
                inds.append(idx)
        masks_by_m[m].append(tuple(inds))

    for k in range(1, 2 * n + 1):
        if k - n >= best:
            break

        for m in range(1, r + 1):
            length = m * k
            if abs(length - n) >= best:
                continue

            for inds in masks_by_m[m]:
                if abs(length - n) >= best:
                    continue

                b = cnt[:]
                for idx in inds:
                    b[idx] -= k

                cost = min_cost_flow_line(b, n, best)
                if cost < best:
                    best = cost
                    if best == 0:
                        return 0

    return best


def validate_flow():
    """Cross-check the line-flow DP against the closed-form formula."""
    random.seed(777)
    for _ in range(200):
        b = [random.randint(-3, 3) for _ in range(26)]
        n_val = sum(v for v in b if v > 0)
        c1 = min_cost_flow_line(b, n_val, INF)
        c2 = min_cost_formula(b)
        if c1 != c2:
            return False, f"b={b} line={c1} formula={c2}"
    return True, ""


def run_tests():
    sol = Solution()
    failures = []
    bf_cache = {}

    def get_bf(s):
        if s not in bf_cache:
            bf_cache[s] = brute_force(s)
        return bf_cache[s]

    examples = [
        ("acab", 1),
        ("wddw", 0),
        ("aaabc", 2),
    ]

    for s, expected in examples:
        sol_ans = sol.makeStringGood(s)
        bf_ans = get_bf(s)
        if sol_ans != expected or sol_ans != bf_ans:
            failures.append((s, expected, sol_ans, bf_ans))

    edge_cases = [
        "aaa",
        "aaaa",
        "zzzz",
        "zzzzz",
        "abc",
        "abcd",
        "abcde",
        "abcdef",
        "yzz",
        "zzza",
        "yzzz",
        "xzyz",
        "zzzy",
        "xzyzz",
        "yzza",
        "yzyz",
        "aaaccc",
        "abbbc",
        "aaabc",
        "acab",
        "wddw",
    ]

    random.seed(12345)
    random_cases = []

    for _ in range(120):
        n = random.randint(3, 5)
        alpha = random.choice([
            "abcde",
            "abcxyz",
            "abcdefghijklmnopqrstuvwxyz",
        ])
        random_cases.append("".join(random.choice(alpha) for _ in range(n)))

    for _ in range(40):
        n = random.randint(3, 5)
        random_cases.append("".join(random.choice("xyz") for _ in range(n)))

    for s in edge_cases + random_cases:
        sol_ans = sol.makeStringGood(s)
        bf_ans = get_bf(s)
        if sol_ans != bf_ans:
            failures.append((s, bf_ans, sol_ans, bf_ans))

    flow_ok, flow_msg = validate_flow()
    if not flow_ok:
        failures.append(("flow_validation", flow_msg, None, None))

    print("SAMPLE TESTS:", "FAIL" if failures else "PASS")
    if failures:
        for f in failures[:20]:
            print("FAIL", f)
    else:
        print("Examples: acab=1, wddw=0, aaabc=2")
        print(f"Checked {len(bf_cache)} unique strings against brute force; no failing cases.")


if __name__ == "__main__":
    run_tests()