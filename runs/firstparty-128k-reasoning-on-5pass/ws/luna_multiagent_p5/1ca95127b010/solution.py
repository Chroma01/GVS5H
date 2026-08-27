import sys


def has_move(s: str, x: int, y: int) -> bool:
    n = len(s)
    runs = []
    i = 0
    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1
        runs.append((s[i], j - i))
        i = j

    for (c1, l1), (c2, l2) in zip(runs, runs[1:]):
        if c1 == "0" and c2 == "1" and l1 >= x and l2 >= y:
            return True
        if c1 == "1" and c2 == "0" and l1 >= y and l2 >= x:
            return True
    return False


def zero_residues(s: str, y: int):
    return (i % y for i, c in enumerate(s, 1) if c == "0")


def main() -> None:
    input = sys.stdin.readline
    n, x, y = map(int, input().split())
    s = input().strip()
    t = input().strip()

    if s.count("0") != t.count("0"):
        print("No")
        return

    mod = x * y
    sum_s = sum(i for i, c in enumerate(s, 1) if c == "0") % mod
    sum_t = sum(i for i, c in enumerate(t, 1) if c == "0") % mod
    if sum_s != sum_t:
        print("No")
        return

    if any(a != b for a, b in zip(zero_residues(s, y), zero_residues(t, y))):
        print("No")
        return

    movable_s = has_move(s, x, y)
    movable_t = has_move(t, x, y)

    if not movable_s or not movable_t:
        print("Yes" if s == t else "No")
        return

    print("Yes")


if __name__ == "__main__":
    main()