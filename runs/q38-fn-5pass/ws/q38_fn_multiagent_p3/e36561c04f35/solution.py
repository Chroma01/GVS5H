import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    t = data[0]
    idx = 1
    out = []

    for _ in range(t):
        n = data[idx]
        idx += 1

        start = idx
        end = idx + n

        vals = []
        weights = []
        ends = []

        i = start
        while i < end:
            v = data[i]
            j = i + 1
            while j < end and data[j] == v:
                j += 1
            vals.append(v)
            weights.append(j - i)
            ends.append(j - start)  # 1-based end position inside this test case
            i = j

        idx = end

        bit = [0] * (n + 1)
        cur = [0] * (n + 1)
        cost = 0

        for k in range(len(vals) - 1, -1, -1):
            v = vals[k]
            w = weights[k]
            e = ends[k]
            j = cur[v]

            if j == 0:
                cost += 1
                x = e
                while x <= n:
                    bit[x] += w
                    x += x & -x
                cur[v] = e
            else:
                s1 = 0
                x = j - 1
                while x > 0:
                    s1 += bit[x]
                    x -= x & -x

                s2 = 0
                x = e
                while x > 0:
                    s2 += bit[x]
                    x -= x & -x

                c = s1 - s2

                if w * c > 1:
                    cost += 1
                    x = e
                    while x <= n:
                        bit[x] += w
                        x += x & -x
                    cur[v] = e
                else:
                    cost += w * c
                    x = j
                    while x <= n:
                        bit[x] += w
                        x += x & -x

        out.append(str(cost))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()