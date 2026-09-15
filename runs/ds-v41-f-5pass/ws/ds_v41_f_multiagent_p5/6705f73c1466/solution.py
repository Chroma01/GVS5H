import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1]

    a = []
    k = 0
    for idx in range(len(s)):
        if s[idx] == 49:  # ord('1')
            k += 1
            # 1-based position of this one minus its rank among the ones
            a.append((idx + 1) - k)

    m = len(a)
    med = a[m // 2]  # a is non-decreasing, so this is a valid median
    ans = 0
    for x in a:
        if x >= med:
            ans += x - med
        else:
            ans += med - x

    sys.stdout.write(str(ans) + "\n")


main()