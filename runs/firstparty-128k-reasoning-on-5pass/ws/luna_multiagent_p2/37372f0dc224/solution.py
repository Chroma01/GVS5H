import sys


def solve() -> None:
    s = sys.stdin.buffer.readline().strip().decode()
    n = len(s)

    combined = s[::-1] + "#" + s
    pi = [0] * len(combined)

    for i in range(1, len(combined)):
        j = pi[i - 1]
        while j > 0 and combined[i] != combined[j]:
            j = pi[j - 1]
        if combined[i] == combined[j]:
            j += 1
        pi[i] = j

    longest_palindromic_suffix = pi[-1]
    result = s + s[:n - longest_palindromic_suffix][::-1]
    sys.stdout.write(result)


if __name__ == "__main__":
    solve()