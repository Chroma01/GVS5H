import sys


def normalize(s: bytes, N: int, X: int, Y: int):
    """
    Try to construct the A-normal form of s.

    The construction is greedy over the ordered residue sequences:
      - positions of '1' modulo X
      - positions of '0' modulo Y
    It also verifies that the produced string has no 0^X 1^Y.
    If anything fails, returns None.
    """
    ones = []
    zeros = []

    # Build ordered residue sequences (0-indexed positions).
    if X == 1:
        for idx, c in enumerate(s):
            if c == 49:  # '1'
                ones.append(0)
            else:
                zeros.append(idx % Y)
    elif Y == 1:
        for idx, c in enumerate(s):
            if c == 49:
                ones.append(idx % X)
            else:
                zeros.append(0)
    else:
        for idx, c in enumerate(s):
            if c == 49:
                ones.append(idx % X)
            else:
                zeros.append(idx % Y)

    K = len(ones)
    Z = len(zeros)

    # Latest possible position (deadline) for each occurrence in its own sequence.
    if X == 1:
        dl1 = list(range(N - K, N))
    else:
        dl1 = [0] * K
        limit = N
        for idx in range(K - 1, -1, -1):
            r = ones[idx]
            q = limit - 1
            q -= (q - r) % X
            if q < 0:
                return None
            dl1[idx] = q
            limit = q

    if Y == 1:
        dl0 = list(range(N - Z, N))
    else:
        dl0 = [0] * Z
        limit = N
        for idx in range(Z - 1, -1, -1):
            r = zeros[idx]
            q = limit - 1
            q -= (q - r) % Y
            if q < 0:
                return None
            dl0[idx] = q
            limit = q

    out = bytearray(N)
    i = j = 0
    X1 = (X == 1)
    Y1 = (Y == 1)

    for p in range(N):
        if i < K and p > dl1[i]:
            return None
        if j < Z and p > dl0[j]:
            return None

        if X1:
            can1 = i < K
        else:
            can1 = i < K and (p % X == ones[i])

        if Y1:
            can0 = j < Z
        else:
            can0 = j < Z and (p % Y == zeros[j])

        if not can1 and not can0:
            return None

        if can1 and can0:
            if X1:
                n1 = p + 1
            else:
                q = p + 1
                n1 = q + ((ones[i] - q) % X)

            if Y1:
                n0 = p + 1
            else:
                q = p + 1
                n0 = q + ((zeros[j] - q) % Y)

            # If one cannot wait, it is forced.
            # Otherwise, if zero cannot wait, zero is forced.
            # If both can wait, prefer '1' for the lexicographically maximum normal form.
            if n1 > dl1[i]:
                choose1 = True
            elif n0 > dl0[j]:
                choose1 = False
            else:
                choose1 = True

        elif can1:
            # Zero is not placeable now; it must still be able to meet its deadline.
            if j < Z:
                if Y1:
                    n0 = p + 1
                else:
                    q = p + 1
                    n0 = q + ((zeros[j] - q) % Y)
                if n0 > dl0[j]:
                    return None
            choose1 = True

        else:
            # One is not placeable now; it must still be able to meet its deadline.
            if i < K:
                if X1:
                    n1 = p + 1
                else:
                    q = p + 1
                    n1 = q + ((ones[i] - q) % X)
                if n1 > dl1[i]:
                    return None
            choose1 = False

        if choose1:
            out[p] = 49
            i += 1
        else:
            out[p] = 48
            j += 1

    if i != K or j != Z:
        return None

    # Verify that the produced string is A-normal: no 0^X followed by 1^Y.
    prev_c = -1
    prev_len = 0
    cur_c = out[0]
    cur_len = 1

    for idx in range(1, N):
        c = out[idx]
        if c == cur_c:
            cur_len += 1
        else:
            if prev_c == 48 and cur_c == 49 and prev_len >= X and cur_len >= Y:
                return None
            prev_c, prev_len = cur_c, cur_len
            cur_c, cur_len = c, 1

    if prev_c == 48 and cur_c == 49 and prev_len >= X and cur_len >= Y:
        return None

    return out


def residue_equal(s: bytes, t: bytes, mod: int, ch: int) -> bool:
    """Compare ordered residues modulo mod of all occurrences of ch."""
    n = len(s)

    if mod == 1:
        sub = b'1' if ch == 49 else b'0'
        return s.count(sub) == t.count(sub)

    i = j = 0
    while True:
        while i < n and s[i] != ch:
            i += 1
        while j < n and t[j] != ch:
            j += 1

        if i == n or j == n:
            return i == n and j == n

        if i % mod != j % mod:
            return False

        i += 1
        j += 1


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3]
    T = data[4]

    # No operation window exists.
    if X + Y > N:
        print("Yes" if S == T else "No")
        return

    if S == T:
        print("Yes")
        return

    ns = normalize(S, N, X, Y)
    nt = normalize(T, N, X, Y)

    # If both verified normal forms were produced, compare them.
    if ns is not None and nt is not None and ns == nt:
        print("Yes")
        return

    # Defensive fallback: the invariant comparison is linear and proven.
    if residue_equal(S, T, X, 49) and residue_equal(S, T, Y, 48):
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    solve()