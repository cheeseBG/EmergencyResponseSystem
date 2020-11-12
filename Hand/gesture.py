from math import sqrt, acos
from math import degrees

gesture_dict = {'11111': "zero",
                '10111': "one",
                '10011': "two",
                '10001': "three",
                '10000': "four",
                '00000': "five",
                 }


def handedness(point0, point1):
    if point1[0] > point0[0]:
        return 'left'
    elif point0[0] > point1[0]:
        return 'right'


def transf_vector(point1, point2, point3):

    # point21 vector
    v1 = [point1[0] - point2[0],
            point1[1] - point2[1],
            point1[2] - point2[2]]

    # point23 vector
    v2 = [point3[0] - point2[0],
            point3[1] - point2[1],
            point3[2] - point2[2]]

    return v1, v2


def normalize(vec):
    len = sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])
    return [vec[0] / len, vec[1] / len, vec[2] / len]


# Dot product
def dot(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2]


def get_degree(vec1, vec2):
    return degrees(acos(dot(normalize(vec1), normalize(vec2))))


def bent_or_straight(degree, thumb_check):
    threshold = 90.0
    thumb_threshold = 160.0

    # if bent, return 1
    if thumb_check == 0:
        if degree < threshold:
            return 1
        else:
            return 0
    elif thumb_check == 1:
        if degree < thumb_threshold:
            return 1
        else:
            return 0


# Angle
def define_gesture(lnd_list):
    hand_map = ''
    finger_idx = [2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18, 20]
    cnt = 0

    for i in range(0, 5):
        vec1, vec2 = transf_vector(lnd_list[finger_idx[cnt]],
                                   lnd_list[finger_idx[cnt+1]],
                                   lnd_list[finger_idx[cnt+2]])
        if i == 0:
            hand_map += str(bent_or_straight(get_degree(vec1, vec2), 1))
        else:
            hand_map += str(bent_or_straight(get_degree(vec1, vec2), 0))
        cnt += 3

    return hand_map


def find_gesture(hand_map):
    try:
        return gesture_dict[hand_map]
    except:
        return 'None'




# Distance

def calculate_dist(point1, point2):

    dist = sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2 + (point1[2]-point2[2])**2)

    return dist


def calculate(lnd_list):
    hand_map = ''
    finger_idx = [2, 4, 5, 8, 9, 12, 13, 16, 17, 20]
    cnt = 0

    for i in range(0, 5):
        dist1 = calculate_dist(lnd_list[0], lnd_list[finger_idx[cnt]])
        dist2 = calculate_dist(lnd_list[0], lnd_list[finger_idx[cnt+1]])

        print(dist1)
        print(dist2)

        # bent
        if dist1 > dist2:
            hand_map += str(1)
        elif dist1 < dist2:
            hand_map += str(0)
        cnt += 2

    return hand_map

