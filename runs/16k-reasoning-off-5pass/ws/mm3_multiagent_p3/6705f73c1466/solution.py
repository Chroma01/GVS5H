import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    s = data[1].strip()
    k = s.count('1')
    if k == 0 or k == n:
        print(0)
        return
    # Initial window
    current_ones = s[:k].count('1')
    max_ones = current_ones
    for i in range(k, n):
        if s[i - k] == '1':
            current_ones -= 1
        if s[i] == '1':
            current_ones += 1
        if current_ones > max_ones:
            max_ones = current_ones
    print(k - max_ones)

if __name__ == "__main__":
    main()