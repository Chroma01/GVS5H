import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    a.sort()
    total = 0
    # Pair smallest with largest, second smallest with second largest, etc.
    # If n is odd, the middle element is left unpaired automatically.
    for i in range(n // 2):
        total += a[n - 1 - i] - a[i]  # a[n-1-i] >= a[i] because of sorting
    print(total)

if __name__ == "__main__":
    solve()