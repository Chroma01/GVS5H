import sys

def main():
    data = sys.stdin.buffer.readline().strip()
    if not data:
        data = sys.stdin.buffer.read().strip()
    S = data
    n = len(S)

    revS = S[::-1]
    T = revS + b'#' + S

    m = len(T)
    pi = [0] * m
    j = 0

    for i in range(1, m):
        c = T[i]
        while j and c != T[j]:
            j = pi[j - 1]
        if c == T[j]:
            j += 1
        pi[i] = j

    L = pi[-1]
    k = n - L
    ans = S + revS[n - k:]
    sys.stdout.buffer.write(ans + b'\n')

if __name__ == "__main__":
    main()