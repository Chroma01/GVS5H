import sys


def has_operation(s: str, x: int, y: int) -> bool:
    n = len(s)
    i = 0
    prev_bit = None
    prev_len = 0

    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1

        bit = s[i]
        length = j - i

        if prev_bit == "0" and bit == "1":
            if prev_len >= x and length >= y:
                return True
        elif prev_bit == "1" and bit == "0":
            if prev_len >= y and length >= x:
                return True

        prev_bit = bit
        prev_len = length
        i = j

    return False


def same_residue_sequence(s: str, t: str, bit: str, mod: int) -> bool:
    n = len(s)
    i = 0
    j = 0

    while True:
        while i < n and s[i] != bit:
            i += 1
        while j < n and t[j] != bit:
            j += 1

        if (i == n) != (j == n):
            return False
        if i == n:
            return True

        if i % mod != j % mod:
            return False

        i += 1
        j += 1


def solve() -> None:
    input = sys.stdin.readline

    n, x, y = map(int, input().split())
    s = input().strip()
    t = input().strip()

    if s == t:
        print("Yes")
        return

    if not has_operation(s, x, y) or not has_operation(t, x, y):
        print("No")
        return

    if not same_residue_sequence(s, t, "1", x):
        print("No")
        return

    if not same_residue_sequence(s, t, "0", y):
        print("No")
        return

    print("Yes")


if __name__ == "__main__":
    solve()