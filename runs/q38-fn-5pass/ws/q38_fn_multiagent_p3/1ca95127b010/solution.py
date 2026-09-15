import sys


def same_residues(s, t, ch, mod):
    """
    Compare the left-to-right sequences of positions (0-indexed) of character
    ch in s and t, modulo mod.
    """
    n = len(s)
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


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3]
    T = data[4]

    # If the block length is larger than the string, no operation is possible.
    if X + Y > N:
        sys.stdout.write("Yes\n" if S == T else "No\n")
        return

    # Ones move by X positions, zeros move by Y positions.
    # Their left-to-right order is preserved.
    if not same_residues(S, T, 49, X):  # ord('1') == 49
        sys.stdout.write("No\n")
        return

    if not same_residues(S, T, 48, Y):  # ord('0') == 48
        sys.stdout.write("No\n")
        return

    sys.stdout.write("Yes\n")


def _oracle():
    """
    Small BFS oracle for development/verification only.
    It is intentionally not called by solve().
    """
    from collections import deque
    import random

    def next_states(s, x, y):
        n = len(s)
        res = []
        for i in range(n - x - y + 1):
            if s[i:i + x] == '0' * x and s[i + x:i + x + y] == '1' * y:
                res.append(s[:i] + '1' * y + '0' * x + s[i + x + y:])
            if s[i:i + y] == '1' * y and s[i + y:i + y + x] == '0' * x:
                res.append(s[:i] + '0' * x + '1' * y + s[i + y + x:])
        return res

    def invariant(s, t, x, y):
        if x + y > len(s):
            return s == t

        def seq(u, c, m):
            return [i % m for i, ch in enumerate(u) if ch == c]

        return (
            seq(s, '1', x) == seq(t, '1', x)
            and seq(s, '0', y) == seq(t, '0', y)
        )

    random.seed(12345)
    for _ in range(200):
        n = random.randint(1, 6)
        x = random.randint(1, n)
        y = random.randint(1, n)
        s = ''.join(random.choice('01') for _ in range(n))

        seen = {s}
        q = deque([s])
        while q:
            cur = q.popleft()
            for nxt in next_states(cur, x, y):
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)

        for t in seen:
            if not invariant(s, t, x, y):
                print('counterexample', n, x, y, s, t)
                return

        for mask in range(1 << n):
            t = ''.join('1' if (mask >> i) & 1 else '0' for i in range(n))
            if invariant(s, t, x, y) and t not in seen:
                print('counterexample', n, x, y, s, t)
                return

    print('oracle ok')


if __name__ == "__main__":
    solve()