import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0

    n = data[pos]
    pos += 1

    a = data[pos:pos + n]
    pos += n
    b = data[pos:pos + n]
    pos += n

    k = data[pos]
    pos += 1

    queries = []
    for qi in range(k):
        x = data[pos]
        y = data[pos + 1]
        pos += 2
        queries.append((x, y, qi))

    values = sorted(set(a + b))
    rank_map = {v: i + 1 for i, v in enumerate(values)}
    m = len(values)

    ar = [rank_map[v] for v in a]
    br = [rank_map[v] for v in b]

    prefix_a = [0] * (n + 1)
    prefix_b = [0] * (n + 1)
    for i in range(n):
        prefix_a[i + 1] = prefix_a[i] + a[i]
        prefix_b[i + 1] = prefix_b[i] + b[i]

    # A block size close to N / sqrt(K) minimizes the total Mo movement.
    block = max(1, int(n / max(1, k) ** 0.5))

    def block_key(q):
        x, y, qi = q
        xb = x // block
        if xb & 1:
            return xb, -y
        return xb, y

    queries.sort(key=block_key)

    cnt_a = [0] * (m + 1)
    sum_a = [0] * (m + 1)
    cnt_b = [0] * (m + 1)
    sum_b = [0] * (m + 1)

    def update(cnt, sums, p, dc, ds):
        while p <= m:
            cnt[p] += dc
            sums[p] += ds
            p += p & -p

    def absolute_sum(p, value, cnt, sums, total_count, total_sum):
        left_count = 0
        left_sum = 0
        q = p
        while q:
            left_count += cnt[q]
            left_sum += sums[q]
            q -= q & -q

        right_count = total_count - left_count
        right_sum = total_sum - left_sum
        return (
            value * left_count - left_sum
            + right_sum - value * right_count
        )

    current_x = 0
    current_y = 0
    current_answer = 0
    answers = [0] * k

    for target_x, target_y, qi in queries:
        while current_x < target_x:
            idx = current_x
            value = a[idx]
            current_answer += absolute_sum(
                ar[idx], value,
                cnt_b, sum_b,
                current_y, prefix_b[current_y]
            )
            update(cnt_a, sum_a, ar[idx], 1, value)
            current_x += 1

        while current_x > target_x:
            idx = current_x - 1
            value = a[idx]
            current_answer -= absolute_sum(
                ar[idx], value,
                cnt_b, sum_b,
                current_y, prefix_b[current_y]
            )
            update(cnt_a, sum_a, ar[idx], -1, -value)
            current_x -= 1

        while current_y < target_y:
            idx = current_y
            value = b[idx]
            current_answer += absolute_sum(
                br[idx], value,
                cnt_a, sum_a,
                current_x, prefix_a[current_x]
            )
            update(cnt_b, sum_b, br[idx], 1, value)
            current_y += 1

        while current_y > target_y:
            idx = current_y - 1
            value = b[idx]
            current_answer -= absolute_sum(
                br[idx], value,
                cnt_a, sum_a,
                current_x, prefix_a[current_x]
            )
            update(cnt_b, sum_b, br[idx], -1, -value)
            current_y -= 1

        answers[qi] = current_answer

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()