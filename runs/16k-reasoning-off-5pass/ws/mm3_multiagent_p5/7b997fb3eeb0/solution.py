import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    A = [0] * (N + 2)
    for i in range(1, N + 1):
        A[i] = int(data[idx]); idx += 1

    # For each position i, compute nxt[i] = smallest j > i with A[j] >= 2*A[i],
    # or N+1 if none. This is the earliest valid "large" partner for mochi i.
    nxt = [N + 1] * (N + 2)
    j = 1
    for i in range(1, N + 1):
        if j < i + 1:
            j = i + 1
        while j <= N and A[j] < 2 * A[i]:
            j += 1
        nxt[i] = j if j <= N else N + 1

    # For each query [L, R], greedily pair using two pointers.
    # The greedy "smallest unpaired with smallest available large >= 2*small" is
    # optimal on a sorted array. We maintain 'cand' (next candidate large) and
    # 'last' (most recently used large index + 1) to ensure each mochi is used
    # at most once. The two-pointer advances i and cand monotonically, so the
    # total work per query is O(R-L+1) with a very small constant.
    Q = int(data[idx]); idx += 1
    out = []
    for _ in range(Q):
        L = int(data[idx]); idx += 1
        R = int(data[idx]); idx += 1
        i = L
        cand = L
        last = L  # one past the most recently used large mochi
        ans = 0
        while i <= R:
            # Candidate large for mochi i: must be > last used large and
            # at a position where A[pos] >= 2*A[i]. nxt[i] gives the first
            # such position; we also need it to be > last.
            c = nxt[i]
            if c < last:
                c = last
            if c > R:
                break
            ans += 1
            i += 1
            last = c + 1
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()