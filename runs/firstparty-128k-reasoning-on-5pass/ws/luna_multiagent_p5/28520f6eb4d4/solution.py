import sys


def orient(a, b, c):
    """ twice signed area of triangle (a, b, c) """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def main():
    input = sys.stdin.buffer.readline
    n = int(input())

    hull = []
    best_num = None
    best_den = 1

    for _ in range(n):
        x, h = map(int, input().split())
        current = (x, h)

        if hull:
            left, right = 0, len(hull) - 1

            # On the upper convex hull, the intercept values are unimodal.
            # For adjacent points a,b:
            # intercept(a) - intercept(b) has the same sign as orient(a,b,current).
            while left < right:
                mid = (left + right) // 2
                if orient(hull[mid], hull[mid + 1], current) < 0:
                    left = mid + 1
                else:
                    right = mid

            px, ph = hull[left]
            numerator = x * ph - px * h
            denominator = x - px

            if best_num is None or numerator * best_den > best_num * denominator:
                best_num = numerator
                best_den = denominator

        # Maintain the upper hull of all buildings processed so far.
        while len(hull) >= 2 and orient(hull[-2], hull[-1], current) >= 0:
            hull.pop()
        hull.append(current)

    if best_num is None or best_num < 0:
        print(-1)
    else:
        print("{:.18f}".format(best_num / best_den))


if __name__ == "__main__":
    main()