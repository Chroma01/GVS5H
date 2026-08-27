import sys

def solve():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    N = 1 << W
    cnt = [0] * N
    idx = 2
    for _ in range(H):
        s = data[idx]
        idx += 1
        # Convert row string to integer mask
        mask = int(s, 2)
        cnt[mask] += 1

    # Precompute popcount for all masks
    popcnt = [0] * N
    for i in range(1, N):
        popcnt[i] = popcnt[i >> 1] + (i & 1)

    # Build kernel f[mask] = min(popcount(mask), W - popcount(mask))
    f = [0] * N
    for i in range(N):
        pc = popcnt[i]
        f[i] = pc if pc <= W - pc else W - pc

    # Walsh-Hadamard Transform (in-place)
    def fwt(a):
        n = len(a)
        step = 1
        while step < n:
            jump = step * 2
            for i in range(0, n, jump):
                for j in range(step):
                    u = a[i + j]
                    v = a[i + j + step]
                    a[i + j] = u + v
                    a[i + j + step] = u - v
            step <<= 1

    # Forward transforms
    fwt(cnt)
    fwt(f)

    # Pointwise multiplication
    for i in range(N):
        cnt[i] *= f[i]

    # Inverse transform
    fwt(cnt)
    # Normalize by dividing by N
    for i in range(N):
        cnt[i] //= N

    # Answer is the minimum over all column masks C
    ans = min(cnt)
    print(ans)

if __name__ == "__main__":
    solve()