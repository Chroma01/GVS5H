import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, A, B = data[:4]
    intervals = []
    idx = 4
    for _ in range(M):
        L = data[idx]
        R = data[idx + 1]
        idx += 2
        intervals.append((L, R))

    # If A == B, the path is forced to one residue class modulo A.
    if A == B:
        if (N - 1) % A != 0:
            print("No")
            return

        total = (N - 1) // A
        for L, R in intervals:
            # Required squares are 1 + k*A.
            k_min = (L - 1 + A - 1) // A  # ceil((L-1)/A)
            k_max = (R - 1) // A          # floor((R-1)/A)
            if k_min <= k_max and k_min <= total and k_max >= 0:
                print("No")
                return

        print("Yes")
        return

    # For A < B, jumps A..B generate all sufficiently large distances.
    # Compute T such that every distance >= T is representable.
    T = 500  # safe fallback for given constraints
    reach = [True]  # reach[d] = d is representable
    consec = 0
    d = 0
    while consec < A:
        d += 1
        val = False
        for s in range(A, B + 1):
            if s <= d and reach[d - s]:
                val = True
                break
        reach.append(val)

        if val:
            consec += 1
            if consec == A:
                T = d - A + 1
                break
        else:
            consec = 0

    # If a good run has this length and any reachable bit is present,
    # its last B squares are certainly all reachable.
    K = T + 2 * B + 1

    all_ones = (1 << B) - 1
    # Bits corresponding to offsets A..B from the current position.
    check_mask = (((1 << (B - A + 1)) - 1) << (A - 1)) & all_ones

    def advance_good(mask, length):
        if length <= 0 or mask == 0:
            return mask
        if length >= K:
            return all_ones

        m = mask
        ao = all_ones
        cm = check_mask
        for _ in range(length):
            if m == 0 or m == ao:
                break
            m = ((m << 1) & ao) | (1 if (m & cm) else 0)
        return m

    def advance_bad(mask, length):
        if length <= 0 or mask == 0:
            return mask
        if length >= B:
            return 0
        return (mask << length) & all_ones

    # Mask bit 0 is the previous square.  Start at square 1, next is 2.
    mask = 1
    cur = 2

    for L, R in intervals:
        if cur < L:
            mask = advance_good(mask, L - cur)
        mask = advance_bad(mask, R - L + 1)
        cur = R + 1

    if cur <= N:
        mask = advance_good(mask, N - cur + 1)

    print("Yes" if (mask & 1) else "No")


if __name__ == "__main__":
    solve()