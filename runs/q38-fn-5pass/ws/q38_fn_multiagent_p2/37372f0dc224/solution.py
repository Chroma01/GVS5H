import sys

def solve() -> None:
    s = sys.stdin.buffer.readline().strip()
    if not s:
        return

    # T = reverse(S) + '#' + S
    # The final prefix-function value is the longest prefix of reverse(S)
    # that is also a suffix of S, i.e. the longest palindromic suffix of S.
    t = s[::-1] + b'#' + s
    n = len(t)

    pi = [0] * n
    j = 0

    for i in range(1, n):
        c = t[i]
        while j and c != t[j]:
            j = pi[j - 1]
        if c == t[j]:
            j += 1
        pi[i] = j

    k = pi[-1]
    ans = s + s[:len(s) - k][::-1]
    sys.stdout.buffer.write(ans + b'\n')

if __name__ == "__main__":
    solve()