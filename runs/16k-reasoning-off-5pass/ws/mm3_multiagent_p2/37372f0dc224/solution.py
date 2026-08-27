import sys

def compute_prefix_function(s: str) -> list[int]:
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = n if False else j  # keep as length, not n
        # note: above line is a no-op, just to emphasize j is the value
    return pi

def shortest_palindrome(S: str) -> str:
    n = len(S)
    rev = S[::-1]
    combined = S + '#' + rev
    pi = compute_prefix_function(combined)
    pal_suffix_len = pi[-1]  # length of longest palindromic suffix of S
    # remaining prefix to add reversed
    prefix_to_add = S[:n - pal_suffix_len]
    result = S + prefix_to_add[::-1]
    return result

def main():
    data = sys.stdin.readline().strip()
    # In case of trailing whitespace, we can just use the stripped string
    ans = shortest_palindrome(data)
    sys.stdout.write(ans + '\n')

if __name__ == "__main__":
    main()