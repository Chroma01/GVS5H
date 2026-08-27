import sys


def main():
    input = sys.stdin.buffer.readline
    N, M = map(int, input().split())
    intervals = [tuple(map(int, input().split())) for _ in range(M)]

    def output(cost, ans):
        sys.stdout.write(str(cost) + "\n")
        sys.stdout.write(" ".join(map(str, ans)) + "\n")

    # Cost 1: one type-1 operation covers the whole sequence.
    for i, (l, r) in enumerate(intervals):
        if l == 1 and r == N:
            ans = [0] * M
            ans[i] = 1
            output(1, ans)
            return

    # Sort by left endpoint ascending and right endpoint descending.
    # Therefore, any earlier interval having R >= current R contains current.
    order = sorted(range(M), key=lambda i: (intervals[i][0], -intervals[i][1]))

    # Coordinate-compressed Fenwick tree for prefix minimum.
    # A right endpoint R is mapped in reverse order, so R' >= R becomes
    # a Fenwick prefix query. The tree stores the minimum original index.
    rights = sorted({r for _, r in intervals})
    right_pos = {r: i for i, r in enumerate(rights)}
    size = len(rights)
    inf = M + 1
    bit = [inf] * (size + 1)

    def update(pos, value):
        while pos <= size:
            if value < bit[pos]:
                bit[pos] = value
            pos += pos & -pos

    def query(pos):
        result = inf
        while pos > 0:
            if bit[pos] < result:
                result = bit[pos]
            pos -= pos & -pos
        return result

    # Cost 2: type 2 on A and type 1 on B, where A is contained in B.
    # For each current interval, select the smallest original operation index
    # among earlier containing intervals.
    for i in order:
        _, r = intervals[i]
        reversed_pos = size - right_pos[r]
        witness = query(reversed_pos)
        if witness != inf:
            ans = [0] * M
            ans[i] = 2
            ans[witness] = 1
            output(2, ans)
            return
        update(reversed_pos, i)

    # Cost 2: two type-1 operations whose intervals together cover [1, N].
    best_left_r = -1
    best_left_idx = -1
    best_right_l = N + 1
    best_right_idx = -1

    for i, (l, r) in enumerate(intervals):
        if l == 1 and r > best_left_r:
            best_left_r = r
            best_left_idx = i
        if r == N and l < best_right_l:
            best_right_l = l
            best_right_idx = i

    if best_left_idx != -1 and best_right_idx != -1:
        if best_left_r >= best_right_l:
            ans = [0] * M
            ans[best_left_idx] = 1
            ans[best_right_idx] = 1
            output(2, ans)
            return

    # Cost 2: two type-2 operations. Their complements cover everything
    # exactly when their original intervals are disjoint.
    max_r = -1
    max_r_idx = -1
    for i in order:
        l, r = intervals[i]
        if max_r_idx != -1 and max_r < l:
            ans = [0] * M
            ans[max_r_idx] = 2
            ans[i] = 2
            output(2, ans)
            return
        if r > max_r:
            max_r = r
            max_r_idx = i

    # For M >= 3, choose type 2 on intervals with maximum L and minimum R.
    # The region missed by both is contained in every interval, so type 1 on
    # any third interval covers it.
    if M >= 3:
        p = max(range(M), key=lambda i: intervals[i][0])
        q = min(range(M), key=lambda i: intervals[i][1])

        if p != q:
            k = next(i for i in range(M) if i != p and i != q)
            ans = [0] * M
            ans[p] = 2
            ans[q] = 2
            ans[k] = 1
            output(3, ans)
            return

    sys.stdout.write("-1\n")


if __name__ == "__main__":
    main()