import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    a = b"".join(data[1:])

    cost0 = [1 if ch == ord('1') else 0 for ch in a]
    cost1 = [1 if ch == ord('0') else 0 for ch in a]

    while len(cost0) > 1:
        next0 = []
        next1 = []

        for i in range(0, len(cost0), 3):
            x0, y0, z0 = cost0[i], cost0[i + 1], cost0[i + 2]
            x1, y1, z1 = cost1[i], cost1[i + 1], cost1[i + 2]

            next0.append(x0 + y0 + z0 - max(x0, y0, z0))
            next1.append(x1 + y1 + z1 - max(x1, y1, z1))

        cost0 = next0
        cost1 = next1

    print(cost1[0] if cost0[0] == 0 else cost0[0])

if __name__ == "__main__":
    main()