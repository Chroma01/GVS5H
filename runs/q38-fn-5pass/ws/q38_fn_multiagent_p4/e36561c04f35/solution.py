import sys
from collections import deque

INF = 10**18


# ----------------------------------------------------------------------
# Solver: RLE + constant-state DP.
#
# State (p, l, one):
#   p  = value of the previous batch
#   l  = value of the current latest batch
#   one = current latest batch has total length exactly 1
#
# Value 0 is only a sentinel for "no previous batch"; real values are positive.
# ----------------------------------------------------------------------
def apply_run(dp, val, w):
    if dp is None:
        return {(0, val, w == 1): 1}

    ndp = {}
    one_w = (w == 1)

    for (p, l, one), cost in dp.items():
        if val == l:
            # Join the current latest batch.
            key = (p, l, False)
            if cost < ndp.get(key, INF):
                ndp[key] = cost
        else:
            ncost = cost + 1

            # Start a new batch.
            key = (l, val, one_w)
            if ncost < ndp.get(key, INF):
                ndp[key] = ncost

            # Put this singleton into the previous batch, crossing only a
            # singleton current batch. This costs one inversion.
            if val == p and one and one_w:
                key = (p, l, True)
                if ncost < ndp.get(key, INF):
                    ndp[key] = ncost

    return ndp


def dp_min(seq):
    if not seq:
        return 0

    dp = None
    cur = seq[0]
    w = 1

    for x in seq[1:]:
        if x == cur:
            w += 1
        else:
            dp = apply_run(dp, cur, w)
            cur = x
            w = 1

    dp = apply_run(dp, cur, w)
    return min(dp.values())


def solve_original_from_ints(data):
    if not data:
        return

    t = data[0]
    idx = 1
    out = []

    for _ in range(t):
        n = data[idx]
        idx += 1

        if n == 0:
            out.append("0")
            continue

        cur = data[idx]
        idx += 1
        w = 1
        dp = None

        for _ in range(n - 1):
            x = data[idx]
            idx += 1
            if x == cur:
                w += 1
            else:
                dp = apply_run(dp, cur, w)
                cur = x
                w = 1

        dp = apply_run(dp, cur, w)
        out.append(str(min(dp.values()) if dp else 0))

    sys.stdout.write("\n".join(out))


# ----------------------------------------------------------------------
# Exhaustive verifier / stress tester.
#
# This is only executed when stdin is empty.  The online judge input is
# non-empty, so the solver path above is used there.
# ----------------------------------------------------------------------
def canonicalize(seq):
    mp = {}
    nxt = 0
    res = []
    for x in seq:
        if x not in mp:
            mp[x] = nxt
            nxt += 1
        res.append(mp[x])
    return tuple(res)


def brute_distances(max_len):
    """
    Exact reverse BFS over canonical equality patterns up to max_len.

    Reverse operations:
      - adjacent swap
      - prepend a positive block of equal values, then canonicalize

    All generated states are kept canonical.  For swaps, canonicalization is
    done directly from the canonical state; for prepends, the canonical label
    transformation is explicit.
    """
    zero_blocks = [()] + [(0,) * i for i in range(1, max_len + 1)]
    dist = {(): 0}
    q = deque([()])

    while q:
        s = q.popleft()
        base = dist[s]
        k = len(s)

        # Reverse adjacent swaps.
        if k > 1:
            dmax = max(s) + 1
            first = [-1] * dmax
            for i, x in enumerate(s):
                if first[x] == -1:
                    first[x] = i

            for i in range(k - 1):
                a = s[i]
                b = s[i + 1]
                if a == b:
                    continue

                # If both are first occurrences, their first-occurrence order
                # swaps; all other occurrences of a and b swap labels too,
                # while the two first occurrences themselves remain a, b.
                if first[a] == i and first[b] == i + 1:
                    ns = tuple(
                        a if j == i else
                        b if j == i + 1 else
                        (b if x == a else a if x == b else x)
                        for j, x in enumerate(s)
                    )
                else:
                    # Otherwise the first-occurrence order is unchanged, so
                    # the simple adjacent swap is already canonical.
                    ns = s[:i] + (b, a) + s[i + 2:]

                if ns not in dist:
                    dist[ns] = base + 1
                    q.append(ns)

        # Reverse deletions: prepend an equal block.
        if k < max_len:
            dmax = max(s) + 1 if s else 0
            max_add = max_len - k

            # Prepend a new value: new label becomes 0, old labels shift +1.
            mapped_new = tuple(x + 1 for x in s) if s else ()
            for length in range(1, max_add + 1):
                ns = zero_blocks[length] + mapped_new
                if ns not in dist:
                    dist[ns] = base + 1
                    q.append(ns)

            # Prepend an existing value v.
            # v becomes label 0; labels < v shift +1; labels > v stay.
            for v in range(dmax):
                mapped = tuple(
                    0 if x == v else (x + 1 if x < v else x)
                    for x in s
                )
                for length in range(1, max_add + 1):
                    ns = zero_blocks[length] + mapped
                    if ns not in dist:
                        dist[ns] = base + 1
                        q.append(ns)

    return dist


def gen_canon(n):
    res = []

    def rec(prefix, max_label):
        if len(prefix) == n:
            res.append(tuple(prefix))
            return
        for v in range(max_label + 2):
            rec(prefix + [v], max(max_label, v))

    rec([], -1)
    return res


def check_dist(dist, max_len, check_missing=True, random_trials=0):
    missing = []

    if check_missing:
        for n in range(1, max_len + 1):
            for s in gen_canon(n):
                if s not in dist:
                    missing.append(s)

    mismatches = []

    # Exhaustively check every canonical state in the BFS state space.
    for s, want in dist.items():
        got = dp_min(tuple(x + 1 for x in s))
        if got != want:
            mismatches.append((s, got, want))

    random_checked = 0
    if random_trials:
        import random
        rng = random.Random(123456789)
        lo = max(1, max_len - 1)

        for _ in range(random_trials):
            n = rng.randint(lo, max_len)
            seq = tuple(rng.randint(1, min(n, 5)) for _ in range(n))
            c = canonicalize(seq)
            random_checked += 1

            if c not in dist:
                missing.append(c)
                continue

            got = dp_min(seq)
            want = dist[c]
            if got != want:
                mismatches.append((c, got, want))

    lines = [f"Checked {len(dist)} brute-force states up to length {max_len}."]
    if random_checked:
        lines.append(f"Random raw sequences checked: {random_checked}.")

    if missing:
        lines.append(f"Missing {len(missing)} patterns in brute-force BFS.")
        for s in missing[:20]:
            lines.append(f"missing {s}")

    if mismatches:
        lines.append(f"Counterexamples found: {len(mismatches)}")
        for s, got, want in mismatches[:20]:
            lines.append(f"seq={tuple(x + 1 for x in s)} dp={got} brute={want}")
    else:
        lines.append("No counterexamples found.")

    return "\n".join(lines)


def verify(max_len, random_trials=0):
    dist = brute_distances(max_len)
    return check_dist(dist, max_len, True, random_trials)


def run_tests():
    # Exhaustive verifier for all equality patterns of length <= 8.
    report8 = verify(8)
    print(report8)

    # If the small exhaustive verifier passes, stress/exhaustively check
    # canonical patterns up to length 10 and random raw sequences of length 9/10.
    if "No counterexamples found." in report8 and "Missing" not in report8:
        dist10 = brute_distances(10)
        report10 = check_dist(dist10, 10, True, 1000)
        print(report10)


def main():
    data = sys.stdin.buffer.read().split()
    if data:
        solve_original_from_ints(list(map(int, data)))
    else:
        run_tests()


if __name__ == "__main__":
    main()