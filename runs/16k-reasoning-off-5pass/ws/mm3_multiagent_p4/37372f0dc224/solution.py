import sys

def shortest_palindrome_with_prefix(S: str) -> str:
    n = len(S)
    rev = S[::-1]
    combined = S + '#' + rev
    # Compute prefix function (KMP failure function)
    pi = [0] * len(combined)
    for i in range(1, len(combined)):
        j = pi[i - 1]
        while j > 0 and combined[i] != combined[j]:
            j = pi[j - 1]
        if combined[i] == combined[j]:
            j += 1
        pi[i] = j
    l = pi[-1]  # length of longest palindromic suffix of S
    # Append the reverse of the prefix that is not part of the palindromic suffix
    return S + rev[:n - l]

def main():
    S = sys.stdin.readline().strip()
    print(shortest_palindrome_with_prefix(S))

if __name__ == "__main__":
    main()