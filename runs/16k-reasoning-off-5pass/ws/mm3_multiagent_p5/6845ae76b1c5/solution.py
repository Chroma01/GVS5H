import sys
import bisect

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    K = int(next(it))
    queries = []
    for idx in range(K):
        x = int(next(it))
        y = int(next(it))
        queries.append((y, x, idx))  # sort by Y, keep X and original index

    # Coordinate compression of A values
    sorted_A_vals = sorted(set(A))
    M = len(sorted_A_vals)
    # Map A value to compressed index (1-based for BIT)
    def comp_a(val):
        # bisect_right gives number of elements <= val
        return bisect.bisect_right(sorted_A_vals, val)

    # Fenwick tree implementation
    class BIT:
        __slots__ = ('n', 'tree')
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        def add(self, i, v):
            # i is 1-based
            n = self.n
            tree = self.tree
            while i <= n:
                tree[i] += v
                i += i & -i
        def sum(self, i):
            # sum of [1..i]
            s = 0
            tree = self.tree
            while i > 0:
                s += tree[i]
                i -= i & -i
            return s

    bit_cnt = BIT(M)
    bit_sum = BIT(M)

    # Sort queries by Y
    queries.sort()
    answers = [0] * K
    cur_total = 0
    bj = 0  # number of B elements processed (0-indexed count)
    ai = 0  # number of A elements inserted into BITs

    total_cnt = 0
    total_sum = 0

    for y, x, qid in queries:
        # Add B elements up to index y (1-based)
        while bj < y:
            bj += 1
            b_val = B[bj - 1]
            # Find compressed index for b_val in A's compression
            idx = comp_a(b_val)
            cntL = bit_cnt.sum(idx)
            sumL = bit_sum.sum(idx)
            cntR = total_cnt - cntL
            sumR = total_sum - sumL
            # contribution = (cntL * b_val - sumL) + (sumR - cntR * b_val)
            cur_total += cntL * b_val - sumL + sumR - cntR * b_val
        # Add A elements up to index x (1-based)
        while ai < x:
            ai += 1
            a_val = A[ai - 1]
            idx = comp_a(a_val)
            bit_cnt.add(idx, 1)
            bit_sum.add(idx, a_val)
            total_cnt += 1
            total_sum += a_val
        answers[qid] = cur_total

    out = '\n'.join(str(v) for v in answers)
    sys.stdout.write(out)

if __name__ == "__main__":
    solve()