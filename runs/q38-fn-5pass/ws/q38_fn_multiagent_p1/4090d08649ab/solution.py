import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    last = [0] * (n + 2)

    sum_last = 0
    adjacent_min_sum = 0
    ans = 0

    for i in range(1, n + 1):
        v = data[i]
        old = last[v]

        # Remove old contributions of adjacent pairs involving v.
        if v > 1:
            u = last[v - 1]
            adjacent_min_sum -= u if u < old else old
        if v < n:
            u = last[v + 1]
            adjacent_min_sum -= u if u < old else old

        # Update last occurrence and sum of last occurrences.
        sum_last += i - old
        last[v] = i

        # Add new contributions of adjacent pairs involving v.
        if v > 1:
            u = last[v - 1]
            adjacent_min_sum += u if u < i else i
        if v < n:
            u = last[v + 1]
            adjacent_min_sum += u if u < i else i

        # Contribution of all subarrays ending at i.
        ans += sum_last - adjacent_min_sum

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    solve()