import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))

    a1 = x[0]
    gaps = [x[i + 1] - x[i] for i in range(n - 1)]  # gap j (0-based) is g_{j+1}

    # Operation swaps g_i and g_{i+2} for 1 <= i <= n-3.
    # Hence odd-indexed gaps (k=1,3,5,...) permute freely among themselves,
    # and even-indexed gaps (k=2,4,...) permute freely among themselves.
    odd = sorted(gaps[0::2])   # slots k = 1,3,5,...
    even = sorted(gaps[1::2])  # slots k = 2,4,6,...

    # Weight of gap k is (n-k), decreasing in k. To minimize the sum,
    # place the largest gaps at the largest k (smallest weight).
    # So assign ascending-sorted values to ascending k within each class.
    g = [0] * (n - 1)
    for idx, j in enumerate(range(0, n - 1, 2)):
        g[j] = odd[idx]
    for idx, j in enumerate(range(1, n - 1, 2)):
        g[j] = even[idx]

    # sum = n*a1 + sum_{k=1}^{n-1} (n-k) * g_k
    total = n * a1
    for k in range(1, n):
        total += (n - k) * g[k - 1]
    sys.stdout.write(str(total) + "\n")

main()