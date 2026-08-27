import sys


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, pos, delta):
        i = pos + 1
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] += delta
            i += i & -i

    def sum(self, pos):  # prefix sum over [0, pos)
        s = 0
        i = pos
        bit = self.bit
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    A = data[1:1 + n]
    B = data[1 + n:1 + 2 * n]
    C = data[1 + 2 * n:1 + 3 * n]

    items = []  # (C, index, initially_one, finally_one, common_one)
    for i in range(n):
        a = A[i]
        b = B[i]
        if a == 0 and b == 0:
            continue
        items.append((C[i], i, a == 1, b == 1, a == 1 and b == 1))

    items.sort(key=lambda x: (x[0], x[1]))
    m = len(items)

    cnt_p = Fenwick(m)  # present initial 1s: A_i = 1
    sum_p = Fenwick(m)
    cnt_q = Fenwick(m)  # present final 1s: B_i = 1
    sum_q = Fenwick(m)

    p = q = 0
    for pos, (c, _, in_p, in_q, _) in enumerate(items):
        if in_p:
            cnt_p.add(pos, 1)
            sum_p.add(pos, c)
            p += 1
        if in_q:
            cnt_q.add(pos, 1)
            sum_q.add(pos, c)
            q += 1

    # rem_coeff: sum over current initial-1 items of C * (# present items with larger C)
    rem_coeff = 0
    seen = 0
    for pos in range(m - 1, -1, -1):
        c, _, in_p, _, _ = items[pos]
        if in_p:
            rem_coeff += c * seen
            seen += 1

    # add_coeff: sum over current final-1 items of C * (# present items with larger C + 1)
    add_coeff = 0
    seen = 0
    for pos in range(m - 1, -1, -1):
        c, _, _, in_q, _ = items[pos]
        if in_q:
            add_coeff += c * (seen + 1)
            seen += 1

    ans = rem_coeff + add_coeff  # keep no common 1: go A -> 0 -> B
    kept_sum = 0

    # Try keeping the cheapest k common 1s. Process common 1s in increasing C,
    # moving each from "temporarily turned off" to "kept on".
    for pos, (c, _, in_p, in_q, is_common) in enumerate(items):
        if not is_common:
            continue

        # Remove this common 1 from the removal set P.
        less_cnt = cnt_p.sum(pos)
        greater_cnt = p - less_cnt - 1
        less_sum = sum_p.sum(pos)
        rem_coeff -= greater_cnt * c + less_sum
        cnt_p.add(pos, -1)
        sum_p.add(pos, -c)
        p -= 1

        # Remove this common 1 from the addition set Q.
        less_cnt = cnt_q.sum(pos)
        greater_cnt = q - less_cnt - 1
        less_sum = sum_q.sum(pos)
        add_coeff -= (greater_cnt + 1) * c + less_sum
        cnt_q.add(pos, -1)
        sum_q.add(pos, -c)
        q -= 1

        kept_sum += c
        total = (p + q) * kept_sum + rem_coeff + add_coeff
        if total < ans:
            ans = total

    sys.stdout.write(str(ans))


if __name__ == "__main__":
    main()