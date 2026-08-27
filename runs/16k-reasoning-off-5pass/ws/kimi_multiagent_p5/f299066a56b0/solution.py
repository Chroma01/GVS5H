import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    half = n // 2
    j = half
    count = 0
    for i in range(half):
        while j < n and a[i] * 2 > a[j]:
            j += 1
        if j == n:
            break
        count += 1
        j += 1
    print(count)

main()