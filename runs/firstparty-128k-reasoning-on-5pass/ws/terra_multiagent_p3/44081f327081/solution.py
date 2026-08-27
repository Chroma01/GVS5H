import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    k = data[1]
    a = data[2:]

    m = max(a)
    freq = [0] * (m + 1)

    for x in a:
        freq[x] += 1

    ans = [0] * (m + 1)
    freq_local = freq
    ans_local = ans

    for d in range(1, m + 1):
        count = 0
        for multiple in range(d, m + 1, d):
            count += freq_local[multiple]
            if count >= k:
                for value in range(d, m + 1, d):
                    ans_local[value] = d
                break

    sys.stdout.write("\n".join(map(str, (ans_local[x] for x in a))))

if __name__ == "__main__":
    main()