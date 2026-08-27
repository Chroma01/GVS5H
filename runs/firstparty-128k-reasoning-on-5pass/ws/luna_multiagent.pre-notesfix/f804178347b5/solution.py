import sys
from array import array

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = b"".join(data[1:]).decode()

    cost0 = array("I", (0 if ch == "0" else 1 for ch in s))
    cost1 = array("I", (1 if ch == "0" else 0 for ch in s))

    for _ in range(n):
        next0 = array("I")
        next1 = array("I")

        for i in range(0, len(cost0), 3):
            a0, b0, c0 = cost0[i], cost0[i + 1], cost0[i + 2]
            a1, b1, c1 = cost1[i], cost1[i + 1], cost1[i + 2]

            # All eight assignments of the three child outputs:
            # 000, 001, 010, 100 produce 0;
            # 011, 101, 110, 111 produce 1.
            best0 = min(
                a0 + b0 + c0,
                a0 + b0 + c1,
                a0 + b1 + c0,
                a1 + b0 + c0,
            )
            best1 = min(
                a0 + b1 + c1,
                a1 + b0 + c1,
                a1 + b1 + c0,
                a1 + b1 + c1,
            )

            next0.append(best0)
            next1.append(best1)

        cost0, cost1 = next0, next1

    # Exactly one of these is zero: the unmodified root value.
    answer = cost1[0] if cost0[0] == 0 else cost0[0]
    print(answer)

if __name__ == "__main__":
    solve()