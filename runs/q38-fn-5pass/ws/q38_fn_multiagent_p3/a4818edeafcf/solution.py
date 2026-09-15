import sys


def solve():
    first = sys.stdin.buffer.readline().split()
    if not first:
        return
    N = int(first[0])
    A = list(map(int, first[1:]))
    while len(A) < N:
        A.extend(map(int, sys.stdin.buffer.readline().split()))
    if len(A) > N:
        A = A[:N]

    # Possible left cuts are 0 .. N-3 (0-indexed prefix end).
    M = N - 2

    # prev[j] = max(previous occurrence of A[j], 0), only needed for j <= N-2.
    # Lval[i] = distinct(A[0..i]) + 1, used when activating left cut i.
    prev = [0] * (N - 1)
    Lval = [0] * M

    last = [-1] * (N + 1)
    cnt = 0
    for idx, a in enumerate(A):
        p = last[a]
        if idx < N - 1:
            prev[idx] = p if p >= 0 else 0
        if p == -1:
            cnt += 1
        if idx < M:
            Lval[idx] = cnt + 1
        last[a] = idx

    # R[i] = distinct(A[i..N-1]).
    R = [0] * (N + 1)
    last = [-1] * (N + 1)
    cnt = 0
    for idx in range(N - 1, -1, -1):
        a = A[idx]
        if last[a] == -1:
            last[a] = idx
            cnt += 1
        R[idx] = cnt

    del A, last

    # Lazy segment tree: range add +1, global maximum.
    # Inactive leaves are NEG; each iteration activates one new left cut.
    NEG = -10**9
    size = 1 << (M - 1).bit_length()
    log = size.bit_length() - 1
    d = [NEG] * (2 * size)
    lz = [0] * size
    half = size >> 1

    if log:
        down = list(range(log, 0, -1))
        up = list(range(1, log + 1))
        masks = [0] * (log + 1)
        for s in range(1, log + 1):
            masks[s] = (1 << s) - 1
    else:
        down = []
        up = []
        masks = [0]

    def add_range(l, r, d=d, lz=lz, size=size, half=half,
                  down=down, up=up, masks=masks):
        """Add 1 to [l, r)."""
        if l >= r:
            return

        l += size
        r += size
        l0 = l
        r0 = r

        # Push lazy values on boundary paths.
        for s in down:
            mask = masks[s]

            if l0 & mask:
                k = l0 >> s
                z = lz[k]
                if z:
                    c = k << 1
                    c1 = c + 1
                    d[c] += z
                    d[c1] += z
                    if k < half:
                        lz[c] += z
                        lz[c1] += z
                    lz[k] = 0

            if r0 & mask:
                k = (r0 - 1) >> s
                z = lz[k]
                if z:
                    c = k << 1
                    c1 = c + 1
                    d[c] += z
                    d[c1] += z
                    if k < half:
                        lz[c] += z
                        lz[c1] += z
                    lz[k] = 0

        # Apply to covered nodes.
        while l < r:
            if l & 1:
                d[l] += 1
                if l < size:
                    lz[l] += 1
                l += 1
            if r & 1:
                r -= 1
                d[r] += 1
                if r < size:
                    lz[r] += 1
            l >>= 1
            r >>= 1

        # Recompute boundary ancestors.
        for s in up:
            mask = masks[s]

            if l0 & mask:
                k = l0 >> s
                c = k << 1
                c1 = c + 1
                x = d[c]
                y = d[c1]
                d[k] = (x if x >= y else y) + lz[k]

            if r0 & mask:
                k = (r0 - 1) >> s
                c = k << 1
                c1 = c + 1
                x = d[c]
                y = d[c1]
                d[k] = (x if x >= y else y) + lz[k]

    ans = 0

    d_local = d
    lz_local = lz
    sz = size
    prev_local = prev
    L_local = Lval
    R_local = R
    add = add_range

    # Right cut end J (0-indexed) ranges from 1 to N-2.
    for j in range(1, N - 1):
        idx = j - 1  # new left cut I = J-1

        # Activate left cut idx. Its middle is just A[j], so value is L[idx] + 1.
        pos = sz + idx
        d_local[pos] = L_local[idx]

        # Update ancestors. Since no previous update covered this new leaf,
        # no lazy tag exists on its path; direct assignment is safe.
        pos >>= 1
        while pos:
            c = pos << 1
            c1 = c + 1
            x = d_local[c]
            y = d_local[c1]
            new = (x if x >= y else y) + lz_local[pos]
            if new == d_local[pos]:
                break
            d_local[pos] = new
            pos >>= 1

        # For old left cuts I < idx, A[j] increases middle distinct count
        # exactly when previous occurrence p <= I.
        p = prev_local[j]
        if p < idx:
            add(p, idx)

        v = d_local[1] + R_local[j + 1]
        if v > ans:
            ans = v

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()