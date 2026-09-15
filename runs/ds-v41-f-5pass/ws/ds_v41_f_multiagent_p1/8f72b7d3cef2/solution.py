import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[i])
    del data

    P = [0] * (n + 1)
    s = 0
    for i in range(1, n + 1):
        s += A[i]
        P[i] = s

    lo = [0] * (n + 1)
    st = []
    for i in range(1, n + 1):
        ai = A[i]
        while st and A[st[-1]] < ai:
            st.pop()
        lo[i] = st[-1] + 1 if st else 1
        st.append(i)

    hi = [0] * (n + 1)
    st = []
    for i in range(n, 0, -1):
        ai = A[i]
        while st and A[st[-1]] <= ai:
            st.pop()
        hi[i] = st[-1] - 1 if st else n
        st.append(i)

    reach = [0] * (n + 1)

    for i in range(1, n + 1):
        if reach[i]:
            continue
        path = []
        cur = i
        while True:
            if reach[cur]:
                res = reach[cur]
                break
            l = lo[cur]
            h = hi[cur]
            W = P[h] - P[l - 1]
            if l > 1 and A[l - 1] < W:
                path.append(cur)
                cur = l - 1
            elif h < n and A[h + 1] < W:
                path.append(cur)
                cur = h + 1
            else:
                reach[cur] = cur
                res = cur
                break
        for node in path:
            reach[node] = res

    out = []
    append = out.append
    for k in range(1, n + 1):
        if lo[k] == k and k < n and A[k + 1] == A[k]:
            append(A[k])
        else:
            r = reach[k]
            append(P[hi[r]] - P[lo[r] - 1])

    sys.stdout.write(' '.join(map(str, out)))
    sys.stdout.write('\n')

main()