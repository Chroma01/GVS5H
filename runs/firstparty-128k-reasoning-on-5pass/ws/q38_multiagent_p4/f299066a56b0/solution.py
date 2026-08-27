import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    m = n // 2
    i = 0
    j = m
    ans = 0

    while i < m and j < n:
        if a[i] * 2 <= a[j]:
            ans += 1
            i += 1
            j += 1
        else:
            j += 1

    print(ans)

if __name__ == "__main__":
    main()