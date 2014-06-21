from point2D import Point2D
import argparse
import random
import matplotlib.pyplot as plt


def closestPairBase(px):
    p1 = px[0]
    p2 = px[1]
    p3 = px[2]
    d12 = p1.distanceSquaredTo(p2)
    d13 = p1.distanceSquaredTo(p3)
    d23 = p2.distanceSquaredTo(p3)
    m = min(d12, d13, d23)
    if d12 == m:
        return [p1, p2]
    elif d13 == m:
        return [p1, p3]
    else:
        return [p2, p3]


def bestPair(pairs):
    bestpair = pairs[0]
    p1, q1 = bestpair
    best = p1.distanceSquaredTo(q1)
    for p in pairs[1:]:
        p0, p1 = p
        d = p0.distanceSquaredTo(p1)
        if d < best:
            best = d
            bestpair = p
    return bestpair


def createPoints(N):
    """
    create array of points
    px: sorted by x-coord
    py: sorted by y-coord
    """
    a = [None] * N
    d = set()
    i = 0
    while i < N:
        x = random.random()
        y = random.random()
        if x not in d and y not in d:
            d.add(x)
            d.add(y)
            a[i] = Point2D(x, y)
            i += 1

    # array of N random points in unit box
    # all points have distinct x coords and distinct y coords

    # make copies of points
    px = list(a)
    py = list(a)
    # sort by x-coords
    px.sort(key=lambda p: p.getX())
    # sort by y-coords
    py.sort(key=lambda p: p.getY())
    return px, py


def closestSplitPair(px, py, delta):
    """
    px: points sorted by x-coord
    py: points sorted by y-coord
    Q: points to left of xbar in 2D space
    R: points to right of xbar in 2D space
    xbar: x-coord of mid point of px
    delta: min(min distance betw pts in Q, min distance betw pts in R)
    returns pair pof points (p, q) if a pair exists
    returns None otherwise
    """
    n = len(px)
    xbar = px[n // 2].getX()  # x-coord of px[mid]
    sy = []
    for p in py:
        if abs(p.getX() - xbar) < delta:
            sy.append(p)  # points in py with x-coord centered around xbar
    best = delta
    bestpair = None
    # scan points in sy
    # if best pair (p, q) exists, p, q are within 7 positions from each other
    for i in range(0, len(sy) - 1):
        for j in range(1, min(len(sy) - i, 8)):
            p, q = sy[i], sy[i + j]
            d = p.distanceTo(q)
            if d < best:
                best = d
                bestpair = (p, q)
    return bestpair


def closestPair(px, py):
    """
    find pair of points that are closest to each other
    in n log n running time
    """
    # base case
    n = len(px)
    if n == 2:
        return px
    if n == 3:
        return closestPairBase(px)

    # Q = left half of px; R = right half of px
    Qx = px[:n // 2]
    Rx = px[n // 2:]
    Qx.sort(key=lambda p: p.getX())
    Rx.sort(key=lambda p: p.getX())
    Qy = []
    Ry = []
    pivot = px[len(px) // 2 - 1].getX()  # pivot is x-coord of px[mid]
    for p in py:
        if p.getX() <= pivot:
            Qy.append(p)
        else:
            Ry.append(p)

    (p1, q1) = closestPair(Qx, Qy)  # pair is in left
    (p2, q2) = closestPair(Rx, Ry)  # pair is in right
    delta = min(p1.distanceTo(q1), p2.distanceTo(q2))
    split_pair = closestSplitPair(px, py, delta)  # pair split betw left right
    # return best of the 3 candidate closest pairs
    pairs = []
    if split_pair:
        pairs.extend([(p1, q1), (p2, q2), split_pair])
    else:
        pairs.extend([(p1, q1), (p2, q2)])
    bestpair = bestPair(pairs)
    return bestpair

####################################
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('N', type=int)
    args = parser.parse_args()

    # do work
    N = args.N
    px, py = createPoints(N)
    p, q = closestPair(px, py)

    # prepare plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # plot data
    xvec = [pt.getX() for pt in px]
    yvec = [pt.getY() for pt in px]
    ax.scatter(xvec, yvec)
    plt.plot([p.getX(), q.getX()], [p.getY(), q.getY()], lw=5, color='red')

    plt.show()







