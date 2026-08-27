import sys


def is_one_operation(a: bytes, b: bytes) -> bool:
    n = len(a)

    pref = [False] * (n + 1)
    pref[0] = True
    for i in range(n):
        expected = 48 if i == 0 else a[i - 1]
        pref[i + 1] = pref[i] and b[i] == expected

    suff = [False] * (n + 1)
    suff[n] = True
    for i in range(n - 1, -1, -1):
        expected = 48 if i == n - 1 else a[i + 1]
        suff[i] = suff[i + 1] and b[i] == expected

    for pivot in range(n):
        center = 49 if (
            a[pivot] == 49
            or (pivot > 0 and a[pivot - 1] == 49)
            or (pivot + 1 < n and a[pivot + 1] == 49)
        ) else 48

        if pref[pivot] and suff[pivot + 1] and b[pivot] == center:
            return True

    return False


def feasible(k: int, src: list[int], dst: list[int]) -> bool:
    """
    Check whether source pieces can be partitioned into consecutive nonempty
    groups, one for each destination position, such that:
      - every source in a group is within distance k of its destination;
      - source gaps between neighboring groups are at least destination gaps.
    """
    m = len(src)
    r = len(dst)

    if r > m:
        return False

    left_ptr = 0
    right_ptr = 0

    def bounds(target: int) -> tuple[int, int]:
        nonlocal left_ptr, right_ptr

        low = target - k
        high = target + k

        while left_ptr < m and src[left_ptr] < low:
            left_ptr += 1
        while right_ptr < m and src[right_ptr] <= high:
            right_ptr += 1

        return left_ptr, right_ptr - 1

    current_left, current_right = bounds(dst[0])

    # The first source must belong to the first target group.
    if current_left > current_right or not (current_left <= 0 <= current_right):
        return False

    start = 0

    for j in range(r - 1):
        next_left, next_right = bounds(dst[j + 1])
        if next_left > next_right:
            return False

        # Choose the earliest possible end of the current group.
        end = max(start, next_left - 1)
        if end > current_right:
            return False

        needed_gap = dst[j + 1] - dst[j]
        while end < m - 1 and src[end + 1] - src[end] < needed_gap:
            end += 1

        if end >= m - 1 or end > current_right:
            return False

        start = end + 1

        # The first source of the next group must be eligible for it.
        if start < next_left or start > next_right:
            return False

        current_left, current_right = next_left, next_right

    # The final target group must contain every remaining source, including last.
    return current_left <= start <= current_right and m - 1 <= current_right


def solve_case(n: int, a: bytes, b: bytes) -> int:
    if a == b:
        return 0

    # Radius 1 requires all moves to be induced by one common pivot.
    if is_one_operation(a, b):
        return 1

    src = [i for i, ch in enumerate(a) if ch == 49]
    dst = [i for i, ch in enumerate(b) if ch == 49]

    if len(dst) > len(src):
        return -1

    # Distance n covers every possible pair of squares.
    if not feasible(n, src, dst):
        return -1

    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid, src, dst):
            hi = mid
        else:
            lo = mid + 1

    # If radius 1 partitioning is possible but no single pivot works,
    # two operations suffice, while 0 and 1 have already been excluded.
    return 2 if lo == 1 else lo


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    pos = 1
    ans = []

    for _ in range(t):
        n = int(data[pos])
        a = data[pos + 1]
        b = data[pos + 2]
        pos += 3
        ans.append(str(solve_case(n, a, b)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()