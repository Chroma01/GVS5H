import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n, x, y = map(int, data[:3])
    s = data[3].decode()
    t = data[4].decode()

    one_residues = []
    zero_residues = []

    for i, c in enumerate(s):
        if c == "1":
            one_residues.append(i % x)
        else:
            zero_residues.append(i % y)

    one_index = 0
    zero_index = 0
    possible = True

    for i, c in enumerate(t):
        if c == "1":
            if one_index >= len(one_residues) or one_residues[one_index] != i % x:
                possible = False
                break
            one_index += 1
        else:
            if zero_index >= len(zero_residues) or zero_residues[zero_index] != i % y:
                possible = False
                break
            zero_index += 1

    if one_index != len(one_residues) or zero_index != len(zero_residues):
        possible = False

    print("Yes" if possible else "No")


if __name__ == "__main__":
    solve()