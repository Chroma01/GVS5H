import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # count of each value and sum of 1‑based positions of that value
    cnt = [0] * M
    sumPos = [0] * M
    for idx, val in enumerate(A):
        cnt[val] += 1
        sumPos[val] += idx + 1          # positions are 1‑based

    # ---------- Fenwick tree for the initial inversion number ----------
    size = M
    bit = [0] * (size + 2)              # 1‑based

    def bit_add(i: int, x: int) -> None:
        while i <= size:
            bit[i] += x
            i += i & -i

    def bit_sum(i: int) -> int:
        s = 0
        while i:
            s += bit[i]
            i -= i & -i
        return s

    inv0 = 0
    for idx, val in enumerate(A):
        v = val + 1                      # shift because BIT is 1‑based
        # previous elements greater than val = idx - (# previous ≤ val)
        inv0 += idx - bit_sum(v)
        bit_add(v, 1)

    # ---------- transition from k‑1 to k ----------
    ans = [0] * M
    ans[0] = inv0
    N1 = N + 1
    for k in range(1, M):
        v = (M - k) % M                  # values that wrap from M‑1 to 0 now
        c = cnt[v]
        sp = sumPos[v]
        delta = 2 * sp - c * N1          # change of inversion count
        ans[k] = ans[k - 1] + delta

    sys.stdout.write('\n'.join(str(x) for x in ans))

if __name__ == "__main__":
    solve()