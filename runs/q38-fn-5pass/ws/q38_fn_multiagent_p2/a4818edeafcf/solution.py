import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data  # A[1..N] are the sequence values

    # Segment tree over the difference array of candidate values.
    size = 1
    while size < N:
        size <<= 1
    base = size
    NEG = -10**18

    sumv = [0] * (2 * size)
    pref = [NEG] * (2 * size)

    # Initial candidate value for left split i is prefix distinct count L[i].
    # Store D[i] = L[i] - L[i-1] in the segment tree.
    seen = [0] * (N + 1)
    cnt = 0
    prev = 0
    for i in range(1, N + 1):
        x = A[i]
        if seen[x] == 0:
            seen[x] = 1
            cnt += 1
        val = cnt - prev
        prev = cnt
        idx = base + i - 1
        sumv[idx] = val
        pref[idx] = val

    # Build segment tree: each node stores (sum, max non-empty prefix sum).
    for idx in range(base - 1, 0, -1):
        left = idx << 1
        right = left | 1
        s = sumv[left] + sumv[right]
        p = pref[left]
        alt = sumv[left] + pref[right]
        if alt > p:
            p = alt
        sumv[idx] = s
        pref[idx] = p

    # Suffix distinct counts R[i] = distinct in A[i..N].
    seen = [0] * (N + 1)
    R = [0] * (N + 2)
    cnt = 0
    for i in range(N, 0, -1):
        x = A[i]
        if seen[x] == 0:
            seen[x] = 1
            cnt += 1
        R[i] = cnt

    def add_pair(a: int, b: int, sv=sumv, pr=pref, base=base) -> None:
        """
        Apply D[a] += 1 and D[b] -= 1, then recompute unique ancestors.
        Here a < b always in this problem.
        """
        ia = base + a
        ib = base + b

        v = sv[ia] + 1
        sv[ia] = v
        pr[ia] = v

        v = sv[ib] - 1
        sv[ib] = v
        pr[ib] = v

        ia >>= 1
        ib >>= 1

        while ia:
            if ia == ib:
                left = ia << 1
                right = left | 1
                s = sv[left] + sv[right]
                p = pr[left]
                alt = sv[left] + pr[right]
                if alt > p:
                    p = alt
                sv[ia] = s
                pr[ia] = p
                ia >>= 1
                ib >>= 1
            else:
                left = ia << 1
                right = left | 1
                s = sv[left] + sv[right]
                p = pr[left]
                alt = sv[left] + pr[right]
                if alt > p:
                    p = alt
                sv[ia] = s
                pr[ia] = p

                left = ib << 1
                right = left | 1
                s = sv[left] + sv[right]
                p = pr[left]
                alt = sv[left] + pr[right]
                if alt > p:
                    p = alt
                sv[ib] = s
                pr[ib] = p

                ia >>= 1
                ib >>= 1

    def query_prefix(
        count: int,
        sv=sumv,
        pr=pref,
        base=base,
        size=size,
        NEG=NEG,
    ) -> int:
        """
        Return max prefix sum among first `count` elements (1 <= count <= N).
        This is max V[1..count].
        """
        idx = 1
        l = 0
        r = size
        acc_sum = 0
        acc_max = NEG

        while idx < size:
            if count >= r:
                alt = acc_sum + pr[idx]
                if alt > acc_max:
                    acc_max = alt
                return acc_max

            mid = (l + r) >> 1
            if count <= mid:
                idx <<= 1
                r = mid
            else:
                left = idx << 1
                alt = acc_sum + pr[left]
                if alt > acc_max:
                    acc_max = alt
                acc_sum += sv[left]
                idx = left | 1
                l = mid

        if count > l:
            alt = acc_sum + pr[idx]
            if alt > acc_max:
                acc_max = alt

        return acc_max

    last = [0] * (N + 1)
    last[A[1]] = 1

    ans = 0
    add = add_pair
    query = query_prefix

    # Right split j ranges from 2 to N-1.
    for j in range(2, N):
        x = A[j]
        p = last[x]

        # Add A[j] to the middle segment.
        # It increases distinct count for left splits i in [p, j-1],
        # or [1, j-1] if p == 0.
        if p == 0:
            a = 0
        else:
            a = p - 1
        b = j - 1

        add(a, b)
        last[x] = j

        best_middle_plus_left = query(j - 1)
        total = best_middle_plus_left + R[j + 1]
        if total > ans:
            ans = total

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()