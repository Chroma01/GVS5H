import sys
from collections import deque


def invariant_possible(S, T, N, X, Y):
    if S == T:
        return True

    ones_count = S.count('1')
    if ones_count != T.count('1'):
        return False

    zeros_count = N - ones_count

    # If no operation can ever be applied, reachability is just equality.
    if X + Y > N or ones_count < Y or zeros_count < X:
        return False

    # Invariant 1: ordered positions of 1s modulo X.
    ones_s = [i % X for i, ch in enumerate(S) if ch == '1']
    ones_t = [i % X for i, ch in enumerate(T) if ch == '1']
    if ones_s != ones_t:
        return False

    # Free memory before building the second pair of lists.
    del ones_s, ones_t

    # Invariant 2: ordered positions of 0s modulo Y.
    zeros_s = [i % Y for i, ch in enumerate(S) if ch == '0']
    zeros_t = [i % Y for i, ch in enumerate(T) if ch == '0']
    return zeros_s == zeros_t


def bfs_reachable(S, T, N, X, Y):
    """Exact brute force for tiny N, used as a cross-check."""
    if S == T:
        return True
    if X + Y > N:
        return False
    if S.count('1') != T.count('1'):
        return False

    L = X + Y
    pat_a = '0' * X + '1' * Y
    res_a = '1' * Y + '0' * X
    pat_b = '1' * Y + '0' * X
    res_b = '0' * X + '1' * Y

    q = deque([S])
    seen = {S}

    while q:
        s = q.popleft()
        for i in range(N - L + 1):
            if s[i:i + L] == pat_a:
                ns = s[:i] + res_a + s[i + L:]
                if ns == T:
                    return True
                if ns not in seen:
                    seen.add(ns)
                    q.append(ns)

            if s[i:i + L] == pat_b:
                ns = s[:i] + res_b + s[i + L:]
                if ns == T:
                    return True
                if ns not in seen:
                    seen.add(ns)
                    q.append(ns)

    return False


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3]
    T = data[4]

    # Tiny exact validation.  If the invariant-based answer disagrees with BFS,
    # report the counterexample instead of finalizing.
    if N <= 10:
        exact = bfs_reachable(S, T, N, X, Y)
        inv = invariant_possible(S, T, N, X, Y)
        if exact != inv:
            print("Counterexample")
            return
        print("Yes" if exact else "No")
        return

    print("Yes" if invariant_possible(S, T, N, X, Y) else "No")


if __name__ == "__main__":
    solve()