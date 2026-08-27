import sys
sys.setrecursionlimit(1 << 25)


def normalize(s, X, Y):
    """
    Return the terminal word obtained by repeatedly applying
        0^X 1^Y -> 1^Y 0^X
    (move ones left).  The rewrite system is terminating and, for this
    non-overlapping left-hand side, the leftmost-greedy reduction gives the
    component representative used below.
    """
    L = X + Y
    if L > len(s):
        return s
    lhs = '0' * X + '1' * Y
    rhs = '1' * Y + '0' * X
    a = list(s)
    i = 0
    # Leftmost scan.  After a rewrite at i, only a rewrite ending at/after
    # i-X can newly appear, so backing up X positions is sufficient.
    while i <= len(a) - L:
        if a[i:i+L] == lhs:
            a[i:i+L] = rhs
            i = max(0, i - X)
        else:
            i += 1
    return ''.join(a)


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0]); X = int(data[1]); Y = int(data[2])
    S = data[3].strip()
    T = data[4].strip()
    if normalize(S, X, Y) == normalize(T, X, Y):
        sys.stdout.write('Yes\n')
    else:
        sys.stdout.write('No\n')


if __name__ == '__main__':
    main()