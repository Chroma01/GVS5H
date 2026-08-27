import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    S = data[0]
    n = len(S)
    T = S + '#' + S[::-1]
    m = len(T)
    pi = [0] * m
    k = 0
    for i in range(1, m):
        c = T[i]
        while k > 0 and T[k] != c:
            k = pi[k - 1]
        if T[k] == c:
            k += 1
        pi[i] = k
    k = pi[-1]
    sys.stdout.write(S + S[k:][::-1])

solve()