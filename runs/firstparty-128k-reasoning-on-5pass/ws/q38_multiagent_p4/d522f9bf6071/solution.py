from typing import List
from bisect import bisect_left
import random
import sys
from itertools import product


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        # Store as (right, left, original_index, weight) and sort by right endpoint.
        arr = [(r, l, i, w) for i, (l, r, w) in enumerate(intervals)]
        arr.sort()
        rights = [x[0] for x in arr]

        bl = bisect_left
        NEG = -1

        # scores[c][i] = best score using exactly c intervals among first i sorted intervals
        # tuples[c][i] = lexicographically smallest sorted index tuple for that score
        scores = [[NEG] * (n + 1) for _ in range(5)]
        tuples = [[None] * (n + 1) for _ in range(5)]

        scores[0] = [0] * (n + 1)
        tuples[0] = [()] * (n + 1)

        for i in range(n):
            r, l, idx, w = arr[i]

            # Number of previous intervals ending strictly before l.
            pi = bl(rights, l, 0, i)
            i1 = i + 1

            # Skip interval i.
            for c in range(5):
                scores[c][i1] = scores[c][i]
                tuples[c][i1] = tuples[c][i]

            # Take interval i.
            for c in range(1, 5):
                prev_score = scores[c - 1][pi]
                if prev_score == NEG:
                    continue

                cand_score = prev_score + w
                cur_score = scores[c][i1]

                if cand_score > cur_score:
                    prev_tuple = tuples[c - 1][pi]
                    pos = bl(prev_tuple, idx)
                    cand_tuple = prev_tuple[:pos] + (idx,) + prev_tuple[pos:]
                    scores[c][i1] = cand_score
                    tuples[c][i1] = cand_tuple
                elif cand_score == cur_score:
                    prev_tuple = tuples[c - 1][pi]
                    pos = bl(prev_tuple, idx)
                    cand_tuple = prev_tuple[:pos] + (idx,) + prev_tuple[pos:]
                    cur_tuple = tuples[c][i1]
                    if cur_tuple is None or cand_tuple < cur_tuple:
                        scores[c][i1] = cand_score
                        tuples[c][i1] = cand_tuple

        best_score = -1
        best_tuple = ()

        for c in range(5):
            s = scores[c][n]
            t = tuples[c][n]
            if t is None:
                continue
            if s > best_score or (s == best_score and t < best_tuple):
                best_score = s
                best_tuple = t

        return list(best_tuple)


MAX_N = 12
MAX_MASK = 1 << MAX_N
POPCOUNT = [0] * MAX_MASK
LSB_INDEX = [0] * MAX_MASK
for mask in range(1, MAX_MASK):
    POPCOUNT[mask] = POPCOUNT[mask >> 1] + (mask & 1)
    LSB_INDEX[mask] = (mask & -mask).bit_length() - 1
MASK_TUPLES = [tuple(i for i in range(MAX_N) if (mask >> i) & 1) for mask in range(MAX_MASK)]


def brute_force(intervals: List[List[int]]) -> List[int]:
    n = len(intervals)
    if n > MAX_N:
        raise ValueError("brute_force is only for n <= 12")

    compat = [0] * n
    for i in range(n):
        li, ri, _ = intervals[i]
        for j in range(n):
            if i == j:
                continue
            lj, rj, _ = intervals[j]
            if ri < lj or rj < li:
                compat[i] |= 1 << j

    size = 1 << n
    score = [0] * size
    valid = [False] * size
    valid[0] = True

    best_score = -1
    best = ()

    for mask in range(size):
        if mask:
            i = LSB_INDEX[mask]
            prev = mask & (mask - 1)
            score[mask] = score[prev] + intervals[i][2]
            valid[mask] = valid[prev] and ((prev & ~compat[i]) == 0)

        if not valid[mask] or POPCOUNT[mask] > 4:
            continue

        s = score[mask]
        if s < best_score:
            continue

        cand = MASK_TUPLES[mask]
        if s > best_score or (s == best_score and cand < best):
            best_score = s
            best = cand

    return list(best)


def check_case(intervals, expected=None, label="") -> bool:
    got = Solution().maximumWeight([list(x) for x in intervals])
    brute = brute_force(intervals)

    if (
        len(got) > 4
        or len(set(got)) != len(got)
        or got != sorted(got)
        or any(x < 0 or x >= len(intervals) for x in got)
        or got != brute
        or (expected is not None and got != expected)
    ):
        print(f"MISMATCH {label}: intervals={intervals}")
        print(f"  brute={brute} expected={expected} got={got}")
        return False
    return True


def run_tests() -> None:
    ex1 = [[1, 3, 2], [4, 5, 2], [1, 5, 5], [6, 9, 3], [6, 7, 1], [8, 9, 1]]
    ex2 = [[5, 8, 1], [6, 7, 7], [4, 7, 3], [9, 10, 6], [7, 8, 2], [11, 14, 3], [3, 5, 5]]

    if not check_case(ex1, [2, 3], "example1"):
        sys.exit(1)
    if not check_case(ex2, [1, 3, 5, 6], "example2"):
        sys.exit(1)

    edge_cases = [
        ([], []),
        ([[1, 1, 1]], [0]),
        ([[1, 2, 5], [2, 3, 5]], [0]),
        ([[1, 2, 5], [3, 4, 5]], [0, 1]),
        ([[1, 2, 1], [1, 2, 1], [3, 4, 1]], [0, 2]),
        ([[1, 2, 1], [2, 3, 1], [3, 4, 1]], [0, 2]),
        ([[1, 3, 3], [2, 2, 1], [3, 3, 2]], [0]),
        ([[1, 1, 1], [2, 2, 2], [1, 2, 3]], [0, 1]),
        ([[1, 3, 1], [2, 3, 2], [4, 5, 1]], [1, 2]),
        ([[1, 1, 1], [2, 2, 1], [3, 3, 1], [4, 4, 1], [5, 5, 1]], [0, 1, 2, 3]),
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]], [0]),
        ([[10, 10, 1], [1, 1, 1], [2, 2, 1], [3, 3, 1]], [0, 1, 2, 3]),
        ([[1, 10**9 - 1, 1], [10**9, 10**9, 1]], [0, 1]),
        ([[1, 10**9, 1], [1, 10**9, 1]], [0]),
        ([[1, 5, 2], [6, 6, 1], [7, 7, 1], [2, 3, 1], [4, 5, 1]], [0, 1, 2]),
        ([[1, 1, 1], [2, 2, 1], [1, 2, 2], [3, 3, 1], [4, 4, 1]], [0, 1, 3, 4]),
        ([[1, 1, 1], [1, 1, 2], [2, 2, 1]], [1, 2]),
        ([[1, 3, 1], [2, 3, 2], [3, 3, 3], [4, 4, 1]], [2, 3]),
        ([[1, 10, 1], [1, 1, 1]], [0]),
        ([[i, i, 1] for i in range(1, 13)], [0, 1, 2, 3]),
        ([[12 - i, 12 - i, 1] for i in range(12)], [0, 1, 2, 3]),
        ([[i, i, 1 if i == 2 else 2] for i in range(1, 13)], [0, 2, 3, 4]),
        ([[12 - i, 12 - i, 1 if i == 1 else 2] for i in range(12)], [0, 2, 3, 4]),
    ]

    for idx, (case, expected) in enumerate(edge_cases):
        if not check_case(case, expected, f"edge{idx}"):
            sys.exit(1)

    pool = [
        [1, 1, 1], [1, 1, 2],
        [1, 2, 1], [1, 2, 2],
        [2, 2, 1], [2, 2, 2],
        [2, 3, 1], [2, 3, 2],
        [3, 3, 1], [3, 3, 2],
    ]
    for n in range(1, 4):
        for combo in product(pool, repeat=n):
            intervals = [list(x) for x in combo]
            if not check_case(intervals, None, f"exhaustive{n}"):
                sys.exit(1)

    random.seed(12345)

    for t in range(3000):
        n = random.randint(1, 12)
        max_coord = random.choice([3, 4, 5, 6, 8, 10])
        max_w = random.choice([1, 2, 3, 5])
        intervals = []
        for _ in range(n):
            l = random.randint(1, max_coord)
            r = random.randint(l, max_coord)
            w = random.randint(1, max_w)
            if intervals and random.random() < 0.25:
                l, r, w = random.choice(intervals)
            intervals.append([l, r, w])
        if not check_case(intervals, None, f"random{t}"):
            sys.exit(1)

    for t in range(500):
        n = 12
        max_coord = random.choice([4, 5, 6, 7])
        max_w = random.choice([1, 2, 3])
        intervals = []
        for _ in range(n):
            l = random.randint(1, max_coord)
            r = random.randint(l, max_coord)
            w = random.randint(1, max_w)
            if intervals and random.random() < 0.35:
                l, r, w = random.choice(intervals)
            intervals.append([l, r, w])
        if not check_case(intervals, None, f"random12_{t}"):
            sys.exit(1)

    print("No mismatches found.")


if __name__ == "__main__":
    run_tests()