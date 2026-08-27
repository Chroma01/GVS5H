import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    half = n // 2
    i = 0                  # pointer over candidate tops: a[0 : half]
    j = (n + 1) // 2       # pointer over candidate bottoms: a[ceil(n/2) : n]
    count = 0
    while i < half and j < n:
        if 2 * a[i] <= a[j]:
            count += 1
            i += 1
            j += 1
        else:
            j += 1
    sys.stdout.write(str(count) + "\n")

if __name__ == "__main__":
    solve()