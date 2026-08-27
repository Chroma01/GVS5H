import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1].decode()

    cost0 = [0 if ch == '0' else 1 for ch in s]
    cost1 = [1 if ch == '0' else 0 for ch in s]

    for _ in range(n):
        next0 = []
        next1 = []

        for i in range(0, len(cost0), 3):
            a0, a1 = cost0[i], cost1[i]
            b0, b1 = cost0[i + 1], cost1[i + 1]
            c0, c1 = cost0[i + 2], cost1[i + 2]

            next0.append(min(
                a0 + b0 + min(c0, c1),
                a0 + c0 + min(b0, b1),
                b0 + c0 + min(a0, a1)
            ))
            next1.append(min(
                a1 + b1 + min(c0, c1),
                a1 + c1 + min(b0, b1),
                b1 + c1 + min(a0, a1)
            ))

        cost0, cost1 = next0, next1

    if cost0[0] == 0:
        print(cost1[0])
    else:
        print(cost0[0])

if __name__ == "__main__":
    solve()