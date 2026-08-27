import sys

def main():
    s = sys.stdin.readline().strip()
    n = len(s)

    t = s[::-1] + '#' + s
    pi = [0] * len(t)

    for i in range(1, len(t)):
        j = pi[i - 1]
        while j > 0 and t[i] != t[j]:
            j = pi[j - 1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j

    longest_palindromic_suffix = pi[-1]
    answer = s + s[:n - longest_palindromic_suffix][::-1]
    sys.stdout.write(answer + '\n')

if __name__ == "__main__":
    main()