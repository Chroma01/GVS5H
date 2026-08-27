import sys
import random
from itertools import product


def solve_hull(points):
    def cross(o, a, b):
        return ((a[0] - o[0]) * (b[1] - o[1])
                - (a[1] - o[1]) * (b[0] - o[0]))

    hull = []
    best_num = None
    best_den = 1

    for x, y in points:
        if hull:
            lo, hi = 0, len(hull) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                xi, yi = hull[mid]
                xj, yj = hull[mid + 1]
                # slope((x,y),(xi,yi)) < slope((x,y),(xj,yj)), denominators positive
                if (y - yi) * (x - xj) < (y - yj) * (x - xi):
                    hi = mid
                else:
                    lo = mid + 1

            xj, yj = hull[lo]
            num = x * yj - xj * y
            den = x - xj
            if best_num is None or num * best_den > best_num * den:
                best_num, best_den = num, den

        p = (x, y)
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) >= 0:
            hull.pop()
        hull.append(p)

    if best_num is None or best_num < 0:
        return None
    return (best_num, best_den)


def solve_bruteforce(points):
    best_num = None
    best_den = 1
    best_pair = None

    for i in range(1, len(points)):
        xi, hi = points[i]
        for j in range(i):
            xj, hj = points[j]
            num = xi * hj - xj * hi
            den = xi - xj
            if best_num is None or num * best_den > best_num * den:
                best_num, best_den = num, den
                best_pair = (j, i)

    if best_num is None or best_num < 0:
        return None, None
    return (best_num, best_den), best_pair


def same_answer(a, b):
    if a is None or b is None:
        return a is b
    return a[0] * b[1] == b[0] * a[1]


def answer_string(ans):
    if ans is None:
        return "-1"
    return f"{ans[0]}/{ans[1]}={ans[0] / ans[1]:.18f}"


def check_case(name, points):
    hull_ans = solve_hull(points)
    brute_ans, witness = solve_bruteforce(points)
    if not same_answer(hull_ans, brute_ans):
        print("MISMATCH", name)
        print("points =", points)
        print("hull   =", answer_string(hull_ans))
        print("brute  =", answer_string(brute_ans), "witness =", witness)
        return False
    return True


def run_differential_tests():
    total = 0

    deterministic = [
        ("sample1", [(3, 2), (5, 4), (7, 5)]),
        ("sample2", [(1, 1), (2, 100)]),
        ("sample3-zero-equality", [(1, 1), (2, 2), (3, 3)]),
        ("sample4", [(10, 10), (17, 5), (20, 100), (27, 270)]),
        ("n1", [(1, 1)]),
        ("horizontal-equal-thresholds", [(1, 7), (2, 7), (5, 7), (9, 7)]),
        ("collinear-zero-intercept", [(1, 2), (2, 4), (3, 6), (4, 8)]),
        ("collinear-positive-intercept", [(1, 3), (2, 5), (3, 7), (4, 9)]),
        ("decreasing-heights", [(1, 100), (2, 50), (3, 25), (4, 12), (5, 6)]),
        ("increasing-fast-negative", [(1, 1), (2, 100), (3, 10000)]),
        ("tall-early-blocks-low-later", [(1, 100), (2, 1), (3, 2), (4, 3)]),
        ("low-early-tall-later", [(1, 1), (2, 2), (3, 100), (4, 101)]),
    ]
    for name, pts in deterministic:
        total += 1
        if not check_case(name, pts):
            return False

    # Exhaustive small sanity net: x = 1..n, heights in 1..4.
    for n in range(1, 6):
        for hs in product(range(1, 5), repeat=n):
            pts = [(i + 1, hs[i]) for i in range(n)]
            total += 1
            if not check_case(f"exhaustive-n{n}", pts):
                return False

    rng = random.Random(20240521)

    for t in range(1500):
        n = rng.randint(1, 50)
        xs = []
        cur = 0
        for _ in range(n):
            cur += rng.randint(1, 12)
            xs.append(cur)

        mode = rng.randrange(7)
        if mode == 0:
            hs = [rng.randint(1, 80) for _ in range(n)]
        elif mode == 1:
            hs = sorted(rng.randint(1, 80) for _ in range(n))
        elif mode == 2:
            hs = sorted((rng.randint(1, 80) for _ in range(n)), reverse=True)
        elif mode == 3:
            a = rng.randint(0, 4)
            c = rng.randint(0, 8)
            if a == 0 and c == 0:
                c = 1
            hs = [a * x + c for x in xs]
        elif mode == 4:
            h = rng.randint(1, 50)
            hs = [h] * n
        elif mode == 5:
            hs = [rng.randint(50, 100)] + [rng.randint(1, 20) for _ in range(n - 1)]
        else:
            hs = [rng.randint(1, 20) for _ in range(n - 1)] + [rng.randint(50, 100)] if n > 1 else [1]

        pts = list(zip(xs, hs))
        total += 1
        if not check_case(f"random-{t}-mode-{mode}", pts):
            return False

    # A few big-coordinate/big-height cases to stress exact integer comparisons.
    for t in range(200):
        n = rng.randint(1, 8)
        xs = []
        cur = 0
        for _ in range(n):
            cur += rng.randint(1, 10**8)
            xs.append(cur)
        hs = [rng.randint(1, 10**9) for _ in range(n)]
        pts = list(zip(xs, hs))
        total += 1
        if not check_case(f"big-{t}", pts):
            return False

    print(f"OK {total} differential cases")
    return True


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        ok = run_differential_tests()
        sys.exit(0 if ok else 1)

    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    pts = [(data[i], data[i + 1]) for i in range(1, 2 * n + 1, 2)]

    ans = solve_hull(pts)
    if ans is None:
        sys.stdout.write("-1\n")
    else:
        sys.stdout.write("{:.18f}\n".format(ans[0] / ans[1]))


if __name__ == "__main__":
    main()