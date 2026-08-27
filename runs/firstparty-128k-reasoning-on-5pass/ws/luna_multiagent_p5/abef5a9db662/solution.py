import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    contests = [(next(it), next(it)) for _ in range(n)]
    q = next(it)
    queries = [next(it) for _ in range(q)]

    M = 500_000
    S = 1
    while S < M:
        S <<= 1

    neg_inf = -10**18
    maxv = [neg_inf] * (2 * S)
    lazy = [0] * (2 * S)

    maxv[S:S + M] = range(1, M + 1)
    for i in range(S - 1, 0, -1):
        left = maxv[i << 1]
        right = maxv[i << 1 | 1]
        maxv[i] = left if left > right else right

    def push(node):
        z = lazy[node]
        if z:
            left = node << 1
            right = left | 1
            maxv[left] += z
            maxv[right] += z
            lazy[left] += z
            lazy[right] += z
            lazy[node] = 0

    def first_at_least(node, l, r, target):
        if l >= M or maxv[node] < target:
            return M
        if r - l == 1:
            return l

        push(node)
        mid = (l + r) >> 1
        res = first_at_least(node << 1, l, mid, target)
        if res != M:
            return res
        return first_at_least(node << 1 | 1, mid, r, target)

    def first_greater(node, l, r, target):
        if l >= M or maxv[node] <= target:
            return M
        if r - l == 1:
            return l

        push(node)
        mid = (l + r) >> 1
        res = first_greater(node << 1, l, mid, target)
        if res != M:
            return res
        return first_greater(node << 1 | 1, mid, r, target)

    def range_add(node, l, r, ql, qr):
        if qr <= l or r <= ql:
            return
        if ql <= l and r <= qr:
            maxv[node] += 1
            lazy[node] += 1
            return

        push(node)
        mid = (l + r) >> 1
        range_add(node << 1, l, mid, ql, qr)
        range_add(node << 1 | 1, mid, r, ql, qr)
        left = maxv[node << 1]
        right = maxv[node << 1 | 1]
        maxv[node] = left if left > right else right

    for L, R in contests:
        left = first_at_least(1, 0, S, L)
        if left == M:
            continue

        right_exclusive = first_greater(1, 0, S, R)
        if right_exclusive == M:
            right_exclusive = M

        if left < right_exclusive:
            range_add(1, 0, S, left, right_exclusive)

    for node in range(1, S):
        z = lazy[node]
        if z:
            left = node << 1
            right = left | 1
            maxv[left] += z
            maxv[right] += z
            lazy[left] += z
            lazy[right] += z
            lazy[node] = 0

    out = []
    for x in queries:
        out.append(str(maxv[S + x - 1]))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()