import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    arr = list(map(int, data[1:1 + n]))
    if n < 3:
        print(0)
        return
    arr.sort()
    count = 0
    # Check consecutive triples for equal differences
    # i from 1 to n-2 inclusive
    for i in range(1, n - 1):
        if arr[i] - arr[i - 1] == arr[i + 1] - arr[i]:
            count += 1
    print(count)

if __name__ == "__main__":
    solve()