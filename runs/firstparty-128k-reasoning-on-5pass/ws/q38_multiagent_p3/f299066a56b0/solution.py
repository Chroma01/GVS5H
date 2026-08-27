import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]

    m = n // 2
    i = 0
    j = m
    ans = 0

    while i < m and j < n:
        if 2 * a[i] <= a[j]:
            ans += 1
            i += 1
            j += 1
        else:
            j += 1

    print(ans)

if __name__ == "__main__":
    main()