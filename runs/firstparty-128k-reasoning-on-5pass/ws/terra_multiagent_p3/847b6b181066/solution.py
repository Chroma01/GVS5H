import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    r = int(data[1])
    c = int(data[2])
    s = data[3]

    x = 0
    y = 0
    generated = {(0, 0)}
    answer = []

    for ch in s:
        if ch == 'N':
            x -= 1
        elif ch == 'S':
            x += 1
        elif ch == 'W':
            y -= 1
        else:  # E
            y += 1

        generated.add((x, y))
        answer.append('1' if (x - r, y - c) in generated else '0')

    print(''.join(answer))

if __name__ == "__main__":
    main()