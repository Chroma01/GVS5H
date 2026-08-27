import sys


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, index, value):
        index += 1
        while index <= self.n:
            self.bit[index] += value
            index += index & -index

    def prefix_sum(self, end):
        result = 0
        while end > 0:
            result += self.bit[end]
            end -= end & -end
        return result

    def predecessor(self, pos):
        # Largest active index strictly less than pos, or -1.
        rank = self.prefix_sum(pos)
        if rank == 0:
            return -1

        idx = 0
        step = 1 << (self.n.bit_length() - 1)
        while step:
            nxt = idx + step
            if nxt <= self.n and self.bit[nxt] < rank:
                idx = nxt
                rank -= self.bit[nxt]
            step >>= 1
        return idx


def normal_form(string, x, y):
    ones = string.count("1")
    pile_count = ones + 1

    # count[p] = zeros occurring after exactly p ones.
    count = [0] * pile_count
    p = 0
    for ch in string:
        if ch == "1":
            p += 1
        else:
            count[p] += 1

    active = Fenwick(pile_count)
    blocker = [False] * pile_count
    sink = [-1] * pile_count
    final_count = [0] * pile_count

    def add_blocker(pos, destination):
        if not blocker[pos]:
            blocker[pos] = True
            active.add(pos, 1)
        sink[pos] = destination

    # Process piles in increasing number of preceding ones.  A blocker is
    # either a pile with a nonzero residue modulo X, or a terminal pile less
    # than Y positions above a lower blocker/boundary.
    for p, c in enumerate(count):
        if c == 0:
            continue

        blocks, residue = divmod(c, x)
        lower = active.predecessor(p)

        # Destination of movable X-zero blocks after all possible B rewrites.
        if lower == -1:
            if p < y:
                dest = p
            else:
                dest = p % y
        else:
            gap = p - lower
            if gap < y:
                dest = p
            else:
                dest = p - (gap // y) * y

        if residue:
            final_count[p] += residue

            if dest == p:
                # This pile cannot move its whole blocks.
                add_blocker(p, p)
            elif lower != -1 and dest == lower:
                # Whole blocks arriving here can continue along lower's route.
                add_blocker(p, sink[lower])
            else:
                # Blocks stop at a newly created terminal pile.
                add_blocker(dest, dest)
                add_blocker(p, dest)

            if blocks:
                final_count[sink[p]] += blocks * x

        elif blocks:
            if dest == p:
                # Even though divisible by X, it is too close to move.
                add_blocker(p, p)
                final_count[p] += blocks * x
            elif lower != -1 and dest == lower:
                final_count[sink[lower]] += blocks * x
            else:
                add_blocker(dest, dest)
                final_count[dest] += blocks * x

    return tuple((i, value) for i, value in enumerate(final_count) if value)


def main():
    input = sys.stdin.readline
    n, x, y = map(int, input().split())
    s = input().strip()
    t = input().strip()

    if s.count("0") != t.count("0"):
        print("No")
        return

    print("Yes" if normal_form(s, x, y) == normal_form(t, x, y) else "No")


if __name__ == "__main__":
    main()