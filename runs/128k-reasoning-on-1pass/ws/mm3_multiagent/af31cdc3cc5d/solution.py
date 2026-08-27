import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    a.sort()
    k = n // 2                     # number of pairs
    sum_small = sum(a[:k])          # K smallest values
    sum_large = sum(a[-k:]) if k > 0 else 0   # K largest values

    ans = sum_large - sum_small
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()