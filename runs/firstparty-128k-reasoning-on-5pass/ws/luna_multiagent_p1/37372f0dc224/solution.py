import sys
from array import array

def solve():
    s = sys.stdin.buffer.readline().strip()
    n = len(s)

    text = s[::-1] + b'#' + s
    m = len(text)
    prefix = array('I', [0]) * m

    for i in range(1, m):
        j = prefix[i - 1]
        while j > 0 and text[i] != text[j]:
            j = prefix[j - 1]
        if text[i] == text[j]:
            j += 1
        prefix[i] = j

    palindromic_suffix_length = prefix[-1]
    result = s + s[:n - palindromic_suffix_length][::-1]
    sys.stdout.buffer.write(result)

if __name__ == "__main__":
    solve()