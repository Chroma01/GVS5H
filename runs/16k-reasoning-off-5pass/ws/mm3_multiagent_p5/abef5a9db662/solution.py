import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    MAX_R = 500000
    # Maximum possible rating: start at most 500000, and can increase by at most N per step.
    # After exceeding MAX_R, cnt becomes 0, but we must allocate enough space to avoid index errors.
    S = MAX_R + N + 5
    cnt = [0] * (S + 2)
    for _ in range(N):
        L = int(next(it)); R = int(next(it))
        cnt[L] += 1
        if R + 1 <= S:
            cnt[R + 1] -= 1
    # prefix sum to get cnt for all positions up to S
    for i in range(1, S + 1):
        cnt[i] += cnt[i-1]
    # After MAX_R, cnt should be 0, but we ensure it explicitly to be safe
    for i in range(MAX_R + 1, S + 1):
        cnt[i] = 0
    # build next: for i > MAX_R, cnt[i] == 0, so next[i] = i
    nxt = [0] * (S + 2)
    for i in range(1, S + 1):
        nxt[i] = i + cnt[i]
    # binary lifting table
    LOG = 20  # 2^20 = 1,048,576 > 700,000
    up = [[0] * (S + 2) for _ in range(LOG)]
    for i in range(1, S + 1):
        up[0][i] = nxt[i]
    for k in range(1, LOG):
        prev = up[k-1]
        curr = up[k]
        for i in range(1, S + 1):
            j = prev[i]
            if j > S:
                j = S
            curr[i] = prev[j]
    Q = int(next(it))
    out_lines = []
    for _ in range(Q):
        X = int(next(it))
        cur = X
        for k in range(LOG-1, -1, -1):
            if up[k][cur] != cur:
                cur = up[k][cur]
        out_lines.append(str(cur))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()