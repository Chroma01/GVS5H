import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    pos = [0] * (n + 1)

    for i in range(1, n + 1):
        pos[data[i]] = i

    # Fenwick tree initially containing 1 at every position.
    # For an all-ones array, bit[i] = lowbit(i).
    bit = [0] + [i & -i for i in range(1, n + 1)]

    ans = 0

    for x in range(n, 0, -1):
        idx = pos[x]

        # Current position of x among still-active values 1..x.
        rank = 0
        j = idx
        while j > 0:
            rank += bit[j]
            j -= j & -j

        # Cost to move x from rank to position x:
        # rank + (rank+1) + ... + (x-1)
        ans += (x - 1) * x // 2 - (rank - 1) * rank // 2

        # Remove x from the active set.
        j = idx
        while j <= n:
            bit[j] -= 1
            j += j & -j

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    solve()