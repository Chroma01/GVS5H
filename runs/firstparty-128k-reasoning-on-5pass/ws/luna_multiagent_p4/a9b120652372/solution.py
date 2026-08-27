import sys


def solve() -> None:
    input = sys.stdin.readline
    t = int(input())
    answers = []

    for _ in range(t):
        n = int(input())
        a = input().strip()
        b = input().strip()

        initial = [i for i, ch in enumerate(a) if ch == "1"]
        target = [i for i, ch in enumerate(b) if ch == "1"]

        m = len(initial)
        q = len(target)

        if q > m:
            answers.append("-1")
            continue

        # Every positive gap between consecutive target squares must be
        # assigned to a distinct initial gap at least as large.
        possible = True
        ptr = 0

        for j in range(q - 1):
            required_gap = target[j + 1] - target[j]

            while ptr < m - 1 and initial[ptr + 1] - initial[ptr] < required_gap:
                ptr += 1

            if ptr == m - 1:
                possible = False
                break

            ptr += 1

        if not possible:
            answers.append("-1")
            continue

        # The leftmost and rightmost pieces determine the minimum number
        # of operations; all intermediate displacements can be realized
        # whenever the gap condition above holds.
        answer = max(
            target[0] - initial[0],
            initial[-1] - target[-1],
        )
        answers.append(str(answer))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()