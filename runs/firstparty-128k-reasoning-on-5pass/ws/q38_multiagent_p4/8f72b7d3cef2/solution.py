import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    N1 = N + 1
    A = [0] + data[1:] + [0]
    del data

    pref = [0] * (N + 2)
    s = 0
    for i in range(1, N + 1):
        s += A[i]
        pref[i + 1] = s

    prev = [0] * (N + 2)
    st = []
    for i in range(1, N + 1):
        ai = A[i]
        while st and A[st[-1]] <= ai:
            st.pop()
        if st:
            prev[i] = st[-1]
        st.append(i)

    node_of = [0] * (N + 2)
    node_L = [0]
    node_R = [0]
    node_max = [0]
    good = bytearray(N + 2)
    keys = {}
    shift = N1.bit_length()
    shift2 = shift * 2
    st = []
    get = keys.get

    for i in range(N, 0, -1):
        ai = A[i]
        while st and A[st[-1]] <= ai:
            st.pop()
        if st:
            nxt = st[-1]
        else:
            nxt = N1
        st.append(i)

        L = prev[i]
        key = (ai << shift2) | (L << shift) | nxt
        nid = get(key)
        if nid is None:
            nid = len(node_L)
            keys[key] = nid
            node_L.append(L)
            node_R.append(nxt)
            node_max.append(ai)
        node_of[i] = nid

        if (i > L + 1 and A[i - 1] < ai) or (i < nxt - 1 and A[i + 1] < ai):
            good[i] = 1

    M = len(node_L) - 1
    del get, keys, st, prev

    node_sum = [0] * (M + 1)
    barrier = [0] * (M + 1)
    first = [0] * (M + 1)
    sibling = [0] * (M + 1)
    bad = bytearray(M + 1)
    root = 1

    for v in range(1, M + 1):
        L = node_L[v]
        R = node_R[v]
        node_sum[v] = pref[R] - pref[L + 1]

        if L == 0:
            if R == N1:
                p = 0
            else:
                p = node_of[R]
        elif R == N1:
            p = node_of[L]
        else:
            if A[L] <= A[R]:
                p = node_of[L]
            else:
                p = node_of[R]

        barrier[v] = p
        if p:
            if node_sum[v] <= node_max[p]:
                bad[v] = 1
            sibling[v] = first[p]
            first[p] = v
        else:
            root = v

    del pref, node_L, node_R

    dp = node_max
    del node_max

    root_sum = node_sum[root]
    barrier[root] = 0
    stack = [root]

    while stack:
        v = stack.pop()
        b = barrier[v]
        if b:
            dp[v] = node_sum[b]
        else:
            dp[v] = root_sum

        c = first[v]
        while c:
            if bad[c]:
                barrier[c] = c
            else:
                barrier[c] = b
            stack.append(c)
            c = sibling[c]

    del node_sum, first, sibling, bad, barrier, stack

    out = [str(dp[node_of[i]]) if good[i] else str(A[i]) for i in range(1, N + 1)]
    sys.stdout.write(' '.join(out))
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()