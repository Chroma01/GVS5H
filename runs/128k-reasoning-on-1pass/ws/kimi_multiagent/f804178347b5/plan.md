```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = b"".join(data[1:])

    # cost0[i]: min changes to make this position/subtree 0
    # cost1[i]: min changes to make this position/subtree 1
    cost0 = [x - 48 for x in a]
    cost1 = [1 - x for x in cost0]

    while len(cost0) > 1:
        nxt0 = []
        nxt1 = []
        ap0 = nxt0.append
        ap1 = nxt1.append
        for i in range(0, len(cost0), 3):
            z0, z1, z2 = cost0[i], cost0[i + 1], cost0[i + 2]
            o0, o1, o2 = cost1[i], cost1[i + 1], cost1[i + 2]

            sz = z0 + z1 + z2
            so = o0 + o1 + o2

            ap0(min(sz, o0 + z1 + z2, z0 + o1 + z2, z0 + z1 + o2))
            ap1(min(so, z0 + o1 + o2, o0 + z1 + o2, o0 + o1 + z2))

        cost0, cost1 = nxt0, nxt1

    sys.stdout.write(str(cost0[0] if cost0[0] > cost1[0] else cost1[0]))

if __name__ == "__main__":
    main()
```