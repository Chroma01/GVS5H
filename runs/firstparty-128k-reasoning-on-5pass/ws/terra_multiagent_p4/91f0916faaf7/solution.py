import sys

MOD = 998244353


def add_to(arr, idx, value):
    value += arr[idx]
    if value >= MOD:
        value -= MOD
    arr[idx] = value


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    edge_factors = []
    primes = set()

    for x in a:
        fac = {}
        d = 2
        while d * d <= x:
            if x % d == 0:
                cnt = 0
                while x % d == 0:
                    x //= d
                    cnt += 1
                fac[d] = cnt
                primes.add(d)
            d += 1 if d == 2 else 2
        if x > 1:
            fac[x] = 1
            primes.add(x)
        edge_factors.append(fac)

    answer = 1

    for p in primes:
        steps = [fac.get(p, 0) for fac in edge_factors]
        max_height = sum(steps)
        size = max_height + 1

        pows = [1] * size
        for h in range(1, size):
            pows[h] = pows[h - 1] * p % MOD

        # total[h]: weighted paths currently at h
        # hit[h]: weighted paths currently at h that have visited height 0
        total = pows[:]
        hit = [0] * size
        hit[0] = 1

        for d in steps:
            if d == 0:
                total = [(total[h] * pows[h]) % MOD for h in range(size)]
                hit = [(hit[h] * pows[h]) % MOD for h in range(size)]
                continue

            next_total = [0] * size
            next_hit = [0] * size

            for h in range(size):
                cur_total = total[h]
                if cur_total == 0:
                    continue

                cur_hit = hit[h]

                up = h + d
                if up <= max_height:
                    value = cur_total * pows[up] % MOD
                    add_to(next_total, up, value)

                    if cur_hit:
                        hit_value = cur_hit * pows[up] % MOD
                        add_to(next_hit, up, hit_value)

                down = h - d
                if down >= 0:
                    value = cur_total * pows[down] % MOD
                    add_to(next_total, down, value)

                    # Reaching zero makes every path a "hit" path.
                    if down == 0:
                        add_to(next_hit, down, value)
                    elif cur_hit:
                        hit_value = cur_hit * pows[down] % MOD
                        add_to(next_hit, down, hit_value)

            total = next_total
            hit = next_hit

        contribution = sum(hit) % MOD
        answer = answer * contribution % MOD

    print(answer)


if __name__ == "__main__":
    solve()