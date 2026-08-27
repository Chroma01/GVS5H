import sys
from array import array

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    s = b"".join(data[1:])

    cost0 = array('I')
    cost1 = array('I')

    for ch in s:
        if ch == ord('0'):
            cost0.append(0)
            cost1.append(1)
        else:
            cost0.append(1)
            cost1.append(0)

    for _ in range(n):
        next0 = array('I')
        next1 = array('I')

        for i in range(0, len(cost0), 3):
            a0, b0, c0 = cost0[i], cost0[i + 1], cost0[i + 2]
            a1, b1, c1 = cost1[i], cost1[i + 1], cost1[i + 2]

            next0.append(a0 + b0 + c0 - max(a0, b0, c0))
            next1.append(a1 + b1 + c1 - max(a1, b1, c1))

        cost0, cost1 = next0, next1

    if cost0[0] == 0:
        print(cost1[0])
    else:
        print(cost0[0])

if __name__ == "__main__":
    main()