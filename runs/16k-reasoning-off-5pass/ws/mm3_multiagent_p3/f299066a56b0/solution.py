import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    i = 0  # pointer for top (smaller)
    j = 1  # pointer for bottom (larger)
    k = 0
    while i < n and j < n:
        if A[i] * 2 <= A[j]:
            k += 1
            i += 1
            j += 1
        else:
            j += 1
    print(k)

if __name__ == "__main__":
    solve()