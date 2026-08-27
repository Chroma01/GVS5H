import sys
from array import array

def main():
    s = sys.stdin.readline().strip()
    r = s[::-1]
    t = r + "#" + s

    pi = array('I', [0]) * len(t)
    j = 0

    for i in range(1, len(t)):
        while j > 0 and t[i] != t[j]:
            j = pi[j - 1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j

    longest_palindromic_suffix = pi[-1]
    answer = s + s[:len(s) - longest_palindromic_suffix][::-1]
    print(answer)

if __name__ == "__main__":
    main()