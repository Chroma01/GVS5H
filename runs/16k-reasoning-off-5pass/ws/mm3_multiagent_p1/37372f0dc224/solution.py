import sys

def solve() -> None:
    data = sys.stdin.buffer.read().decode().strip()
    if not data:
        return
    s = data
    n = len(s)
    rev = s[::-1]
    # Build combined string: s + '#' + rev
    combined = s + '#' + rev
    m = n + 1 + n
    # Compute prefix function (pi) for KMP
    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and combined[i] != combined[j]:
            j = pi[j - 1]
        if combined[i] == combined[j]:
            j += 1
        pi[i] = j
    # The last value of pi gives the length of the longest prefix of rev
    # that matches a suffix of s, i.e., longest palindromic suffix of s.
    L = pi[-1]
    # Build answer: s + reverse of the prefix that is not part of the palindromic suffix
    to_add = rev[:n - L]  # reverse of s[0:n-L]
    # Actually rev[:n-L] is reverse of s[0:n-L] because rev is s reversed
    ans = s + to_add
    sys.stdout.write(ans)

if __name__ == "__main__":
    solve()