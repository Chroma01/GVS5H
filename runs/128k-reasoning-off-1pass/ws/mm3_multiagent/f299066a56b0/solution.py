import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    i = 0
    j = 1
    count = 0
    while i < j and j < n:
        if 2 * a[i] <= a[j]:
            count += 1
            i += 1
            j += 1
        else:
            j += 1
    print(count)

if __name__ == "__main__":
    solve()