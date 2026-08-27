import sys

def z_algorithm(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z

def shortest_palindrome(s):
    if len(s) <= 1:
        return s
    rev = s[::-1]
    t = s + '#' + rev
    z = z_algorithm(t)
    k = z[len(s) + 1]
    return s + rev[k:]

def main():
    s = sys.stdin.readline().strip()
    print(shortest_palindrome(s))

if __name__ == "__main__":
    main()