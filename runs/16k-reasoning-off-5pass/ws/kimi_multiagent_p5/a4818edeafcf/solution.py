import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]

    first = [0] * (n + 1)
    last = [0] * (n + 1)
    for idx, v in enumerate(A, 1):
        if first[v] == 0:
            first[v] = idx
        last[v] = idx

    # prefix distinct counts P[i] = distinct in A[1..i]
    P = [0] * (n + 1)
    seen = bytearray(n + 1)
    c = 0
    for i in range(1, n + 1):
        if not seen[A[i - 1]]:
            seen[A[i - 1]] = 1
            c += 1
        P[i] = c

    # suffix distinct counts S[i] = distinct in A[i..n]
    S = [0] * (n + 2)
    seen = bytearray(n + 1)
    c = 0
    for i in range(n, 0, -1):
        if not seen[A[i - 1]]:
            seen[A[i - 1]] = 1
            c += 1
        S[i] = c

    # bucket values by last occurrence
    bucket = [[] for _ in range(n + 1)]
    for v in range(1, n + 1):
        if first[v] != 0:
            bucket[last[v]].append(first[v])

    # lazy segment tree over indices 1..n, initialized with P[i]
    size = 1
    while size < n + 2:
        size <<= 1
    NEG = float('-inf')
    mx = [0] * (2 * size)
    lazy = [0] * (2 * size)
    for i in range(1, n + 1):
        mx[size + i] = P[i]
    for i in range(size - 1, 0, -1):
        mx[i] = max(mx[2 * i], mx[2 * i + 1])

    def push(node):
        if lazy[node]:
            v = lazy[node]
            lazy[2 * node] += v
            mx[2 * node] += v
            lazy[2 * node + 1] += v
            mx[2 * node + 1] += v
            lazy[node] = 0

    def range_add(node, nl, nr, l, r, val):
        if r < nl or nr < l:
            return
        if l <= nl and nr <= r:
            mx[node] += val
            lazy[node] += val
            return
        push(node)
        mid = (nl + nr) // 2
        range_add(2 * node, nl, mid, l, r, val)
        range_add(2 * node + 1, mid + 1, nr, l, r, val)
        mx[node] = max(mx[2 * node], mx[2 * node + 1])

    def range_max(node, nl, nr, l, r):
        if r < nl or nr < l:
            return NEG
        if l <= nl and nr <= r:
            return mx[node]
        push(node)
        mid = (nl + nr) // 2
        return max(range_max(2 * node, nl, mid, l, r),
                   range_max(2 * node + 1, mid + 1, nr, l, r))

    ans = 0
    for j in range(2, n):  # j from 2 to n-1
        for f in bucket[j]:
            if f >= 2:
                range_add(1, 0, size - 1, 1, f - 1, 1)
        best_i = range_max(1, 0, size - 1, 1, j - 1)
        total = best_i + S[j + 1]
        if total > ans:
            ans = total

    print(ans)

main()