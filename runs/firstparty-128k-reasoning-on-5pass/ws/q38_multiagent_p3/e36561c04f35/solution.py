import sys
from collections import deque
from itertools import product
import random


def greedy(A):
    n = len(A)
    if n == 0:
        return 0

    INF = n + 1
    maxv = max(A)

    # nxt[i] = next position of the same value as A[i], or INF
    nxt = [INF] * n
    last = [INF] * (maxv + 1)
    for i in range(n - 1, -1, -1):
        v = A[i]
        nxt[i] = last[v]
        last[v] = i

    # latest[v] = index in the stack of the newest batch of value v
    latest = [-1] * (maxv + 1)

    # Stack of batches in creation order.
    # firsts[k] = first position of batch k
    # sizes[k]  = number of elements currently assigned to batch k
    firsts = []
    sizes = []

    cost = 0

    for i, v in enumerate(A):
        idx = latest[v]
        top = len(sizes) - 1

        if idx == -1:
            # First occurrence of this value: must start a batch.
            firsts.append(i)
            sizes.append(1)
            latest[v] = len(sizes) - 1
            cost += 1

        elif idx == top:
            # No newer elements above this batch: continue for free.
            sizes[idx] += 1

        elif idx == top - 1 and sizes[-1] == 1:
            # Exactly one newer element exists: the only element of the top batch.
            # Continuing costs 1 inversion; starting a new batch costs 1 deletion.
            # Tie-break by the earlier next occurrence.
            cost += 1
            if nxt[i] < nxt[firsts[-1]]:
                firsts.append(i)
                sizes.append(1)
                latest[v] = len(sizes) - 1
            else:
                sizes[idx] += 1

        else:
            # At least two newer elements exist: starting a new batch is better.
            firsts.append(i)
            sizes.append(1)
            latest[v] = len(sizes) - 1
            cost += 1

    return cost


_EXACT_DIST = None


def precompute_dist(max_len, alphabet):
    """
    Exact distances for all sequences of length <= max_len over values 1..alphabet.

    Reverse operations:
      - adjacent swap
      - prepend a non-empty monochromatic run

    Since every forward operation has a reverse operation of the same cost,
    the distance from empty to a sequence equals the minimum operations to
    delete that sequence to empty.
    """
    dist = {(): 0}
    q = deque([()])

    while q:
        s = q.popleft()
        d = dist[s]
        L = len(s)

        # Reverse of adjacent swap.
        for i in range(L - 1):
            if s[i] == s[i + 1]:
                continue
            t = s[:i] + (s[i + 1], s[i]) + s[i + 2:]
            if t not in dist:
                dist[t] = d + 1
                q.append(t)

        # Reverse of deleting a monochromatic prefix.
        rem = max_len - L
        if rem > 0:
            for v in range(1, alphabet + 1):
                prefix = ()
                for _ in range(rem):
                    prefix = prefix + (v,)
                    t = prefix + s
                    if t not in dist:
                        dist[t] = d + 1
                        q.append(t)

    return dist


def _ensure_exact_dist():
    global _EXACT_DIST
    if _EXACT_DIST is None:
        _EXACT_DIST = precompute_dist(9, 3)
    return _EXACT_DIST


def brute_force(A):
    """Exact verifier for small sequences (length <= 9, values <= 3)."""
    t = tuple(A)
    if len(t) > 9 or (t and max(t) > 3):
        raise ValueError("brute_force only supports length <= 9 and values <= 3")
    return _ensure_exact_dist()[t]


def selftest():
    failures = []
    _ensure_exact_dist()

    def check(seq):
        g = greedy(seq)
        e = brute_force(seq)
        if g != e:
            failures.append((list(seq), e, g))

    def check_expected(seq, expected):
        g = greedy(seq)
        if g != expected:
            failures.append((list(seq), expected, g))

    # Sample cases.
    check_expected((1, 1, 2, 1, 2), 3)
    check_expected((4, 2, 1, 3), 4)
    check_expected((1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1), 8)

    # Required exhaustive: all sequences of length up to 7 over alphabets 1, 2, 3.
    for k in (1, 2, 3):
        for n in range(0, 8):
            for seq in product(range(1, k + 1), repeat=n):
                check(seq)

    # Required exhaustive: all length 8 over alphabet size 2.
    for seq in product(range(1, 3), repeat=8):
        check(seq)

    # Extra exhaustive: all length 8 and 9 over alphabet size 3.
    for n in (8, 9):
        for seq in product(range(1, 4), repeat=n):
            check(seq)

    # Required random: 500 seeded random sequences of length 8-9 over alphabet size 3.
    random.seed(123456789)
    for _ in range(500):
        n = random.randint(8, 9)
        seq = tuple(random.randint(1, 3) for _ in range(n))
        check(seq)

    if failures:
        print("FAIL")
        print(f"{len(failures)} mismatches")
        for seq, e, g in failures[:10]:
            print(f"seq={seq} exact={e} greedy={g}")
        sys.exit(1)
    else:
        print("PASS")


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    t = int(next(it))
    out = []

    for _ in range(t):
        n = int(next(it))
        A = [int(next(it)) for _ in range(n)]
        out.append(str(greedy(A)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
    else:
        main()