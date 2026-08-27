import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); R = int(data[1]); C = int(data[2])
    S = data[3]

    # offset (or_, oc) = cumulative wind displacement up to current time.
    # A smoke particle at world position p is stored as p - offset.
    # Birth at world (0,0) at time t is stored as -offset_t.
    smoke = set()
    smoke.add((0, 0))  # initial smoke at t=0, offset_0 = (0,0)
    or_ = 0
    oc = 0
    out = []
    for ch in S:
        if ch == 'N':
            or_ -= 1
        elif ch == 'S':
            or_ += 1
        elif ch == 'W':
            oc -= 1
        else:  # 'E'
            oc += 1
        key = (-or_, -oc)
        if key not in smoke:
            smoke.add(key)
        out.append('1' if (R - or_, C - oc) in smoke else '0')
    sys.stdout.write(''.join(out))

main()