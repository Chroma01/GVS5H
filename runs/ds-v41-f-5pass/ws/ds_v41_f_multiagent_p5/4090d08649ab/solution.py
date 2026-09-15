import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    # last[v] = last index <= R where value v occurs (0 if none).
    # Sentinels last[0] = last[n+1] = 0.
    last = [0] * (n + 2)

    D = 0          # sum over v of last[v]
    P = 0          # sum over v of min(last[v], last[v+1])
    ans = 0

    for R in range(1, n + 1):
        x = a[R - 1]
        old = last[x]

        # update D: D = sum over L of distinct values in A[L..R]
        D += R - old

        # terms of P involving last[x] (neighbors x-1 and x+1)
        ly = last[x - 1]
        lz = last[x + 1]
        P -= min(old, ly) + min(old, lz)

        last[x] = R
        P += min(R, ly) + min(R, lz)

        # sum over L of f(L,R) = distinct - adjacent-pairs-both-present
        ans += D - P

    sys.stdout.write(str(ans) + "\n")

main()