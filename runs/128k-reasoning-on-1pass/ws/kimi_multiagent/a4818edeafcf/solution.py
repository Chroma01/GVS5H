import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[i])

    NEG = -10**18

    # prefix distinct counts: P[i] = distinct values in A[1..i]
    P = [0] * (n + 1)
    seen = bytearray(n + 1)
    c = 0
    for i in range(1, n + 1):
        v = A[i]
        if not seen[v]:
            seen[v] = 1
            c += 1
        P[i] = c

    # suffix distinct counts: S[i] = distinct values in A[i..n]
    S = [0] * (n + 2)
    seen = bytearray(n + 1)
    c = 0
    for i in range(n, 0, -1):
        v = A[i]
        if not seen[v]:
            seen[v] = 1
            c += 1
        S[i] = c

    # Segment tree over left-cut positions i (1..n-2 become active over time).
    # Invariant maintained: tree[p] = (true max of subtree p) - (lazy on strict ancestors of p).
    # Because we only ever need tree[1] (root, no ancestors) and every update is a
    # range add followed by rebuilding both boundary paths, no push-downs are needed.
    size = 1
    while size < n + 1:
        size <<= 1

    tree = [NEG] * (2 * size)
    lazy = [0] * (2 * size)

    last = [0] * (n + 1)  # last occurrence position of each value
    ans = 0

    # Sweep right cut j = 2 .. n-1. tree[i] (active i < j) holds P[i] + distinct(A[i+1..j]).
    for j in range(2, n):
        x = A[j]
        prev = last[x]
        last[x] = j
        l = prev if prev > 1 else 1   # A[j] is newly distinct in middle iff i >= prev
        R = j - 1
        l0 = l + size
        r0 = R + size

        # Activate left-cut position R with base value P[R].
        # (Its ancestors provably have lazy 0: any node with pending lazy lies
        #  entirely inside some past update range ending <= R-1.)
        tree[r0] = P[R]

        # Range add +1 on [l0, r0]: x = A[j] becomes one more distinct middle value
        while l0 <= r0:
            if l0 & 1:
                tree[l0] += 1
                lazy[l0] += 1
                l0 += 1
            if not (r0 & 1):
                tree[r0] += 1
                lazy[r0] += 1
                r0 -= 1
            l0 >>= 1
            r0 >>= 1

        # Rebuild ancestors of the two boundary leaves
        p = (l + size) >> 1
        while p:
            a = tree[p << 1]
            b = tree[p << 1 | 1]
            tree[p] = (a if a > b else b) + lazy[p]
            p >>= 1
        p = (R + size) >> 1
        while p:
            a = tree[p << 1]
            b = tree[p << 1 | 1]
            tree[p] = (a if a > b else b) + lazy[p]
            p >>= 1

        # tree[1] = max over active i of P[i] + distinct(A[i+1..j])
        cand = tree[1] + S[j + 1]
        if cand > ans:
            ans = cand

    sys.stdout.write(str(ans) + "\n")

main()