import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = b"".join(data[1:])

    # cost0[i]: minimum changes in this subtree to make its output 0
    # cost1[i]: minimum changes in this subtree to make its output 1
    cost0 = [x - 48 for x in a]          # '0' -> 0, '1' -> 1
    cost1 = [1 - x for x in cost0]

    while len(cost0) > 1:
        nxt0 = []
        nxt1 = []
        ap0 = nxt0.append
        ap1 = nxt1.append

        for i in range(0, len(cost0), 3):
            z0, z1, z2 = cost0[i], cost0[i + 1], cost0[i + 2]
            o0, o1, o2 = cost1[i], cost1[i + 1], cost1[i + 2]

            sum_z = z0 + z1 + z2
            sum_o = o0 + o1 + o2

            # To output 0, at least two children must output 0.
            ap0(min(
                sum_z,
                o0 + z1 + z2,
                z0 + o1 + z2,
                z0 + z1 + o2
            ))

            # To output 1, at least two children must output 1.
            ap1(min(
                sum_o,
                z0 + o1 + o2,
                o0 + z1 + o2,
                o0 + o1 + z2
            ))

        cost0, cost1 = nxt0, nxt1

    # The root's current value costs 0 to keep, so the other cost is the answer.
    sys.stdout.write(str(cost0[0] if cost0[0] > cost1[0] else cost1[0]))

if __name__ == "__main__":
    main()