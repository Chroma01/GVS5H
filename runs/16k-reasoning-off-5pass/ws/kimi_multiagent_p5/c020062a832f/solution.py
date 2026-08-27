import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    A = [int(x) for x in data[idx:idx + N]]

    if M == 1:
        # All values are always 0, no inversions ever.
        sys.stdout.write('0\n')
        return

    # ---------- Fenwick tree (1-indexed) ----------
    class BIT:
        __slots__ = ('n', 't')
        def __init__(self, n):
            self.n = n
            self.t = [0] * (n + 1)
        def add(self, i, v):
            t = self.t; n = self.n
            while i <= n:
                t[i] += v
                i += i & -i
        def sum(self, i):
            s = 0; t = self.t
            while i > 0:
                s += t[i]
                i -= i & -i
            return s
        # count of elements in (l, r]  i.e. l < pos <= r
        def range_sum(self, l, r):
            return self.sum(r) - self.sum(l)

    # ---------- initial inversion count (k = 0) ----------
    bit_val = BIT(M)  # over values 0..M-1 -> indices 1..M
    inv = 0
    for i, x in enumerate(A):
        # number of previous elements greater than x
        inv += i - bit_val.sum(x + 1)  # sum(x+1) counts values <= x
        bit_val.add(x + 1, 1)

    # positions grouped by original value A_i
    pos_by_val = [[] for _ in range(M)]
    for i, x in enumerate(A):
        pos_by_val[x].append(i + 1)  # 1-indexed positions

    # BIT over positions of elements currently holding value M-1
    bit_max = BIT(N)
    for p in pos_by_val[M - 1]:
        bit_max.add(p, 1)

    answers = [0] * M
    answers[0] = inv

    cur = inv
    # transition from k to k+1, for k = 0 .. M-2
    for k in range(M - 1):
        # elements currently at value M-1 are those with A_i = M-1-k
        # (0 <= k <= M-2, so v in [1, M-1]; no modulo needed)
        v = M - 1 - k
        S = pos_by_val[v]
        if S:
            delta = 0
            # Compute all deltas BEFORE mutating bit_max.
            # At state k+1 the zero-valued elements are exactly S, so:
            #   after = earlier elements with value > 0 = (p-1) - earlier_in_S
            for p in S:
                later_in_S = bit_max.range_sum(p, N)   # later elements also wrapping
                earlier_in_S = bit_max.sum(p - 1)      # earlier elements also wrapping
                # before: p (value M-1) is greater than later elements of value < M-1
                before = (N - p) - later_in_S
                # after: p (value 0) is smaller than earlier elements of value > 0
                after = (p - 1) - earlier_in_S
                delta += after - before
            cur += delta
            # migrate S out of the max-set (they are now value 0)
            for p in S:
                bit_max.add(p, -1)
        answers[k + 1] = cur

    sys.stdout.write('\n'.join(map(str, answers)) + '\n')

solve()