import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    S = data[0].decode()
    n = len(S)
    R = S[::-1]
    # Longest palindromic suffix of S:
    # KMP prefix function on T = R + '#' + S; pi[-1] is the longest prefix of R
    # that is also a suffix of S, i.e., the longest palindromic suffix of S.
    T = R + '#' + S
    m = len(T)
    pi = [0] * m
    k = 0
    for i in range(1, m):
        Ti = T[i]
        while k > 0 and T[k] != Ti:
            k = pi[k - 1]
        if T[k] == Ti:
            k += 1
        pi[i] = k
    M = pi[-1]  # length of longest palindromic suffix of S
    # Answer: S + reverse(S[:n-M]) = S + R[M:]
    sys.stdout.write(S + R[M:] + '\n')

main()