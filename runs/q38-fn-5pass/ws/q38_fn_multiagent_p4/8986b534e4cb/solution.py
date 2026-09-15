import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)

    N = int(next(it))
    M = int(next(it))
    Q = int(next(it))

    Ls = [0] * M
    Rs = [0] * M
    Ds = [0] * M

    for i in range(M):
        s = int(next(it))
        t = int(next(it))
        if s < t:
            # S < T: interiors must be strictly larger than endpoints.
            Ls[i] = s - 1
            Rs[i] = t - 1
            Ds[i] = 0
        else:
            # S > T: interiors must be strictly smaller than endpoints.
            Ls[i] = t - 1
            Rs[i] = s - 1
            Ds[i] = 1

    size = 1
    while size < N:
        size <<= 1

    # Segment trees over left endpoints, storing the maximum right endpoint
    # among active intervals of that direction.
    tree0 = [-1] * (2 * size)  # direction 0: S < T
    tree1 = [-1] * (2 * size)  # direction 1: S > T

    # Endpoint occupancy for opposite-direction conflicts.
    left0 = [0] * N
    right0 = [0] * N
    left1 = [0] * N
    right1 = [0] * N

    def update(tree, pos, val, size=size):
        i = pos + size
        tree[i] = val
        i >>= 1
        while i:
            li = i << 1
            a = tree[li]
            b = tree[li | 1]
            tree[i] = a if a >= b else b
            i >>= 1

    def find_last_leq(tree, q, x, size=size, N=N):
        """
        Return the largest index p <= q with tree[p] > x, or -1.
        The tree is an iterative max segment tree.
        """
        pos = q + size
        if tree[pos] > x:
            return q

        # Decompose prefix [0, q] from right to left using left siblings
        # of ancestors where the path goes to a right child.
        while pos > 1:
            if pos & 1:
                node = pos - 1
                if tree[node] > x:
                    while node < size:
                        right = (node << 1) | 1
                        if tree[right] > x:
                            node = right
                        else:
                            node <<= 1
                    idx = node - size
                    return idx if idx < N else -1
            pos >>= 1

        return -1

    def range_max_ge(tree, l, r, x, size=size):
        """Return True iff max(tree[l:r]) >= x."""
        if l >= r:
            return False
        l += size
        r += size
        while l < r:
            if l & 1:
                if tree[l] >= x:
                    return True
                l += 1
            if r & 1:
                r -= 1
                if tree[r] >= x:
                    return True
            l >>= 1
            r >>= 1
        return False

    def can_add(i):
        l = Ls[i]
        r = Rs[i]
        d = Ds[i]

        # Opposite direction: conflict iff same left endpoint or same right endpoint.
        if d == 0:
            if left1[l] or right1[r]:
                return False
            tree = tree0
        else:
            if left0[l] or right0[r]:
                return False
            tree = tree1

        # Same direction, existing interval covering the new left endpoint.
        # If it starts at l, conflict. If it contains l and does not strictly
        # contain the new interval, conflict.
        a = find_last_leq(tree, l, l)
        if a != -1:
            b = tree[a + size]
            if a == l or r >= b:
                return False

        # Same direction, existing interval starting strictly inside the new one
        # and reaching at least the new right endpoint: partial overlap or
        # shared right endpoint.
        if range_max_ge(tree, l + 1, r, r):
            return False

        return True

    def add(i):
        l = Ls[i]
        r = Rs[i]
        d = Ds[i]
        if d == 0:
            left0[l] += 1
            right0[r] += 1
            update(tree0, l, r)
        else:
            left1[l] += 1
            right1[r] += 1
            update(tree1, l, r)

    def remove(i):
        l = Ls[i]
        r = Rs[i]
        d = Ds[i]
        if d == 0:
            left0[l] -= 1
            right0[r] -= 1
            update(tree0, l, -1)
        else:
            left1[l] -= 1
            right1[r] -= 1
            update(tree1, l, -1)

    first_bad = [M] * M
    R = 0

    can = can_add
    ad = add
    rem = remove

    for L in range(M):
        if R < L:
            R = L

        while R < M and can(R):
            ad(R)
            R += 1

        first_bad[L] = R

        if R > L:
            rem(L)
        else:
            # A single interval is always feasible, so this should not be needed.
            R = L + 1

    out = []
    append = out.append

    for _ in range(Q):
        lq = int(next(it)) - 1
        rq = int(next(it)) - 1
        if rq < first_bad[lq]:
            append("Yes")
        else:
            append("No")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()