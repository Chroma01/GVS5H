import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    Q = int(next(it))
    queries = [(int(next(it)) - 1, int(next(it)) - 1) for _ in range(Q)]  # 0-indexed inclusive

    # Compute nxt[i]: smallest j > i with A[j] >= 2*A[i], or N if none
    nxt = [N] * N
    j = 0
    for i in range(N):
        if j < i + 1:
            j = i + 1
        while j < N and A[j] < 2 * A[i]:
            j += 1
        if j < N:
            nxt[i] = j
        # else remains N

    LOG = (N + 1).bit_length()
    # jump[k][i] = position after 2^k greedy pairings starting at i, or N if impossible
    jump = [[N] * (N + 1) for _ in range(LOG)]
    # 0 steps: N (sentinel)
    # 1 step:
    for i in range(N):
        if nxt[i] < N:
            jump[0][i] = nxt[i] + 1
        else:
            jump[0][i] = N
    jump[0][N] = N  # sentinel stays N

    for k in range(1, LOG):
        jk = jump[k]
        jkm1 = jump[k - 1]
        for i in range(N + 1):
            jk[i] = jkm1[jkm1[i]]

    out_lines = []
    for L, R in queries:
        cur = L
        ans = 0
        # greedy with binary lifting: try largest steps first
        for k in range(LOG - 1, -1, -1):
            nxt_pos = jump[k][cur]
            if nxt_pos <= R:
                ans += 1 << k
                cur = nxt_pos
        out_lines.append(str(ans))

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()