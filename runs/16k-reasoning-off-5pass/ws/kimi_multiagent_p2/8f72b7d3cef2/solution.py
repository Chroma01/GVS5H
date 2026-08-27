import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]

    # prefix sums, P[i] = sum of A[0..i-1]
    P = [0] * (n + 1)
    s = 0
    for i in range(n):
        s += A[i]
        P[i + 1] = s

    # right-only closure: rend[i] = furthest right index reachable starting
    # alone at i moving only right; computed via monotonic stack swept right->left.
    # stack entries: (threshold = A_j, block_sum, block_right_end)
    rend = [0] * n
    st_thr = [0] * n
    st_sum = [0] * n
    st_end = [0] * n
    top = 0  # stack size
    for i in range(n - 1, -1, -1):
        cur = A[i]
        end = i
        while top > 0 and st_thr[top - 1] < cur:
            top -= 1
            cur += st_sum[top]
            end = st_end[top]
        rend[i] = end
        st_thr[top] = A[i]
        st_sum[top] = cur
        st_end[top] = end
        top += 1

    # left-only closure: lend[i] = furthest left index reachable starting
    # alone at i moving only left; stack swept left->right.
    # stack entries: (threshold = A_j, block_sum, block_left_end)
    lend = [0] * n
    top = 0
    for i in range(n):
        cur = A[i]
        l = i
        while top > 0 and st_thr[top - 1] < cur:
            top -= 1
            cur += st_sum[top]
            l = st_end[top]
        lend[i] = l
        st_thr[top] = A[i]
        st_sum[top] = cur
        st_end[top] = l
        top += 1

    out = [0] * n
    a = A
    p = P
    ld = lend
    rd = rend
    for k in range(n):
        L = k
        R = k
        S = a[k]
        while True:
            # absorb left as far as possible (in jumps)
            while L > 0:
                q = L - 1
                if a[q] < S:
                    nl = ld[q]
                    S += p[q + 1] - p[nl]
                    L = nl
                else:
                    break
            # absorb right as far as possible (in jumps)
            while R < n - 1:
                q = R + 1
                if a[q] < S:
                    nr = rd[q]
                    S += p[nr + 1] - p[q]
                    R = nr
                else:
                    break
            # check whether any further progress is possible
            if (L == 0 or a[L - 1] >= S) and (R == n - 1 or a[R + 1] >= S):
                break
        out[k] = S

    sys.stdout.write(' '.join(map(str, out)))

main()