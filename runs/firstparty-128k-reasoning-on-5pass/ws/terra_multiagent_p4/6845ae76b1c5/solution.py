import sys
import math


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = 0

    n = data[it]
    it += 1
    a = data[it:it + n]
    it += n
    b = data[it:it + n]
    it += n
    k = data[it]
    it += 1

    queries = []
    for qi in range(k):
        x = data[it]
        y = data[it + 1]
        it += 2
        queries.append((x, y, qi))

    vals = sorted(set(a + b))
    m = len(vals)

    pos = {v: i + 1 for i, v in enumerate(vals)}
    pa = [pos[v] for v in a]
    pb = [pos[v] for v in b]

    prefix_a = [0] * (n + 1)
    prefix_b = [0] * (n + 1)
    for i in range(n):
        prefix_a[i + 1] = prefix_a[i] + a[i]
        prefix_b[i + 1] = prefix_b[i] + b[i]

    block_size = max(1, int(n / math.sqrt(k)))

    def query_key(q):
        x, y, qi = q
        block = (x - 1) // block_size
        if block & 1:
            return (block, -y)
        return (block, y)

    queries.sort(key=query_key)

    bit_ca = [0] * (m + 1)
    bit_sa = [0] * (m + 1)
    bit_cb = [0] * (m + 1)
    bit_sb = [0] * (m + 1)

    def prefix_query(bit_count, bit_sum, p):
        cnt = 0
        sm = 0
        while p:
            cnt += bit_count[p]
            sm += bit_sum[p]
            p -= p & -p
        return cnt, sm

    def bit_add(bit_count, bit_sum, p, value, delta):
        while p <= m:
            bit_count[p] += delta
            bit_sum[p] += delta * value
            p += p & -p

    def contribution(bit_count, bit_sum, p, value, total_count, total_sum):
        left_count, left_sum = prefix_query(bit_count, bit_sum, p)
        return (
            value * left_count - left_sum
            + (total_sum - left_sum) - value * (total_count - left_count)
        )

    cur_x = 0
    cur_y = 0
    current_answer = 0
    ans = [0] * k

    for target_x, target_y, qi in queries:
        while cur_x < target_x:
            value = a[cur_x]
            p = pa[cur_x]
            current_answer += contribution(
                bit_cb, bit_sb, p, value, cur_y, prefix_b[cur_y]
            )
            bit_add(bit_ca, bit_sa, p, value, 1)
            cur_x += 1

        while cur_x > target_x:
            cur_x -= 1
            value = a[cur_x]
            p = pa[cur_x]
            current_answer -= contribution(
                bit_cb, bit_sb, p, value, cur_y, prefix_b[cur_y]
            )
            bit_add(bit_ca, bit_sa, p, value, -1)

        while cur_y < target_y:
            value = b[cur_y]
            p = pb[cur_y]
            current_answer += contribution(
                bit_ca, bit_sa, p, value, cur_x, prefix_a[cur_x]
            )
            bit_add(bit_cb, bit_sb, p, value, 1)
            cur_y += 1

        while cur_y > target_y:
            cur_y -= 1
            value = b[cur_y]
            p = pb[cur_y]
            current_answer -= contribution(
                bit_ca, bit_sa, p, value, cur_x, prefix_a[cur_x]
            )
            bit_add(bit_cb, bit_sb, p, value, -1)

        ans[qi] = current_answer

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    solve()