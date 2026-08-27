from typing import List
import itertools
import random
import sys


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        C = 4 * side

        # Map each boundary point to a unique clockwise perimeter coordinate.
        # Corner priority: bottom, right, top, left.
        p = []
        for x, y in points:
            if y == 0:
                p.append(x)
            elif x == side:
                p.append(side + y)
            elif y == side:
                p.append(2 * side + (side - x))
            else:
                p.append(3 * side + (side - y))

        p.sort()
        n = len(p)
        p2 = p + [v + C for v in p]
        m = 2 * n

        def feasible(D: int) -> bool:
            if D == 0:
                return True

            # next[i] = first index j with p2[j] >= p2[i] + D
            nxt = [0] * m
            j = 0
            pp = p2
            for i in range(m):
                if j < i:
                    j = i
                target = pp[i] + D
                while j < m and pp[j] < target:
                    j += 1
                nxt[i] = j

            limit = C - D
            steps = k - 1

            for i in range(n):
                end = i + n
                pos = i
                for _ in range(steps):
                    pos = nxt[pos]
                    if pos >= end:
                        break
                else:
                    if pp[pos] - pp[i] <= limit:
                        return True

            return False

        lo = 0
        hi = min(side, C // k)

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo


def boundary_points(side: int):
    pts = []
    for x in range(side + 1):
        pts.append((x, 0))
    for y in range(1, side + 1):
        pts.append((side, y))
    for x in range(side - 1, -1, -1):
        pts.append((x, side))
    for y in range(side - 1, 0, -1):
        pts.append((0, y))
    return pts


def build_dist(points):
    n = len(points)
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            d = abs(xi - xj) + abs(yi - yj)
            dist[i][j] = dist[j][i] = d
    return dist


def exact_answers_dp(points, side: int) -> List[int]:
    """
    Exact oracle for one point set.
    For each D, build a graph with edges where Manhattan distance < D.
    A valid k-subset is an independent set. Subset DP computes the maximum
    independent set size for the full mask.
    """
    n = len(points)
    dist = build_dist(points)
    full = (1 << n) - 1
    ans = [0] * (n + 1)

    for D in range(side, 0, -1):
        neigh = [0] * n
        for i in range(n):
            m = 0
            for j in range(n):
                if i != j and dist[i][j] < D:
                    m |= 1 << j
            neigh[i] = m

        alpha = [0] * (1 << n)
        for mask in range(1, 1 << n):
            lsb = mask & -mask
            v = lsb.bit_length() - 1
            rest = mask ^ lsb
            excl = alpha[rest]
            incl = 1 + alpha[rest & (full ^ neigh[v])]
            alpha[mask] = incl if incl > excl else excl

        a = alpha[full]
        upper = min(n, a)
        for k in range(4, upper + 1):
            if ans[k] == 0:
                ans[k] = D

        if all(ans[k] != 0 for k in range(4, n + 1)):
            break

    return ans


def brute_force_max_min(points, k: int) -> int:
    """Literal exhaustive k-subset brute force, used for small/full extreme cases."""
    n = len(points)
    if k <= 1:
        return 0

    dist = build_dist(points)
    best = 0

    for comb in itertools.combinations(range(n), k):
        mn = 10**18
        for a in range(k):
            ia = comb[a]
            for b in range(a + 1, k):
                d = dist[ia][comb[b]]
                if d < mn:
                    mn = d
                    if mn <= best:
                        break
            if mn <= best:
                break
        if mn > best:
            best = mn

    return best


def exact_all_subsets(side: int, sol: Solution, mismatches: list) -> None:
    """
    Exhaustively checks every boundary subset for this side and every k.
    Uses subset DP over the full boundary set as the exact oracle.
    """
    pts = boundary_points(side)
    B = 4 * side
    dist = build_dist(pts)
    full_mask = (1 << B) - 1

    alpha_by_D = []
    for D in range(1, side + 1):
        neigh = [0] * B
        for i in range(B):
            m = 0
            for j in range(B):
                if i != j and dist[i][j] < D:
                    m |= 1 << j
            neigh[i] = m

        alpha = [0] * (1 << B)
        for mask in range(1, 1 << B):
            lsb = mask & -mask
            v = lsb.bit_length() - 1
            rest = mask ^ lsb
            excl = alpha[rest]
            incl = 1 + alpha[rest & (full_mask ^ neigh[v])]
            alpha[mask] = incl if incl > excl else excl

        alpha_by_D.append(alpha)

    size = 1 << B
    pop = [0] * size
    for mask in range(1, size):
        pop[mask] = pop[mask >> 1] + (mask & 1)

    maxDistance = sol.maxDistance

    for mask in range(size):
        n = pop[mask]
        if n < 4:
            continue

        indices = [i for i in range(B) if (mask >> i) & 1]
        points = [pts[i] for i in indices]

        for k in range(4, n + 1):
            expected = 0
            for D in range(side, 0, -1):
                if alpha_by_D[D - 1][mask] >= k:
                    expected = D
                    break

            actual = maxDistance(side, points, k)
            if actual != expected:
                mismatches.append((side, mask, k, expected, actual))
                if len(mismatches) >= 20:
                    return


def run_random_harness(side: int, sol: Solution, mismatches: list,
                       small_cases: int, large_cases: int) -> None:
    """
    For side 5/6, full subset enumeration is too large, so use deterministic
    random subsets plus full-boundary checks.
    """
    pts = boundary_points(side)
    B = 4 * side
    maxDistance = sol.maxDistance
    rng = random.Random(12345 + side)

    # Small random subsets: literal brute force when very small, DP otherwise.
    for _ in range(small_cases):
        n = rng.randint(4, min(B, 12))
        indices = rng.sample(range(B), n)
        points = [pts[i] for i in indices]

        if n <= 8:
            for k in range(4, n + 1):
                expected = brute_force_max_min(points, k)
                actual = maxDistance(side, points, k)
                if actual != expected:
                    mismatches.append((side, "random-small", k, expected, actual))
                    if len(mismatches) >= 20:
                        return
        else:
            exact = exact_answers_dp(points, side)
            for k in range(4, n + 1):
                actual = maxDistance(side, points, k)
                if actual != exact[k]:
                    mismatches.append((side, "random-small", k, exact[k], actual))
                    if len(mismatches) >= 20:
                        return

    # Larger random subsets, still exact by subset DP.
    max_large = min(B, 15)
    if max_large >= 13:
        for _ in range(large_cases):
            n = rng.randint(13, max_large)
            indices = rng.sample(range(B), n)
            points = [pts[i] for i in indices]
            exact = exact_answers_dp(points, side)

            for k in range(4, n + 1):
                actual = maxDistance(side, points, k)
                if actual != exact[k]:
                    mismatches.append((side, "random-large", k, exact[k], actual))
                    if len(mismatches) >= 20:
                        return

    # Full boundary set.
    if B <= 20:
        exact = exact_answers_dp(pts, side)
        for k in range(4, B + 1):
            actual = maxDistance(side, pts, k)
            if actual != exact[k]:
                mismatches.append((side, "full", k, exact[k], actual))
                if len(mismatches) >= 20:
                    return
    else:
        n = B
        test_ks = [4, 5, 6, 7]
        test_ks.extend([n - 1, n])
        test_ks = sorted(set(k for k in test_ks if 4 <= k <= n))

        for k in test_ks:
            expected = brute_force_max_min(pts, k)
            actual = maxDistance(side, pts, k)
            if actual != expected:
                mismatches.append((side, "full", k, expected, actual))
                if len(mismatches) >= 20:
                    return


def main() -> None:
    sol = Solution()
    mismatches = []

    examples = [
        (2, [[0, 2], [2, 0], [2, 2], [0, 0]], 4, 2),
        (2, [[0, 0], [1, 2], [2, 0], [2, 2], [2, 1]], 4, 1),
        (2, [[0, 0], [0, 1], [0, 2], [1, 2], [2, 0], [2, 2], [2, 1]], 5, 1),
    ]

    for idx, (side, points, k, expected) in enumerate(examples, 1):
        got = sol.maxDistance(side, points, k)
        print(f"example {idx}: expected {expected}, got {got}")
        if got != expected:
            mismatches.append(("example", idx, k, expected, got))

    # Exhaustive over every boundary subset for side 1..4.
    for side in range(1, 5):
        print(f"running exhaustive side {side}")
        exact_all_subsets(side, sol, mismatches)
        if len(mismatches) >= 20:
            break

    # Randomized plus full-boundary checks for side 5 and 6.
    for side in (5, 6):
        print(f"running random/full side {side}")
        run_random_harness(side, sol, mismatches, small_cases=300, large_cases=50)
        if len(mismatches) >= 20:
            break

    if mismatches:
        print("mismatches found:")
        for item in mismatches[:20]:
            print(item)
        sys.exit(1)
    else:
        print("no mismatches")


if __name__ == "__main__":
    main()