import sys

MOD = 998244353


def build_forward(grid, h, w):
    dp = [[0] * w for _ in range(h)]
    for i in range(h):
        row = grid[i]
        cur = dp[i]
        if i == 0:
            x = row[0] % MOD
            cur[0] = x
            for j in range(1, w):
                x = x * row[j] % MOD
                cur[j] = x
        else:
            prev = dp[i - 1]
            cur[0] = row[0] * prev[0] % MOD
            for j in range(1, w):
                cur[j] = row[j] * (prev[j] + cur[j - 1]) % MOD
    return dp


def build_suffix(grid, h, w):
    suffix = [[0] * w for _ in range(h)]
    for i in range(h - 1, -1, -1):
        row = grid[i]
        cur = suffix[i]
        for j in range(w - 1, -1, -1):
            if i == h - 1 and j == w - 1:
                cur[j] = 1
            else:
                value = 0
                if i + 1 < h:
                    value += grid[i + 1][j] * suffix[i + 1][j]
                if j + 1 < w:
                    value += row[j + 1] * cur[j + 1]
                cur[j] = value % MOD
    return suffix


def main():
    input = sys.stdin.buffer.readline

    h, w = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(h)]

    q, sh, sw = map(int, input().split())
    r, c = sh - 1, sw - 1

    n = h * w

    base_grid = [row[:] for row in grid]
    base_forward = build_forward(base_grid, h, w)
    base_suffix = build_suffix(base_grid, h, w)
    base_answer = base_forward[h - 1][w - 1]

    changed = {}
    min_r = h
    max_r = -1
    min_c = w
    max_c = -1
    spent = 0

    answers = []

    for _ in range(q):
        direction, value = input().split()
        value = int(value)

        if direction == b"L":
            c -= 1
        elif direction == b"R":
            c += 1
        elif direction == b"U":
            r -= 1
        else:
            r += 1

        grid[r][c] = value
        key = r * w + c
        changed[key] = value

        if r < min_r:
            min_r = r
        if r > max_r:
            max_r = r
        if c < min_c:
            min_c = c
        if c > max_c:
            max_c = c

        width = max_c - min_c + 1
        difference_answer = 0
        previous_row = [0] * width

        for i in range(min_r, max_r + 1):
            current_row = [0] * width
            base_row = base_grid[i]
            base_dp_row = base_forward[i]
            suffix_row = base_suffix[i]
            previous_base_dp = base_forward[i - 1] if i > 0 else None

            for offset in range(width):
                j = min_c + offset

                incoming = previous_row[offset]
                if offset:
                    incoming += current_row[offset - 1]
                    if incoming >= MOD:
                        incoming -= MOD

                cell_key = i * w + j
                new_value = changed.get(cell_key)

                injection = 0
                if new_value is not None:
                    if i == 0 and j == 0:
                        prefix = 1
                    else:
                        prefix = 0
                        if i:
                            prefix += previous_base_dp[j]
                        if j:
                            prefix += base_dp_row[j - 1]
                        prefix %= MOD

                    delta = new_value - base_grid[i][j]
                    injection = delta * (prefix + incoming) % MOD
                    difference_answer = (
                        difference_answer + injection * suffix_row[j]
                    ) % MOD

                current_row[offset] = (
                    base_row[j] * incoming + injection
                ) % MOD

            previous_row = current_row

        answers.append(str((base_answer + difference_answer) % MOD))

        spent += (max_r - min_r + 1) * width

        if spent >= n:
            base_grid = [row[:] for row in grid]
            base_forward = build_forward(base_grid, h, w)
            base_suffix = build_suffix(base_grid, h, w)
            base_answer = base_forward[h - 1][w - 1]

            changed.clear()
            min_r = h
            max_r = -1
            min_c = w
            max_c = -1
            spent = 0

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()