import sys


def min_swaps(s: str) -> int:
    adjusted = []
    ones = 0
    for i, ch in enumerate(s):
        if ch == '1':
            adjusted.append(i - ones)
            ones += 1

    if not adjusted:
        return 0

    med = adjusted[len(adjusted) // 2]

    # The median is always feasible, but clamping is harmless.
    n = len(s)
    k = len(adjusted)
    if med < 0:
        med = 0
    elif med > n - k:
        med = n - k

    total = 0
    for x in adjusted:
        total += abs(x - med)
    return total


def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    s = data[1] if len(data) >= 2 else data[0]
    print(min_swaps(s))


def brute_min_swaps(s: str) -> int:
    from collections import deque

    n = len(s)
    k = s.count('1')

    targets = set()
    for l in range(n - k + 1):
        targets.add('0' * l + '1' * k + '0' * (n - k - l))

    q = deque([(s, 0)])
    seen = {s}

    while q:
        state, d = q.popleft()
        if state in targets:
            return d

        for i in range(n - 1):
            if state[i] != state[i + 1]:
                lst = list(state)
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                ns = ''.join(lst)
                if ns not in seen:
                    seen.add(ns)
                    q.append((ns, d + 1))

    return -1


def selftest() -> None:
    samples = [
        (7, '0101001'),
        (3, '100'),
        (10, '0101001001'),
    ]

    for n, s in samples:
        if len(s) != n:
            raise AssertionError('bad sample length')
        if min_swaps(s) != brute_min_swaps(s):
            raise AssertionError(f'sample mismatch: {n} {s}')

    for n in range(2, 11):
        for i in range(n):
            s = '0' * i + '1' + '0' * (n - i - 1)
            if min_swaps(s) != 0:
                raise AssertionError(f'single one mismatch: {s}')

        s = '1' * n
        if min_swaps(s) != 0:
            raise AssertionError(f'all ones mismatch: {s}')

        for phase in (0, 1):
            s = ''.join('1' if (j - phase) % 2 == 0 else '0' for j in range(n))
            if '1' in s and min_swaps(s) != brute_min_swaps(s):
                raise AssertionError(f'alternating mismatch: {s}')

    import random
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(2, 8)
        s = ''.join(rng.choice('01') for _ in range(n))
        if '1' in s and min_swaps(s) != brute_min_swaps(s):
            raise AssertionError(f'random mismatch: {s}')

    print('selftest ok')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest':
        selftest()
    else:
        solve()