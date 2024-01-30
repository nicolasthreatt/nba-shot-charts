from enum import IntEnum

class CourtDimensions(IntEnum):
    CORNER3_Y = 90
    CORNER3_X = 220
    OUTER_PAINT = 80
    INNER_PAINT = 60
    FREE_THROW_LINE  = 142.5
    SIDE_BOUNDARY = 250
    FRONTCOURT_BOUNDARY = -47.5
    BACKBOARD = -30
    DEEP3_Y = 300
    DEEP3_X = 100
    RIGHT_WING_3 = 125
    HALFCOURT_BOUNDARY = 422.5
    RADIUS_3ARC = ((238-90)/2) + (440**2)/(8*(238-90))
