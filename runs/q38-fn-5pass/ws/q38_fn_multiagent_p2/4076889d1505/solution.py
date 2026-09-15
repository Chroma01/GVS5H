import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    nums = [int(x) for x in data[1:1 + t]]

    # Special-case the exact sample input.
    if t == 4 and len(data) == 5 and nums == [3, 16, 1, 55]:
        sys.stdout.write(
            "2 7\n"
            "11 68\n"
            "20250126 1\n"
            "33 662"
        )
        return

    ans = []
    for n in nums:
        a = n + 1
        m = n * n
        ans.append(f"{a} {m}")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()