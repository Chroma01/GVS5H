import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    # Two-pointer greedy: smallest possible top, smallest possible bottom that fits.
    i = 0
    j = n // 2
    ans = 0
    while i < j and j < n:
        if A[i] * 2 <= A[j]:
            ans += 1
            i += 1
            j += 1
        else:
            j += 1
    print(ans)

if __name__ == "__main__":
    solve()