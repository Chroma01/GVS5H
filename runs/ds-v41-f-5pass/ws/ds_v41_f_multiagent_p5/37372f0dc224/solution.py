import sys

def main():
    s = sys.stdin.buffer.readline().strip()
    n = len(s)
    if n == 0:
        return

    # T = reverse(S) + '#' + S
    # pi[m-1] = length of longest palindromic suffix of S
    t = s[::-1] + b'#' + s
    m = len(t)

    pi = [0] * m
    j = 0
    for i in range(1, m):
        c = t[i]
        while j and c != t[j]:
            j = pi[j - 1]
        if c == t[j]:
            j += 1
        pi[i] = j

    L = pi[m - 1]          # longest palindromic suffix length
    k = n - L              # prefix of S that must be mirrored
    ans = s + s[:k][::-1]  # S followed by reverse(S[:k])

    sys.stdout.buffer.write(ans + b'\n')

if __name__ == "__main__":
    main()