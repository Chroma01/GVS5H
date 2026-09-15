import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    S = data[0]
    n = len(S)

    # Longest palindromic suffix length L:
    # T = reverse(S) + '#' + S; then pi[-1] == L.
    rev = S[::-1]
    T = rev + b'#' + S
    m = len(T)

    pi = [0] * m
    j = 0
    for i in range(1, m):
        c = T[i]
        while j > 0 and c != T[j]:
            j = pi[j - 1]
        if c == T[j]:
            j += 1
        pi[i] = j

    L = pi[-1]
    k = n - L
    ans = S + S[:k][::-1]
    sys.stdout.buffer.write(ans + b'\n')

if __name__ == '__main__':
    main()