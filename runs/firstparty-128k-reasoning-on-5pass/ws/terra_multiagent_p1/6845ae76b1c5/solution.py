import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]

    k = next(it)
    queries = [(next(it), next(it), idx) for idx in range(k)]

    values = sorted(set(a + b))
    rank = {v: i for i, v in enumerate(values)}
    m = len(values)

    ar = [rank[v] for v in a]
    br = [rank[v] for v in b]

    # One Fenwick value packs both:
    # packed = value_sum * BASE + element_count.
    # BASE exceeds every possible Fenwick-node count.
    SHIFT = 20
    BASE = 1 << SHIFT
    MASK = BASE - 1

    aval = [a[i] * BASE + 1 for i in range(n)]
    bval = [b[i] * BASE + 1 for i in range(n)]

    # For 2D Mo ordering, balance K * block_size and N^2 / block_size.
    block_size = max(1, int(n / max(1.0, k ** 0.5)))

    def mo_key(q):
        x, y, idx = q
        block = (x - 1) // block_size
        return (block, y if (block & 1) == 0 else -y)

    queries.sort(key=mo_key)

    bit_a = [0] * (m + 1)
    bit_b = [0] * (m + 1)

    def bit_add(bit, pos, delta):
        pos += 1
        while pos <= m:
            bit[pos] += delta
            pos += pos & -pos

    def distance_sum(value, pos, bit, packed_total):
        # Prefix through pos (exclusive in compressed ranks): values < value.
        i = pos
        left_packed = 0
        while i > 0:
            left_packed += bit[i]
            i -= i & -i

        left_count = left_packed & MASK
        left_sum = left_packed >> SHIFT
        total_count = packed_total & MASK
        total_sum = packed_total >> SHIFT

        return total_sum - 2 * left_sum + value * (2 * left_count - total_count)

    answers = [0] * k

    cur_x = 0
    cur_y = 0
    total_a = 0
    total_b = 0
    answer = 0

    for target_x, target_y, qi in queries:
        while cur_x < target_x:
            value = a[cur_x]
            pos = ar[cur_x]
            answer += distance_sum(value, pos, bit_b, total_b)
            packed = aval[cur_x]
            bit_add(bit_a, pos, packed)
            total_a += packed
            cur_x += 1

        while cur_x > target_x:
            cur_x -= 1
            value = a[cur_x]
            pos = ar[cur_x]
            answer -= distance_sum(value, pos, bit_b, total_b)
            packed = aval[cur_x]
            bit_add(bit_a, pos, -packed)
            total_a -= packed

        while cur_y < target_y:
            value = b[cur_y]
            pos = br[cur_y]
            answer += distance_sum(value, pos, bit_a, total_a)
            packed = bval[cur_y]
            bit_add(bit_b, pos, packed)
            total_b += packed
            cur_y += 1

        while cur_y > target_y:
            cur_y -= 1
            value = b[cur_y]
            pos = br[cur_y]
            answer -= distance_sum(value, pos, bit_a, total_a)
            packed = bval[cur_y]
            bit_add(bit_b, pos, -packed)
            total_b -= packed

        answers[qi] = answer

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()