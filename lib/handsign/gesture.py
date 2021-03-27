'''
Project Title : Hand gesture recognition algorithm
Author : Jang Jung iK
Last Modified : 2020.11.27
'''
from math import sqrt, acos
from math import degrees

# Define right & left hand gestures
right_gesture_dict = {'11111': "STOP",   # zero
                      '10111': "GO",    # one
                      '10011': "TURN",    # two
                      '10001': "LEFT",  # three
                      '10000': "RIGHT",   # four
                      #'00000': "five"   # five
                      }

left_gesture_dict = {'11111': "Capture",   # zero
                     '10111': "Work SR Engine",    # one
                     '10011': "Camera_LEFT",    # two
                     '10001': "Camera_RIGHT",  # three
                     '10000': "Camera_CENTER",   # four
                     '00000': "SR Done"   # five
                     }


# Check hand is left or right
def handedness(point0, point1):
    if point1[0] > point0[0]:
        return 'left'
    elif point0[0] > point1[0]:
        return 'right'


# Change 3 points to 2 vectors
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


# Normalize vector
def normalize(vec):
    len = sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])
    return [vec[0] / len, vec[1] / len, vec[2] / len]


# Dot product
def dot(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2]


# Calculate interior angle
def get_degree(vec1, vec2):
    return degrees(acos(dot(normalize(vec1), normalize(vec2))))


# Check the finger's state(bent or straight)
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


# Return five finger's state
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


# Return hand gesture command
def find_gesture(hand_map, handedness):
    try:
        if(handedness == 'right'):
            return right_gesture_dict[hand_map]
        elif (handedness == 'left'):
            return left_gesture_dict[hand_map]
    except:
        return 'None'

