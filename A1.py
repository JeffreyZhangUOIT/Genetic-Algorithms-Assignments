import matplotlib.pyplot as plt
import math
import time

# Returns the difference in slopes of the two lines segments between A-B and B-C
def slope(pointA, pointB, pointC):
    return (pointB[0] - pointA[0]) * (pointC[1] - pointA[1]) - (pointC[0] - pointA[0]) * (pointB[1] - pointA[1]);

# Checks if the orientation is counter clockwise or collinear we include colinear as
# "counter clockwise" since it is possible for the longest line to also be a
# side of the polygon
def CCW(pointA, pointB, pointC):
    return slope(pointA, pointB, pointC) >= 0;

# Mini algorithm for checking if a candidate line is outside the polygon. It achieves
# this by determining if the candidate line intersects with any of the sides of the
# polygon. Furthermore, simply touching the sides and not passing it is
# not counted as an intersection in this case (it's still inside the polygon)
def insidePolygon(pointA, pointB, px, py):
    # Compares the candidate line with the lines that make up the polygon
    for i in range(0, len(px) - 2):
        point = [px[i], py[i]]
        point2 = [px[i + 1], py[i + 1]]
        if CCW(pointA, pointB, point) != CCW(pointA, pointB, point):
            if CCW(point, point2, pointA) != CCW(point, point2, pointB):
                return 0

    # Compares the candidate line with the line connecting the first and last point

    if CCW(pointA, pointB, point2) != CCW(pointA, pointB, point2):
        point = [px[0], py[0]]
        if CCW(point, point2, pointA) != CCW(point, point2, pointB):
            return 0
    return 1

# Attempts to find the region of space inside the polygon that will have the
# longest line in it.
def find_region(a, b, validLine, invalidLine, limit, px, py, index):
    if limit <= 1:
        return validLine, invalidLine

    if index[0] == len(px) - 1:
        index[0] = 0
        a = px[0], py[0]
    else:
        a = px[index[0] + 1], py[index[0] + 1]

    if index[1] == len(px) - 1:
        index[1] = 0
        b = px[0], py[0]
    else:
        b = px[index[1] + 1], py[index[1] + 1]

    if insidePolygon(a, b, px, py) == 1:
        validLine = [a, b]
    else:
        invalidLine = [a, b]

    return find_region(a, b, validLine, invalidLine, limit - 1, px, py, index)

# Finds the longest line by closing the region it can exist in around it
# in a way similar to binary search. Therefore it takes constant time.
# Roughly 120 lines of code.
def find_line(valid, invalid, limit):
    if limit < 1:
        return valid
    p1 = (valid[0][0] + invalid[1][0]) / 2
    p2 = (valid[0][1] + invalid[1][1]) / 2

    if insidePolygon(p1, p2, px, py) == 1:
        valid = [p1, p2]
    else:
        invalid = [p1, p2]

    find_line(valid, invalid, limit - 1)

sides = input('How many sides does this polygon have? ')
polygon = []

for i in range(sides):
    point = input('Point in the form "x, y". ')
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
for i in range(0, sides - 1):
    for j in range (i+1, sides):
        length = math.sqrt(((px[j] - px[i]) ** 2) + ((py[j] - py[i]) ** 2))
        if length > max_distance:
            a = [px[i], py[i]]
            b = [px[j], py[j]]
            max_distance = length
index = [i, j]

# Plot the longest line
if insidePolygon(a, b, px, py) == 1:
    x1, x2, y1, y2 = a[0], b[0], a[1], b[1]
    plt.plot([x1, x2], [y1, y2], 'go-', label='longest line', linewidth = 2)
    print "the maximum line is at (", a, b, ") and has a length of ", max_distance

else:
    # Somehow, I managed to create an algorithm for finding the region with the longest line in linear time.
    # And then procceded to find the longest line to an accuracy of 10^-6 in constant time.
    valid, invalid = find_region(a, b, index, index, sides, px, py, index)
    valid = find_line(valid, invalid, 20)
    x1, x2, y1, y2 = valid[0][0], valid[1][0], valid[0][1], valid[1][1]
    plt.plot([x1, x2], [y1, y2], 'go-', label='longest line', linewidth=2)
    max_distance = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    print "the maximum line is at (", valid, ") and has a length of ", max_distance


print "The program has run for: ", time.time() - start_time, " seconds."
plt.show()