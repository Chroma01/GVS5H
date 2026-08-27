import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[i])
    P = [0] * (n + 1)
    s = 0
    for i in range(1, n + 1):
        s += A[i]
        P[i] = s

    # Sparse table for range-argmax queries over A[1..n]
    logt = [0] * (n + 2)
    for i in range(2, n + 2):
        logt[i] = logt[i >> 1] + 1
    st = [list(range(n + 1))]
    length = 2
    while length <= n:
        prev = st[-1]
        half = length >> 1
        cur = [0] * (n - length + 2)
        for i in range(n - length + 2):
            a = prev[i]
            b = prev[i + half]
            cur[i] = a if A[a] >= A[b] else b
        st.append(cur)
        length <<= 1

    def argmax(l, r):
        k = logt[r - l + 1]
        row = st[k]
        a = row[l]
        b = row[r - (1 << k) + 1]
        return a if A[a] >= A[b] else b

    INF = 1 << 62
    ans = [0] * (n + 1)

    # Iterative divide and conquer.
    # State: (l, r, wall, wall_ans)
    #   wall     = value of the external blocker adjacent to [l,r] on the side
    #              facing the parent max (INF if none / array boundary).
    #   wall_ans = answer assigned to any starter whose internal final sum
    #              exceeds wall (such a starter crosses the wall, absorbs the
    #              parent max's whole closed segment, and ends with wall_ans).
    stack = [(1, n, INF, 0)]
    while stack:
        l, r, wall, wall_ans = stack.pop()
        if l > r:
            continue
        p = argmax(l, r)
        # Closed segment [L,R] of p within [l,r]: greedy expansion.
        L = p
        R = p
        S = A[p]
        while True:
            while L > l and A[L - 1] < S:
                L -= 1
                S += A[L]
            while R < r and A[R + 1] < S:
                R += 1
                S += A[R]
            if (L > l and A[L - 1] < S) or (R < r and A[R + 1] < S):
                continue
            break
        ans[p] = wall_ans if S > wall else S
        ap = ans[p]
        # Outer-left part: crossing blocker A[L-1] leads into p's segment.
        if l <= L - 1:
            stack.append((l, L - 1, A[L - 1], ap))
        # Inner-left part: crossing p (value A[p]) leads into p's segment.
        if L <= p - 1:
            stack.append((L, p - 1, A[p], ap))
        # Inner-right part.
        if p + 1 <= R:
            stack.append((p + 1, R, A[p], ap))
        # Outer-right part.
        if R + 1 <= r:
            stack.append((R + 1, r, A[R + 1], ap))

    out = ' '.join(str(ans[i]) for i in range(1, n + 1))
    sys.stdout.write(out + '\n')

main()