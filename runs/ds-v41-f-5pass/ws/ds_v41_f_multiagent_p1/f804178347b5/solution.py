import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    A = b''.join(data[1:])

    # cost to force leaf to 0 and to 1
    x = [1 if c == 49 else 0 for c in A]  # cost0
    y = [1 - v for v in x]                # cost1

    while len(x) > 1:
        n = len(x)
        nx = []
        ny = []
        ax = nx.append
        ay = ny.append

        for i in range(0, n, 3):
            x0 = x[i]
            x1 = x[i + 1]
            x2 = x[i + 2]
            y0 = y[i]
            y1 = y[i + 1]
            y2 = y[i + 2]

            if x0 >= y0:
                dx0 = x0 - y0
                dy0 = 0
            else:
                dx0 = 0
                dy0 = y0 - x0

            if x1 >= y1:
                dx1 = x1 - y1
                dy1 = 0
            else:
                dx1 = 0
                dy1 = y1 - x1

            if x2 >= y2:
                dx2 = x2 - y2
                dy2 = 0
            else:
                dx2 = 0
                dy2 = y2 - x2

            mx = dx0
            if dx1 > mx:
                mx = dx1
            if dx2 > mx:
                mx = dx2
            ax(x0 + x1 + x2 - mx)

            mx = dy0
            if dy1 > mx:
                mx = dy1
            if dy2 > mx:
                mx = dy2
            ay(y0 + y1 + y2 - mx)

        x = nx
        y = ny

    # The original root value has cost 0; the opposite value gives the answer.
    print(max(x[0], y[0]))

if __name__ == "__main__":
    main()