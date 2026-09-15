import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = map(int, data)
    N = next(it)
    Q = next(it)

    A = [next(it) for _ in range(N)]

    elems = [(v, i + 1) for i, v in enumerate(A)]
    del A

    queries = []
    for idx in range(Q):
        R = next(it)
        X = next(it)
        queries.append((X, R, idx))

    del data, it

    elems.sort()
    queries.sort()

    bit = [0] * (N + 1)
    ans = [0] * Q

    e = 0
    batch = []
    batch_append = batch.append

    for X, R, idx in queries:
        while e < N and elems[e][0] <= X:
            v = elems[e][0]
            batch.clear()

            while e < N and elems[e][0] == v:
                p = elems[e][1]

                i = p - 1
                best = 0
                while i:
                    b = bit[i]
                    if b > best:
                        best = b
                    i &= i - 1

                batch_append((p, best + 1))
                e += 1

            for p, dp in batch:
                i = p
                while i <= N:
                    if dp > bit[i]:
                        bit[i] = dp
                    i += i & -i

        i = R
        best = 0
        while i:
            b = bit[i]
            if b > best:
                best = b
            i &= i - 1

        ans[idx] = best

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    main()