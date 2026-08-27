from typing import List, Optional
import random
import time


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        intervals = []
        for idx, (x, y) in enumerate(conflictingPairs):
            if x < y:
                a, b = x, y
            else:
                a, b = y, x
            intervals.append((b, a, idx))

        if not intervals:
            return n * (n + 1) // 2

        intervals.sort()
        m = len(intervals)
        delta = [0] * m

        max1 = 0
        max2 = 0
        cnt_max1 = 0
        unique_id = -1
        total_invalid = 0

        i = 0
        while i < m:
            b = intervals[i][0]

            while i < m and intervals[i][0] == b:
                _, a, idx = intervals[i]

                if a > max1:
                    max2 = max1
                    max1 = a
                    cnt_max1 = 1
                    unique_id = idx
                elif a == max1:
                    cnt_max1 += 1
                    unique_id = -1
                elif a > max2:
                    max2 = a

                i += 1

            next_b = intervals[i][0] if i < m else n + 1
            length = next_b - b

            total_invalid += max1 * length

            if cnt_max1 == 1:
                delta[unique_id] += (max1 - max2) * length

        total_subarrays = n * (n + 1) // 2
        return total_subarrays - total_invalid + max(delta)


def brute_max_subarrays(n: int, conflictingPairs: List[List[int]]) -> int:
    total = n * (n + 1) // 2
    m = len(conflictingPairs)
    if m == 0:
        return total

    norm = []
    for x, y in conflictingPairs:
        if x < y:
            norm.append((x, y))
        else:
            norm.append((y, x))

    bits = [1 << j for j in range(m)]
    base = 0
    exclusive = [0] * m

    for l in range(1, n + 1):
        for r in range(l, n + 1):
            mask = 0
            for j, (a, b) in enumerate(norm):
                if l <= a and r >= b:
                    mask |= bits[j]
                    if mask & (mask - 1):
                        break

            if mask == 0:
                base += 1
            elif mask & (mask - 1) == 0:
                exclusive[mask.bit_length() - 1] += 1

    return base + max(exclusive)


def check_case(
    n: int,
    pairs: List[List[int]],
    expected: Optional[int] = None,
    label: str = ""
) -> int:
    actual = Solution().maxSubarrays(n, pairs)

    if expected is not None and actual != expected:
        print(f"FAIL {label}: n={n} pairs={pairs} expected={expected} actual={actual}")
        raise AssertionError

    brute = brute_max_subarrays(n, pairs)
    if actual != brute:
        print(f"FAIL {label}: n={n} pairs={pairs} brute={brute} actual={actual}")
        raise AssertionError

    return actual


def run_random_tests() -> None:
    rng = random.Random(20240528)
    cases = 0

    def run(n: int, pairs: List[List[int]], label: str) -> None:
        nonlocal cases
        check_case(n, pairs, label=label)
        cases += 1

    for _ in range(2000):
        n = rng.randint(2, 8)
        m = rng.randint(1, 2 * n)
        pairs = []
        for _ in range(m):
            x = rng.randint(1, n)
            y = rng.randint(1, n)
            while x == y:
                y = rng.randint(1, n)
            pairs.append([x, y])
        run(n, pairs, "uniform")

    for _ in range(500):
        n = rng.randint(2, 8)
        m = rng.randint(1, 2 * n)
        b = rng.randint(2, n)
        pairs = []
        for _ in range(m):
            a = rng.randint(1, b - 1)
            if rng.random() < 0.5:
                pairs.append([a, b])
            else:
                pairs.append([b, a])
        run(n, pairs, "same-b")

    for _ in range(500):
        n = rng.randint(2, 8)
        m = rng.randint(1, 2 * n)
        a = rng.randint(1, n - 1)
        pairs = []
        for _ in range(m):
            b = rng.randint(a + 1, n)
            if rng.random() < 0.5:
                pairs.append([a, b])
            else:
                pairs.append([b, a])
        run(n, pairs, "same-a")

    for _ in range(500):
        n = rng.randint(2, 8)
        m = rng.randint(1, 2 * n)
        base_pairs = []
        for _ in range(rng.randint(1, 3)):
            x = rng.randint(1, n)
            y = rng.randint(1, n)
            while x == y:
                y = rng.randint(1, n)
            base_pairs.append([x, y])
        pairs = [base_pairs[rng.randrange(len(base_pairs))] for _ in range(m)]
        run(n, pairs, "duplicates")

    for _ in range(500):
        n = rng.randint(2, 8)
        m = rng.randint(1, 2 * n)
        a = rng.randint(1, n - 1)
        pairs = []
        for _ in range(m):
            if rng.random() < 0.6:
                b = rng.randint(a + 1, n)
                if rng.random() < 0.5:
                    pairs.append([a, b])
                else:
                    pairs.append([b, a])
            else:
                x = rng.randint(1, n)
                y = rng.randint(1, n)
                while x == y:
                    y = rng.randint(1, n)
                pairs.append([x, y])
        run(n, pairs, "tied-max")

    print(f"Random/biased checker passed: {cases} cases")


def run_performance_test() -> None:
    n = 100_000
    m = 200_000
    total = n * (n + 1) // 2
    rng = random.Random(999)

    t0 = time.perf_counter()
    ans = Solution().maxSubarrays(n, [[1, n]])
    t1 = time.perf_counter()
    assert ans == total
    print(f"Performance single n={n} m=1 answer={ans} time={t1 - t0:.3f}s")

    pairs = []
    for _ in range(m):
        x = rng.randint(1, n)
        y = rng.randint(1, n)
        while x == y:
            y = rng.randint(1, n)
        pairs.append([x, y])

    t0 = time.perf_counter()
    ans = Solution().maxSubarrays(n, pairs)
    t1 = time.perf_counter()
    assert 0 <= ans <= total
    print(f"Performance random n={n} m={m} answer={ans} time={t1 - t0:.3f}s")

    pairs = []
    for _ in range(m):
        a = rng.randint(1, n - 1)
        pairs.append([a, n])

    t0 = time.perf_counter()
    ans = Solution().maxSubarrays(n, pairs)
    t1 = time.perf_counter()
    assert 0 <= ans <= total
    print(f"Performance same-b n={n} m={m} answer={ans} time={t1 - t0:.3f}s")


def main() -> None:
    examples = [
        (4, [[2, 3], [1, 4]], 9),
        (5, [[1, 2], [2, 5], [3, 5]], 12),
    ]
    for n, pairs, expected in examples:
        check_case(n, pairs, expected=expected, label="example")
    print("Examples passed")

    targeted = [
        (2, [[1, 2]], 3),
        (2, [[1, 2], [1, 2]], 2),
        (2, [[1, 2], [2, 1]], 2),
        (3, [[1, 3], [2, 3]], 5),
        (3, [[1, 2], [1, 3]], 5),
        (3, [[2, 3], [3, 2], [1, 3]], 4),
        (4, [[2, 4], [2, 4]], 8),
        (4, [[1, 4], [2, 4], [3, 4]], 8),
        (4, [[1, 4], [1, 4], [2, 4]], 9),
        (4, [[3, 2], [4, 1]], 9),
        (5, [[1, 5], [4, 5]], 14),
        (5, [[1, 2], [4, 5]], 11),
        (6, [[4, 5], [4, 6], [3, 6]], 17),
        (5, [[2, 4], [2, 4], [3, 5]], 11),
        (5, [[3, 5], [3, 5], [4, 5]], 12),
    ]
    for n, pairs, expected in targeted:
        check_case(n, pairs, expected=expected, label="targeted")
    print("Targeted edge cases passed")

    run_random_tests()
    run_performance_test()
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()