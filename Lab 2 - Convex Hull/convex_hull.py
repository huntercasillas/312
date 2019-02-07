from PyQt5.QtCore import QLineF, QPointF, QThread, pyqtSignal

import time

# Find the convex hull of all sorted points O(n log n)
def convex(points):
    # Check how many points we have
    # If we have 2 or less, just return the points O(1)
    if len(points) <= 2:
        return points

    # If we have exactly 3, compute the convex hull by brute force O(1)
    elif len(points) == 3:
        # Find the slope O(1)
        slope1 = slope(points[0], points[1])
        slope2 = slope(points[0], points[2])

        # Check to see if slopes are clockwise or counter-clockwise
        if slope1 < slope2:
            # Swap the points with python's nifty shorthand (no need for a temp variable)
            points[1], points[2] = points[2], points[1]

        # If points have equal heights (y values), we need to do further checking
        elif points[1].y() == points[2].y():
            # Keep points in clockwise order
            if points[1].y() < points[0].y():
                # Swap the points
                points[1], points[2] = points[2], points[1]

        # Finally return the updated array of points
        return points

    # Else we have more than 3 points
    # Divide and conquer by splitting the points into two sides O(n log n)
    else:
        # Find center in the array of points O(1)
        center = (len(points) // 2)
        # Split the points into two sides left and right
        # Call convex recursively O(n log n)
        left = convex(points[:center])
        right = convex(points[center:])
        # Merge both sides and return the final convex hull O(n)
        return merge(left, right)


# Merge the two sides of the hull into a single polygon O(n)
def merge(left, right):
    # Start with the rightmost point of the left hull and the leftmost point of the right hull
    left_index = rightmost(left)  # O(n)
    right_index = leftmost(right)  # O(n)

    # Get upper tangent lines O(n)
    left_upper, right_upper = tangent(left, right, left_index, right_index)
    # Get lower tangent lines O(n)
    right_lower, left_lower = tangent(right, left, right_index, left_index)

    # Create final array to be populated with convex points
    hull = []

    # Both while loops combined are O(n), where n = length of the hull
    # While the lower point on the left hull does not equal the left upper point
    while left_lower != left_upper:
        # Add the point to our new array of all the convex hull points
        hull.append(left[left_lower])
        # Increase left index by 1 and mod to avoid array out of bounds error
        left_lower = (left_lower + 1) % len(left)

    # Add the last point (upper tangent of left hull) after while loop ends
    hull.append(left[left_upper])

    # While the upper point on the right hull does not equal the right lower point
    while right_upper != right_lower:
        # Add the point to our new array of all the convex hull points
        hull.append(right[right_upper])
        # Increase right index by 1 and mod to avoid array out of bounds error
        right_upper = (right_upper + 1) % len(right)

    # Add the last point (lower tangent of right hull) after while loop ends
    hull.append(right[right_lower])

    # Return the completed array of points to form the convex hull
    return hull


# Find the leftmost side of right convex hull O(n)
def leftmost(right):
    # Find the min/lowest value of x in the left convex hull and return its index in the array
    return right.index(min(right, key=lambda p: p.x()))


# Find the rightmost side of left convex hull O(n)
def rightmost(left):
    # Find the max/highest value of x in the left convex hull and return its index in the array
    return left.index(max(left, key=lambda p: p.x()))


# Find the slope O(1)
def slope(p1, p2):
    # Slope is equal to y2 - y1 divided by x2 - x1
    return (p2.y() - p1.y()) / (p2.x() - p1.x())


# Find upper and lower tangent lines O(n)
def tangent(left, right, left_index, right_index):
    # Find the slope between the current points O(1)
    current_slope = slope(left[left_index], right[right_index])
    # Set boolean for initial while loop
    initialize = True

    # In the worst case the index needed is the last in the array O(n)
    # Where n is the length of the hull (both sides combined)
    while initialize:
        initialize = False
        # Set boolean for finding the right index
        increase = True
        while increase:
            # Increase right index by 1 and mod to avoid array out of bounds error O(1)
            new_right_index = (right_index + 1) % len(right)

            # Find the slope between the next points O(1)
            next_slope = slope(left[left_index], right[new_right_index])

            # If our next slope is smaller than our current one, break out of the loop
            if current_slope > next_slope:
                increase = False
            # Otherwise update our current index and slope
            else:
                initialize = True
                right_index = new_right_index
                current_slope = next_slope

        # Set boolean for finding the left index
        decrease = True
        while decrease:
            # Decrease the left index by 1 and mod to avoid array out of bounds error O(1)
            new_left_index = (left_index - 1) % len(left)

            # Find the slope between the next points O(1)
            next_slope = slope(left[new_left_index], right[right_index])

            # If our next slope is greater than our current one, break out of the loop
            if current_slope < next_slope:
                decrease = False
            # Otherwise update our current index and slope
            else:
                initialize = True
                left_index = new_left_index
                current_slope = next_slope

    # Return our final found indexes for the tangent line
    return left_index, right_index

# Solve complex hull with the GUI provided O(n log n)
class ConvexHullSolverThread(QThread):
    def __init__(self, unsorted_points, demo):
        self.points = unsorted_points
        self.pause = demo
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    # These two signals are used for interacting with the GUI.
    show_hull = pyqtSignal(list, tuple)
    display_text = pyqtSignal(str)

    # Some additional thread signals you can implement and use for debugging, if you like
    show_tangent = pyqtSignal(list, tuple)
    erase_hull = pyqtSignal(list)
    erase_tangent = pyqtSignal(list)


    def set_points(self, unsorted_points, demo):
        self.points = unsorted_points
        self.demo = demo


    def run(self):
        assert(type(self.points) == list and type(self.points[0]) == QPointF)

        n = len(self.points)
        print('Computing Hull for set of {} points'.format(n))

        t1 = time.time()
        # Sort the points by increasing x-value O(n log n)
        sorted_points = sorted(self.points, key=lambda p: p.x())
        t2 = time.time()
        print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2-t1))
        t3 = time.time()

        # Compute the convex hull using divide and conquer O(n log n)
        hull = convex(sorted_points)
        length = len(hull)
        t4 = time.time()

        # Pass the convex hull lines back to the GUI for display
        # This is the convex polygon of all the sorted points O(n)
        polygon = [QLineF(hull[i], hull[(i + 1) % length]) for i in range(length)]

        # When passing lines to the display, pass a list of QLineF objects.
        # Each QLineF object can be created with two QPointF objects corresponding to the endpoints
        assert (type(polygon) == list and type(polygon[0]) == QLineF)

        # Send a signal to the GUI thread with the hull and its color
        self.show_hull.emit(polygon, (0, 255, 0))

        # Send a signal to the GUI thread with the time used to compute the hull
        self.display_text.emit('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
        print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
