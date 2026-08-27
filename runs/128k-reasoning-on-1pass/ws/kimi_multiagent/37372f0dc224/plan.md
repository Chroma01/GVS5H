```python
import sys

def main():
    S = sys.stdin.readline().strip()
    n = len(S)
    R = S[::-1]

    lps = [0] * n
    k = 0
    for i in range(1, n):
        while k > 0 and R[i] != R[k]:
            k = lps[k - 1]
        if R[i] == R[k]:
            k += 1
            lps[i] = k

    q = 0
    for ch in S:
        while q > 0 and (q == n or R[q] != ch):
            q = lps[q - 1]
        if q < n and R[q] == ch:
            q += 1

    L = q  # longest palindromic suffix length
    sys.stdout.write(S + S[:n - L][::-1])

if __name__ == "__main__":
    main()
```