import sys


def signature(s: str, x: int, y: int):
    zero_count = s.count('0')
    residues = [0] * zero_count
    sums = [0] * x

    ones = 0
    zi = 0
    for ch in s:
        if ch == '1':
            ones += 1
        else:
            residues[zi] = ones % y
            sums[zi % x] += ones // y
            zi += 1

    return zero_count, residues, sums


def main():
    input = sys.stdin.readline
    n, x, y = map(int, input().split())
    s = input().strip()
    t = input().strip()

    if s.count('0') != t.count('0'):
        print("No")
        return

    zeros = s.count('0')
    ones = n - zeros

    # No operation can ever be performed.
    if zeros < x or ones < y:
        print("Yes" if s == t else "No")
        return

    zs, rs, ss = signature(s, x, y)
    zt, rt, st = signature(t, x, y)

    if zs != zt or rs != rt:
        print("No")
        return

    delta = ss[0] - st[0]
    for i in range(1, x):
        if ss[i] - st[i] != delta:
            print("No")
            return

    print("Yes")


if __name__ == "__main__":
    main()