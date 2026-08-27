import sys


def solve():
    s = sys.stdin.readline().strip()
    r = s[::-1]
    t = r + "#" + s

    pi = [0] * len(t)
    for i in range(1, len(t)):
        j = pi[i - 1]
        while j > 0 and t[i] != t[j]:
            j = pi[j - 1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j

    palindrome_suffix_length = pi[-1]
    answer = s + s[:len(s) - palindrome_suffix_length][::-1]
    sys.stdout.write(answer + "\n")


if __name__ == "__main__":
    solve()