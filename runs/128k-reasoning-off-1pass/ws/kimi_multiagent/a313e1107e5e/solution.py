import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    queries = []
    for qi in range(Q):
        R = int(next(it))
        X = int(next(it))
        queries.append((R, X, qi))

    # Coordinate compress all A values (tails entries are always some A_i)
    comp = sorted(set(A))
    C = len(comp)

    # Pass 1: record tails update events.
    # tails[k] = minimum possible last value of an increasing subsequence of length k+1.
    # Event: (position_in_tails, old_value, new_value); old_value None means "append".
    events = []
    tails = []
    for a in A:
        pos = bisect_left(tails, a)
        if pos == len(tails):
            events.append((pos, None, a))
            tails.append(a)
        else:
            events.append((pos, tails[pos], a))
            tails[pos] = a

    # Fenwick tree over compressed values, counting current tails entries.
    bit = [0] * (C + 1)

    def bit_add(i, delta):
        # i is 0-indexed compressed position
        i += 1
        while i <= C:
            bit[i] += delta
            i += i & (-i)

    def bit_sum(i):
        # sum over compressed positions [0, i), i.e., i elements
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s

    # Sort queries by R, sweep, replaying events.
    queries.sort(key=lambda t: t[0])
    ans = [0] * Q
    cur = 0  # number of events applied so far (== current prefix length)
    for R, X, qi in queries:
        while cur < R:
            pos, old, new = events[cur]
            if old is not None:
                bit_add(bisect_left(comp, old), -1)
            bit_add(bisect_left(comp, new), 1)
            cur += 1
        # Number of tails entries with value <= X
        k = bisect_right(comp, X)
        ans[qi] = bit_sum(k)

    out = sys.stdout
    out.write("\n".join(map(str, ans)) + "\n")

main()