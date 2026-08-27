import sys


class Fenwick:
    __slots__ = ("n", "bit")

    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def add(self, i, v):
        bit = self.bit
        n = self.n
        while i <= n:
            bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        bit = self.bit
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    t = data[0]
    ptr = 1
    out = []

    for _ in range(t):
        n = data[ptr]
        ptr += 1
        a = data[ptr:ptr + n]
        ptr += n

        bit = Fenwick(n)
        last_batch = [0] * (n + 1)

        batches = 0
        inversions = 0
        processed = 0

        for x in a:
            b = last_batch[x]

            if b == 0:
                batches += 1
                b = batches
                last_batch[x] = b
                bit.add(b, 1)
            else:
                later = processed - bit.sum(b)

                # Reusing the old batch costs one swap per element in
                # later batches. If at least two swaps are needed, making
                # a new batch is never worse.
                if later <= 1:
                    inversions += later
                    bit.add(b, 1)
                else:
                    batches += 1
                    b = batches
                    last_batch[x] = b
                    bit.add(b, 1)

            processed += 1

        out.append(str(batches + inversions))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()