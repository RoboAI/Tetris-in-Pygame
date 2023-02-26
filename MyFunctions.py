import math

def get_angle(p1, p2):
    # Difference in x coordinates
    dx = p2[0] - p1[0]

    # Difference in y coordinates
    dy = p2[1] - p1[1]

    # Angle between p1 and p2 in radians
    theta = math.atan2(dy, -dx)
    
    #convert to degrees
    x = math.degrees(theta)

    #pygame.display.set_caption(str(x))

    return x

def get_distance(x1, y1, x2, y2):
    distance = math.sqrt(((x2 - x1) ** 2) + (y2 - y1) ** 2)
    #pygame.display.set_caption(str(distance))
    return distance

def get_distance_from_pts(p1, p2):
    return get_distance(p1[0], p1[1], p2[0], p2[1])
    