import sys

def main():
    s = sys.stdin.buffer.readline().strip()
    n = len(s)

    # T = reverse(S) + separator + S.
    # '#' is safe because S consists only of uppercase English letters.
    t = s[::-1] + b'#' + s
    m = len(t)

    # KMP prefix function.
    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        c = t[i]
        while j and c != t[j]:
            j = pi[j - 1]
        if c == t[j]:
            j += 1
        pi[i] = j

    # Longest palindromic suffix length.
    pal_len = pi[-1]

    # Free large temporary objects before constructing the answer.
    del pi, t

    ans = s + s[:n - pal_len][::-1]
    sys.stdout.buffer.write(ans + b'\n')

if __name__ == "__main__":
    main()