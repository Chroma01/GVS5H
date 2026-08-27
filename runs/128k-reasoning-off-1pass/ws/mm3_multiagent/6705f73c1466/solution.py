import sys

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    # collect positions of '1' (0-indexed)
    p = [i for i, ch in enumerate(S) if ch == '1']
    k = len(p)
    # adjusted positions a[i] = p[i] - i
    a = [p[i] - i for i in range(k)]
    # median of a; any median works, pick the lower median
    med = a[k // 2]
    ans = sum(abs(ai - med) for ai in a)
    print(ans)

if __name__ == "__main__":
    solve()