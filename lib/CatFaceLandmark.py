class CatFaceLandmark:
    # the landmark values do not match their order in catface.py
    LEFT_EYE = 0
    RIGHT_EYE = 4
    MOUTH = 3
    LEFT_OF_LEFT_EAR = 1
    TIP_OF_LEFT_EAR = 7
    RIGHT_OF_LEFT_EAR = 5
    LEFT_OF_RIGHT_EAR = 2
    TIP_OF_RIGHT_EAR = 8
    RIGHT_OF_RIGHT_EAR = 6

    def __init__(self):
        pass

    @staticmethod
    def all():
        return [
            {
                'value': CatFaceLandmark.LEFT_EYE,
                'name': 'Left Eye'
            },
            {
                'value': CatFaceLandmark.RIGHT_EYE,
                'name': 'Right Eye'
            },
            {
                'value': CatFaceLandmark.MOUTH,
                'name': 'Mouth'
            },
            {
                'value': CatFaceLandmark.LEFT_OF_LEFT_EAR,
                'name': 'Left of Left Ear'
            },
            {
                'value': CatFaceLandmark.TIP_OF_LEFT_EAR,
                'name': 'Tip of Left Ear'
            },
            {
                'value': CatFaceLandmark.RIGHT_OF_LEFT_EAR,
                'name': 'Right of Left Ear'
            },
            {
                'value': CatFaceLandmark.LEFT_OF_RIGHT_EAR,
                'name': 'Left of Right Ear'
            },
            {
                'value': CatFaceLandmark.TIP_OF_RIGHT_EAR,
                'name': 'Tip of Right Ear'
            },
            {
                'value': CatFaceLandmark.RIGHT_OF_RIGHT_EAR,
                'name': 'Right of Right Ear'
            }
        ]
