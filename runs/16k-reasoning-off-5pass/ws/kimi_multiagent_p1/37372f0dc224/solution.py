import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    S = data[0]
    n = len(S)
    R = S[::-1]
    T = R + '#' + S
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
    # k = length of longest palindromic suffix of S
    sys.stdout.write(S + S[:n - k][::-1] + '\n')

solve()