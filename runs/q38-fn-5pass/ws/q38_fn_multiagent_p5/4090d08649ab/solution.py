import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    last = [0] * (n + 2)

    # D = sum_v last[v]
    # P = sum_x min(last[x], last[x + 1])
    d = 0
    p = 0
    ans = 0

    for i in range(1, n + 1):
        x = data[i]
        old = last[x]

        # last[x] changes from old to i.
        d += i - old

        # Only adjacent pairs (x-1, x) and (x, x+1) can change.
        # For a neighbor with last position y, min(y, last[x]) changes
        # from min(y, old) to y because y < i.
        if x > 1:
            y = last[x - 1]
            if y > old:
                p += y - old

        if x < n:
            y = last[x + 1]
            if y > old:
                p += y - old

        last[x] = i

        # For this right endpoint i, sum over all left endpoints L of
        # (# distinct values in A[L..i]) - (# adjacent present pairs)
        # is D - P.
        ans += d - p

    print(ans)

if __name__ == "__main__":
    solve()