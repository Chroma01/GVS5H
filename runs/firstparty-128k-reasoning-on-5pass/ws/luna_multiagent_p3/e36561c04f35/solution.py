import sys


class Fenwick:
    __slots__ = ("n", "bit")

    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)
        for i in range(1, n + 1):
            self.bit[i] += 1
            j = i + (i & -i)
            if j <= n:
                self.bit[j] += self.bit[i]

    def add(self, i, value):
        bit = self.bit
        n = self.n
        while i <= n:
            bit[i] += value
            i += i & -i

    def prefix_sum(self, i):
        bit = self.bit
        result = 0
        while i:
            result += bit[i]
            i -= i & -i
        return result

    def range_sum(self, left, right):
        if left > right:
            return 0
        return self.prefix_sum(right) - self.prefix_sum(left - 1)

    def kth(self, k):
        index = 0
        step = 1 << (self.n.bit_length() - 1)
        bit = self.bit

        while step:
            nxt = index + step
            if nxt <= self.n and bit[nxt] < k:
                index = nxt
                k -= bit[nxt]
            step >>= 1

        return index + 1


def solve_case(a):
    n = len(a)

    positions = {}
    for pos, value in enumerate(a, 1):
        positions.setdefault(value, []).append(pos)

    pointers = {value: 0 for value in positions}
    fw = Fenwick(n)

    remaining = n
    answer = 0

    while remaining:
        first_pos = fw.kth(1)
        value = a[first_pos - 1]
        occ = positions[value]
        ptr = pointers[value]

        while ptr < len(occ) and fw.range_sum(occ[ptr], occ[ptr]) == 0:
            ptr += 1

        anchor = occ[ptr]
        selected_count = 1
        ptr += 1
        swaps = 0

        while ptr < len(occ):
            current = occ[ptr]

            while ptr < len(occ) and fw.range_sum(occ[ptr], occ[ptr]) == 0:
                ptr += 1

            if ptr == len(occ):
                break

            current = occ[ptr]

            active_between = fw.range_sum(anchor + 1, current - 1)
            foreign = active_between - (selected_count - 1)

            if foreign > 1:
                break

            swaps += foreign
            selected_count += 1
            ptr += 1

        pointers[value] = ptr
        answer += 1 + swaps

        for i in range(ptr - selected_count, ptr):
            fw.add(occ[i], -1)

        remaining -= selected_count

    return answer


def main():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        out.append(str(solve_case(a)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()