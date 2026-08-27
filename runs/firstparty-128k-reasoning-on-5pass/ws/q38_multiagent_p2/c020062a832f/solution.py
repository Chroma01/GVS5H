import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]

    bit = [0] * (M + 1)
    cnt = [0] * M
    pos_sum = [0] * M

    ans = 0

    # Compute inversion count for k = 0, and record counts / position sums.
    for i in range(1, N + 1):
        a = data[i + 1]  # A_i, 1-based position i
        idx = a + 1

        # Number of previous elements with value <= a
        s = 0
        j = idx
        while j > 0:
            s += bit[j]
            j -= j & -j

        # Previous elements with value > a
        ans += (i - 1) - s

        # Add current value to Fenwick tree
        j = idx
        while j <= M:
            bit[j] += 1
            j += j & -j

        cnt[a] += 1
        pos_sum[a] += i

    out = []
    append = out.append
    n1 = N + 1

    # Sweep k = 0 .. M-1.
    # Transition k -> k+1 wraps original value c = M-1-k from M-1 to 0.
    for k in range(M):
        append(str(ans))
        if k + 1 < M:
            c = M - 1 - k
            t = cnt[c]
            if t:
                ans += 2 * pos_sum[c] - t * n1

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()