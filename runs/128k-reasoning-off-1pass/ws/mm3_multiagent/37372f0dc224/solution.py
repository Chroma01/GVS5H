import sys

def compute_prefix_function(p: str):
    """Compute the prefix function (pi) for KMP on string p."""
    n = len(p)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i-1]
        while j > 0 and p[i] != p[j]:
            j = pi[j-1]
        if p[i] == p[j]:
            j += 1
        pi[i] = j
    return pi

def shortest_palindrome_prefix(s: str) -> str:
    n = len(s)
    rev_s = s[::-1]
    # Combine with a delimiter that cannot appear in S (S has only uppercase letters)
    combined = s + '#' + rev_s
    pi = compute_prefix_function(combined)
    # The length of the longest prefix of s that is a palindromic suffix of s
    l = pi[-1]
    # Append the reverse of the prefix that is not part of the palindromic suffix
    to_add = rev_s[:n - l]
    return s + to_add

def main():
    s = sys.stdin.readline().strip()
    if not s:
        return
    result = shortest_palindrome_prefix(s)
    print(result)

if __name__ == "__main__":
    main()