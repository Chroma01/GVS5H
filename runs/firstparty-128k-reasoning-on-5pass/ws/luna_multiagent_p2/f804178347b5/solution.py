import sys
from array import array


def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1]

    cost0 = array("I", (0 if ch == ord("0") else 1 for ch in s))
    cost1 = array("I", (1 if ch == ord("0") else 0 for ch in s))

    for _ in range(n):
        m = len(cost0)
        next0 = array("I", [0]) * (m // 3)
        next1 = array("I", [0]) * (m // 3)

        for j in range(0, m, 3):
            a0, a1 = cost0[j], cost1[j]
            b0, b1 = cost0[j + 1], cost1[j + 1]
            c0, c1 = cost0[j + 2], cost1[j + 2]
            k = j // 3

            next0[k] = min(
                a0 + b0 + c0,
                a0 + b0 + c1,
                a0 + b1 + c0,
                a1 + b0 + c0,
            )
            next1[k] = min(
                a1 + b1 + c1,
                a1 + b1 + c0,
                a1 + b0 + c1,
                a0 + b1 + c1,
            )

        cost0, cost1 = next0, next1

    print(cost1[0] if cost0[0] == 0 else cost0[0])


if __name__ == "__main__":
    solve()