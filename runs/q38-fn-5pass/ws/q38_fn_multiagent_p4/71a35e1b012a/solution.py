import sys
from bisect import bisect_left

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    arr = []
    full = -1

    prefR = -1
    prefI = -1

    suffL = N + 1
    suffI = -1

    p = 2
    for i in range(M):
        L = int(data[p])
        R = int(data[p + 1])
        p += 2

        arr.append((L, -R, i))

        if L == 1 and R == N:
            full = i

        if L == 1 and R > prefR:
            prefR = R
            prefI = i

        if R == N and L < suffL:
            suffL = L
            suffI = i

    ops = ['0'] * M

    def output(k):
        sys.stdout.write(str(k) + '\n' + ' '.join(ops) + '\n')

    if full != -1:
        ops[full] = '1'
        output(1)
        return

    arr.sort()

    prefix_max = []

    for pos, (L, negR, i) in enumerate(arr):
        R = -negR

        if prefix_max and prefix_max[-1] >= R:
            j = bisect_left(prefix_max, R)
            ops[arr[j][2]] = '1'
            ops[i] = '2'
            output(2)
            return

        if not prefix_max:
            prefix_max.append(R)
        elif R > prefix_max[-1]:
            prefix_max.append(R)
        else:
            prefix_max.append(prefix_max[-1])

    minR = N + 1
    minI = -1

    for L, negR, i in arr:
        R = -negR

        if minR < L:
            ops[minI] = '2'
            ops[i] = '2'
            output(2)
            return

        if R < minR:
            minR = R
            minI = i

    if prefI != -1 and suffI != -1 and prefI != suffI and prefR >= suffL - 1:
        ops[prefI] = '1'
        ops[suffI] = '1'
        output(2)
        return

    if M >= 3:
        ops[arr[0][2]] = '2'
        ops[arr[1][2]] = '1'
        ops[arr[-1][2]] = '2'
        output(3)
        return

    sys.stdout.write('-1\n')

if __name__ == '__main__':
    solve()