import sys
from array import array

MOD = 998244353


class ParityDSU:
    __slots__ = ("parent", "xor_to_parent")

    def __init__(self, n):
        self.parent = array("i", [-1]) * n
        self.xor_to_parent = bytearray(n)

    def find(self, x):
        parent = self.parent
        xp = self.xor_to_parent

        r = x
        total = 0
        while parent[r] >= 0:
            total ^= xp[r]
            r = parent[r]

        cur = x
        prefix = 0
        while parent[cur] >= 0:
            nxt = parent[cur]
            edge_xor = xp[cur]
            parent[cur] = r
            xp[cur] = total ^ prefix
            prefix ^= edge_xor
            cur = nxt

        return r, total

    def unite(self, x, y, w):
        parent = self.parent
        xp = self.xor_to_parent

        rx, vx = self.find(x)
        ry, vy = self.find(y)

        if rx == ry:
            return (vx ^ vy) == w

        # Required value: value(rx) XOR value(ry).
        d = vx ^ vy ^ w

        if parent[rx] > parent[ry]:
            parent[ry] += parent[rx]
            parent[rx] = ry
            xp[rx] = d
        else:
            parent[rx] += parent[ry]
            parent[ry] = rx
            xp[ry] = d

        return True

    def component_count(self):
        return sum(x < 0 for x in self.parent)


def main():
    input = sys.stdin.buffer.readline
    t = int(input())
    ans = []

    for _ in range(t):
        h, w = map(int, input().split())
        ncell = h * w
        dsu = ParityDSU(2 * ncell)
        ok = True

        for i in range(h):
            row = input().strip()

            if not ok:
                continue

            base = i * w
            above = ((i - 1) % h) * w

            for j in range(w):
                # Horizontal boundary X[i][j]: right edge of (i,j).
                # Vertical boundary Y[i][j]: bottom edge of (i,j).
                r = base + j
                l = base + ((j - 1) % w)
                b = ncell + base + j
                top = ncell + above + j

                if row[j] == 65:  # A
                    # top XOR bottom = 1, left XOR right = 1
                    if not dsu.unite(top, b, 1):
                        ok = False
                        break
                    if not dsu.unite(l, r, 1):
                        ok = False
                        break
                else:  # B
                    # top = bottom, left = right, top XOR right = 1
                    if not dsu.unite(top, b, 0):
                        ok = False
                        break
                    if not dsu.unite(l, r, 0):
                        ok = False
                        break
                    if not dsu.unite(top, r, 1):
                        ok = False
                        break

        if not ok:
            ans.append("0")
        else:
            ans.append(str(pow(2, dsu.component_count(), MOD)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()