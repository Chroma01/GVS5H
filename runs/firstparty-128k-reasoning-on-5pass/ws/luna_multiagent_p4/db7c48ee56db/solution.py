import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    a = data[2:]

    total_xor = 0
    for value in a:
        total_xor ^= value

    r = min(k, n - k)

    if r == 0:
        print(total_xor if k == n else 0)
        return

    indices = list(range(r))
    current_xor = 0
    for i in indices:
        current_xor ^= a[i]

    enumerate_omitted = (n - k) < k
    answer = -1

    while True:
        candidate = total_xor ^ current_xor if enumerate_omitted else current_xor
        if candidate > answer:
            answer = candidate

        pos = r - 1
        while pos >= 0 and indices[pos] == n - r + pos:
            pos -= 1

        if pos < 0:
            break

        base = indices[pos] + 1
        for j in range(pos, r):
            old_index = indices[j]
            new_index = base + (j - pos)
            current_xor ^= a[old_index] ^ a[new_index]
            indices[j] = new_index

    print(answer)


if __name__ == "__main__":
    solve()