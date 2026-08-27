import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    i = 0
    j = n // 2
    count = 0
    while i < n // 2 and j < n:
        if 2 * a[i] <= a[j]:
            count += 1
            i += 1
            j += 1
        else:
            j += 1
    print(count)

main()