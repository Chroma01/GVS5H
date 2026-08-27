import sys
from array import array

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = b"".join(data[1:])

    dp0 = array('I', (1 if ch == 49 else 0 for ch in s))
    dp1 = array('I', (0 if ch == 49 else 1 for ch in s))

    for _ in range(n):
        m = len(dp0) // 3
        next0 = array('I', [0]) * m
        next1 = array('I', [0]) * m

        for i in range(m):
            j = 3 * i

            a = dp0[j]
            b = dp0[j + 1]
            c = dp0[j + 2]
            next0[i] = min(a + b, a + c, b + c)

            a = dp1[j]
            b = dp1[j + 1]
            c = dp1[j + 2]
            next1[i] = min(a + b, a + c, b + c)

        dp0, dp1 = next0, next1

    print(max(dp0[0], dp1[0]))

if __name__ == "__main__":
    main()