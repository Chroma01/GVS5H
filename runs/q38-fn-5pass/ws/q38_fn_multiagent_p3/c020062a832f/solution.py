import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]

    # Fenwick tree for the initial inversion count of A.
    bit = [0] * (M + 1)

    # For each value v, store:
    #   cnt[v]     = number of positions i with A_i = v
    #   sum_pos[v] = sum of those 1-indexed positions
    cnt = [0] * M
    sum_pos = [0] * M

    inv = 0

    for i in range(N):
        a = data[2 + i]

        # Count previous elements <= a.
        idx = a + 1
        leq = 0
        while idx:
            leq += bit[idx]
            idx -= idx & -idx

        # Previous elements > a form inversions with current element.
        inv += i - leq

        # Add current value to Fenwick tree.
        idx = a + 1
        while idx <= M:
            bit[idx] += 1
            idx += idx & -idx

        cnt[a] += 1
        sum_pos[a] += i + 1

    del data, bit

    # delta[v] = change in inversion count when all elements with original
    # value v wrap from M-1 to 0.
    delta = [0] * M

    for v in range(M):
        c = cnt[v]
        if c:
            # If positions are p_1 < ... < p_c, then
            # non-wrapping-before-wrapping pairs = sum(p_t - t)
            # = sum_pos[v] - c(c+1)/2.
            s = sum_pos[v] - (c * (c + 1) // 2)

            # Cross pairs between wrapping and non-wrapping elements.
            total_cross = c * (N - c)

            # Each non-wrapping-before-wrapping pair gains +1,
            # each wrapping-before-non-wrapping pair loses -1.
            delta[v] = 2 * s - total_cross

    del cnt, sum_pos

    ans = inv
    out = []

    # For k -> k+1, the wrapping original value is (M-1-k) mod M.
    # Thus print k=0 first, then apply delta[M-1], delta[M-2], ...
    for v in range(M - 1, -1, -1):
        out.append(str(ans))
        ans += delta[v]

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()