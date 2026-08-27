import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = list(map(int, input().split()))

    # Fenwick tree for initial inversion count (k=0)
    # Values are in [0, M-1], we use 1-indexed BIT of size M
    bit = [0] * (M + 2)  # extra space for safety
    def update(i):
        while i <= M:
            bit[i] += 1
            i += i & -i
    def query(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    inv0 = 0
    for i, x in enumerate(A):
        idx = x + 1
        # number of previous elements > x is i - query(idx)
        inv0 += i - query(idx)
        update(idx)

    # count and sum of positions (1-indexed) for each value
    cnt = [0] * M
    sum_pos = [0] * M
    for i, v in enumerate(A):
        cnt[v] += 1
        sum_pos[v] += (i + 1)  # 1-indexed position

    # compute A_v and B_v for each value v
    A_arr = [0] * M
    B_arr = [0] * M
    for v in range(M):
        c = cnt[v]
        s = sum_pos[v]
        # A_v = # pairs (i<j) with i having value v, j not having value v
        A_arr[v] = c * N - s - c * (c - 1) // 2
        # B_v = # pairs (i<j) with i not having value v, j having value v
        B_arr[v] = s - c * (c + 1) // 2

    ans = [0] * M
    ans[0] = inv0
    cur = inv0
    for k in range(M - 1):
        v = (M - 1 - k) % M
        cur += B_arr[v] - A_arr[v]
        ans[k + 1] = cur

    sys.stdout.write('\n'.join(map(str, ans)))

if __name__ == "__main__":
    solve()