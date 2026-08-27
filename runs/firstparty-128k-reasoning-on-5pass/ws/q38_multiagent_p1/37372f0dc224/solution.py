import sys

def main():
    S = sys.stdin.buffer.readline().strip()
    n = len(S)
    R = S[::-1]

    # Prefix function for pattern R.
    pi = [0] * n
    j = 0
    for i in range(1, n):
        ri = R[i]
        while j > 0 and ri != R[j]:
            j = pi[j - 1]
        if ri == R[j]:
            j += 1
        pi[i] = j

    # KMP scan of S with pattern R.
    # q = longest prefix of R that is a suffix of the scanned part of S.
    q = 0
    for c in S:
        while q > 0 and c != R[q]:
            q = pi[q - 1]
        if c == R[q]:
            q += 1
        # Intentionally do not reset q when q == n.

    k = q
    ans = S + S[:n - k][::-1]
    sys.stdout.buffer.write(ans + b"\n")

if __name__ == "__main__":
    main()