
class BoundingBox:
    def __init__(self, p1, p2):
        self._min_x = min(p1[0], p2[0])
        self._min_y = min(p1[1], p2[1])
        self._max_x = max(p1[0], p2[0])
        self._max_y = max(p1[1], p2[1])

    def _in_range(self, min, value, max):
        return value >= min and value <= max

    def intersects(self, other):
        return   ((self._in_range(self._min_x, other._min_x, self._max_x) \
                or self._in_range(self._min_x, other._max_x, self._max_x)) \
              and (self._in_range(self._min_y, other._min_y, self._max_y) \
                or self._in_range(self._min_y, other._max_y, self._max_y))) \
            or   ((self._in_range(other._min_x, self._min_x, other._max_x) \
                or self._in_range(other._min_x, self._max_x, other._max_x)) \
              and (self._in_range(other._min_y, self._min_y, other._max_y) \
                or self._in_range(other._min_y, self._max_y, other._max_y))) \

def cross_product(v0, v1):
    return v0[0]*v1[1] - v1[0]*v0[1]

def right_of_segment(segment, point):
    p, q = segment
    v0 = (point[0] - p[0], point[1] - p[1])
    v1 = (q[0] - p[0], q[1] - p[1])

    return cross_product(v0, v1) > 0

def check_intersection(segment_a, segment_b):
    k, l = segment_b

    k_right = right_of_segment(segment_a, k)
    l_right = right_of_segment(segment_a, l)

    return k_right != l_right

def compute_intersection(segment_a, segment_b):
    p, q = segment_a
    k, l = segment_b

    norm = (p[0]-q[0])*(k[1]-l[1])-(p[1]-q[1])*(k[0]-l[0])
    x = ((p[0]*q[1]-p[1]*q[0])*(k[0]-l[0]) - (p[0]-q[0])*(k[0]*l[1]-k[1]*l[0])) / norm
    y = ((p[0]*q[1]-p[1]*q[0])*(k[1]-l[1]) - (p[1]-q[1])*(k[0]*l[1]-k[1]*l[0])) / norm

    return (x, y)

def num_self_intersections(line):
    added_segments = []
    intersections = 0
    for i in range(len(line)-1):
        a, b = line[i], line[i+1]

        bb = BoundingBox(a, b)

        for other_bb, (c, d) in added_segments:
            if d != a and other_bb.intersects(bb) and check_intersection((a, b), (c, d)):
                intersections += 1
            elif d == a and c == b:
                intersections += 1

        added_segments.append((bb, (a, b)))
    return intersections

def self_intersections(line):
    added_segments = []
    intersections = []
    for i in range(len(line)-1):
        a, b = line[i], line[i+1]

        bb = BoundingBox(a, b)

        for other_bb, (c, d) in added_segments:
            if d != a and other_bb.intersects(bb) and check_intersection((a, b), (c, d)):
                point = compute_intersection((a, b), (c, d))
                intersections.append(point)
            elif d == a and c == b:
                point = compute_intersection((a, b), (c, d))
                intersections.append(point)

        added_segments.append((bb, (a, b)))
    return intersections

def test_self_intersections():
    line = [(0,0), (3,3), (5,2), (4,3), (2,0), (5,1), (1,3)]

    print(self_intersections(line))

if __name__ == "__main__":
    test_self_intersections()

