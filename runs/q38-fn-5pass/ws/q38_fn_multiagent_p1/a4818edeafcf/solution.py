import sys


def solve():
    input = sys.stdin.buffer.readline

    line = input()
    if not line:
        return
    N = int(line)

    A = [0]
    while len(A) <= N:
        line = input()
        if not line:
            break
        A.extend(map(int, line.split()))
    if len(A) > N + 1:
        A = A[:N + 1]

    # prev[i] = previous occurrence of A[i], or 0 if first occurrence.
    prev = [0] * (N + 1)
    last = [0] * (N + 1)
    for i in range(1, N + 1):
        a = A[i]
        prev[i] = last[a]
        last[a] = i

    # suff[i] = number of distinct values in A[i..N].
    # Reuse `last` as a timestamp array for suffix distinct counting.
    suff = [0] * (N + 2)
    token = N + 1
    cnt = 0
    for i in range(N, 0, -1):
        a = A[i]
        if last[a] != token:
            last[a] = token
            cnt += 1
        suff[i] = cnt

    # Lazy segment tree over left split positions i (0-indexed: i-1).
    # Inactive leaves are -INF. Leaves are activated as j grows.
    size = 1 << (N - 1).bit_length()
    log = (N - 1).bit_length()
    NEG = -10**18

    maxv = [NEG] * (2 * size)
    lazy = [0] * (2 * size)
    levels = range(log)

    # Current prefix distinct count for A[1..j-1].
    # Reuse `last` with a new timestamp for left-side distinct counting.
    token = N + 2
    cnt_left = 0
    a = A[1]
    if last[a] != token:
        last[a] = token
        cnt_left += 1

    ans = 0

    # j is the end of the middle subarray, 2 <= j <= N-1.
    for j in range(2, N):
        # Activate left split i = j-1, represented by position j-2.
        leaf = size + j - 2
        maxv[leaf] = cnt_left
        lazy[leaf] = 0

        # Add A[j] to the middle subarray.
        # It increases distinct count for i >= prev[j] (or all active i if prev[j]=0).
        p = prev[j]
        l = p if p else 1

        left = size + l - 1
        right = size + j - 1  # exclusive
        l0 = left
        r0 = right

        while left < right:
            if left & 1:
                maxv[left] += 1
                lazy[left] += 1
                left += 1
            if right & 1:
                right -= 1
                maxv[right] += 1
                lazy[right] += 1
            left >>= 1
            right >>= 1

        # Rebuild ancestors of the two original endpoints.
        # Invariant: maxv[node] = lazy[node] + max(maxv[left_child], maxv[right_child]).
        k1 = l0 >> 1
        k2 = (r0 - 1) >> 1
        for _ in levels:
            if k1:
                c = k1 << 1
                lv = maxv[c]
                rv = maxv[c | 1]
                maxv[k1] = lazy[k1] + (lv if lv >= rv else rv)
            if k2 and k2 != k1:
                c = k2 << 1
                lv = maxv[c]
                rv = maxv[c | 1]
                maxv[k2] = lazy[k2] + (lv if lv >= rv else rv)
            k1 >>= 1
            k2 >>= 1

        # Root maximum is max over all active left splits.
        total = maxv[1] + suff[j + 1]
        if total > ans:
            ans = total

        # Prepare prefix distinct count for the next j.
        a = A[j]
        if last[a] != token:
            last[a] = token
            cnt_left += 1

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()