import sys


def solve():
    s = sys.stdin.readline().strip()
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

    k = pi[-1]
    answer = s + s[:n - k][::-1]
    sys.stdout.write(answer)


if __name__ == "__main__":
    solve()