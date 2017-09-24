import matplotlib.pyplot as plt
import math
import time

# Returns the difference in slopes of the two lines segments between A-B and B-C
def slope(pointA, pointB, pointC):
    return ((pointB[0] - pointA[0]) * (pointC[1] - pointA[1])) - ((pointC[0] - pointA[0]) * (pointB[1] - pointA[1]));

# Checks if the orientation is counter clockwise or collinear we include colinear as
# "counter clockwise" since it is possible for the longest line to also be a
# side of the polygon
def CCW(pointA, pointB, pointC):
    return slope(pointA, pointB, pointC) >= 0;

# Mini algorithm for checking if a candidate line is outside the polygon. It achieves
# this by determining if the candidate line intersects with any of the sides of the
# polygon. Furthermore, simply touching the sides and not passing it is
# not counted as an intersection in this case (it's still inside the polygon)
def insidePolygon(pointA, pointB):
    # Compares the candidate line with the lines that make up the polygon
    for i in range(len(px) - 1):
        point = [px[i], py[i]]
        point2 = [px[i + 1], py[i + 1]]
        if CCW(pointA, pointB, point) != CCW(pointA, pointB, point2):
            if CCW(point, point2, pointA) != CCW(point, point2, pointB):
                return 0

    # Compares the candidate line with the line connecting the first and last point
    point = [px[0], py[0]]
    point2 = px[len(px) - 1], py[len(px) - 1]
    if CCW(pointA, pointB, point) != CCW(pointA, pointB, point2):
        if CCW(point, point2, pointA) != CCW(point, point2, pointB):
            return 0
    return 1

# Attempts to find the region of space inside the polygon that will have the
# longest line in it.
def find_region(pointA, pointB, validLine, invalidLine, limit, index):
    if limit <= 1:
        return validLine, invalidLine

    if index[0] == len(px) - 1:
        index[0] = 0
        pointA = px[0], py[0]
    else:
        index[0] = index[0] + 1
        pointA = px[index[0]], py[index[0]]


    if index[1] == len(px) - 1:
        index[1] = 0
        pointB = px[0], py[0]
    else:
        index[1] = index[1] + 1
        pointB = px[index[1]], py[index[1]]

    if insidePolygon(pointA, pointB) == 1:
        new_length = math.sqrt(((pointA[0] - pointB[0]) ** 2) + ((pointA[1] - pointB[1]) ** 2))
        old_length = math.sqrt(((validLine[0][0] - validLine[1][0]) ** 2) + ((validLine[0][1] - validLine[1][1]) ** 2))
        if new_length > old_length:
            validLine = [pointA, pointB]
            invalidLine = find_longest_invalid_line()
    return find_region(pointA, pointB, validLine, invalidLine, limit - 1, index)

# Checks the adjacent lines to the invalid line, and picks the longer section of invalid line
# as the outer bound for the longest line.
def find_longest_invalid_line():
    if index[0] == 0:
        invalidLine = [px[len(px) - 1], py[len(px) - 1]], [px[index[1] - 1], py[index[1] - 1]]
    elif index[1] == 0:
        invalidLine = [px[index[0] - 1], py[index[0] - 1]], [px[len(px) - 1], py[len(px) - 1]]
    else:
        invalidLine = [px[index[0] - 1], py[index[0] - 1]], [px[index[1] - 1], py[index[1] - 1]]

    new_length = math.sqrt(((invalidLine[0][0] - invalidLine[1][0]) ** 2) + ((invalidLine[0][1] - invalidLine[1][1]) ** 2))

    if index[0] == len(px) - 1:
        invalidLine2 = [px[0], py[0]], [px[index[1] + 1], py[index[1] + 1]]

    elif index[1]== len(px) - 1:
        invalidLine2 = [px[index[0] + 1], py[index[0] + 1]], [px[0], py[0]]
    else:
        invalidLine2 = [px[index[0] + 1], py[index[0] + 1]], [px[index[1] + 1], py[index[1] + 1]]
    old_length =  math.sqrt(((invalidLine2[0][0] - invalidLine2[1][0]) ** 2) + ((invalidLine2[0][1] - invalidLine2[1][1]) ** 2))

    if old_length > new_length:
        return invalidLine2
    else:
        return invalidLine


# Finds the longest line by closing the region it can exist in around it
# in a way similar to binary search. However, n in this case is 20, so
# it takes constant time. This gives us an accuracy of at least 10^-6
def reduce_bounds(valid, invalid, limit):
    if limit < 1:
        return valid, invalid
    p1x = (valid[0][0] + invalid[0][0]) / 2.0
    p1y = (valid[0][1] + invalid[0][1]) / 2.0
    p2x = (valid[1][0] + invalid[1][0]) / 2.0
    p2y = (valid[1][1] + invalid[1][1]) / 2.0
    mp1 = [p1x, p1y]
    mp2 = [p2x, p2y]

    if insidePolygon(mp1, mp2) == 1:
        valid = [mp1, mp2]
    else:
        invalid = [mp1, mp2]
    return reduce_bounds(valid, invalid, limit - 1)

# Grabs all the points between two points and returns it as a list.
def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points

# Takes in a list of points, and finds the longest valid line in the list.
def find_longest (r1, r2):
    r1x = [x[0] for x in r1]
    r1y = [x[1] for x in r1]
    r2x = [x[0] for x in r2]
    r2y = [x[1] for x in r2]
    max_dist = 0

    for i in range(len(r1x)):
        for j in range(len(r2x)):
            length = math.sqrt(((r2x[j] - r1x[i]) ** 2) + ((r2y[j] - r1y[i]) ** 2))
            if length > max_dist:
                pointA = [r1x[i], r1y[i]]
                pointB = [r2x[j], r2y[j]]
                if insidePolygon(pointA, pointB):
                    max_dist = length
                    validA = pointA
                    validB = pointB
    return validA, validB

# Asks the user if they want to make repetitive testing easier, and sets up some variables.
dev = raw_input("Would you like to use quick input format? (y/n)")
sides = input('How many sides does this polygon have? ')
polygon = []

if ('y' in dev) or ("Y" in dev):
    # Input the points in the form [(x1, y1), (x2, y2), ... (xn, yn)]
    print "Example Input: [(30, -20), (0, 50), (-50, 50), (-60, 40), (-50, 30), (-20, 30), (10, -40), (70, -40), (70, -20)]"
    polygon = input("Please enter all the points at once.")

else:
    # Input the points one at a time.
    for i in range(sides):
        point = input('Please enter a point in the form "x, y". ')
        polygon.append(point)

print "Plotting ploygon ", polygon
start_time = time.time()

# Shoves the x coordinates of all points into a seperate list from
# the y coordinates. It's weird how matplotlib works, but it becomes
# useful later on anyway.
px = [x[0] for x in polygon]
py = [x[1] for x in polygon]

plt.plot(px, py, color='b')
plt.plot([px[len(px)-1], px[0]], [py[len(py)-1], py[0]], color='b')
max_distance = 0

# The most computationally expensive part of this algorithm, making it n^2 complexity.
# All just to find the two vertices that are the furthest apart. IS THERE A BETTER WAY?!
for i in range(sides - 1):
    for j in range (i+1, sides):
        length = math.sqrt(((px[j] - px[i]) ** 2) + ((py[j] - py[i]) ** 2))
        if length > max_distance:
            a = [px[i], py[i]]
            b = [px[j], py[j]]
            max_distance = length
            index = [i, j]
            candidate = [a, b]

# Plot the longest line
if insidePolygon(a, b) == 1:
    x1, x2, y1, y2 = a[0], b[0], a[1], b[1]
    plt.plot([x1, x2], [y1, y2], 'go-', label='longest line', linewidth = 2)
    print "The maximum line is at (", a, b, ") and has a length of ", max_distance

else:
    # Somehow, I managed to create an algorithm for finding the region with the longest line in linear time.
    # And then proceeded to find the longest line to an accuracy of 10^-6 in constant time.

    valid, invalid = find_region(a, b, [[0, 0], [0, 0]], candidate, sides, index)
    region1 = get_line(valid[0][0], valid[0][1], invalid[0][0], invalid[0][1])
    region2 = get_line(valid[1][0], valid[1][1], invalid[1][0], invalid[1][1])
    valid = find_longest(region1, region2)
    valid, invalid = reduce_bounds(valid, invalid, 20)
    x1, x2, y1, y2 = valid[0][0], valid[1][0], valid[0][1], valid[1][1]
    plt.plot([x1, x2], [y1, y2], 'go-', label='longest line', linewidth=1)
    max_distance = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    print "The maximum line is at (", valid, ") and has a length of ", max_distance


print "The program has run for: ", time.time() - start_time, " seconds."
plt.show()
