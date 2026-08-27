import sys


def solve():
    s = sys.stdin.buffer.readline().strip()
    combined = s[::-1] + b'\x00' + s

    pi = [0] * len(combined)
    for i in range(1, len(combined)):
        j = pi[i - 1]
        while j > 0 and combined[i] != combined[j]:
            j = pi[j - 1]
        if combined[i] == combined[j]:
            j += 1
        pi[i] = j

    k = pi[-1]
    answer = s + s[:len(s) - k][::-1]
    sys.stdout.buffer.write(answer + b'\n')


if __name__ == "__main__":
    solve()