import sys

def main():
    S = sys.stdin.buffer.read().strip()
    if not S:
        return

    n = len(S)
    R = S[::-1]

    # T = reverse(S) + separator + S
    T = R + b'#' + S
    m = len(T)

    # KMP prefix function on T
    pi = [0] * m
    j = 0
    for i in range(1, m):
        c = T[i]
        while j and T[j] != c:
            j = pi[j - 1]
        if T[j] == c:
            j += 1
        pi[i] = j

    k = pi[-1]

    # Free memory before constructing the answer
    del pi, T, R

    ans = S + S[:n - k][::-1]
    sys.stdout.buffer.write(ans + b'\n')

if __name__ == "__main__":
    main()