class GestureRecognizer:

    def recognize(self, fingers):

        if fingers == [0,0,0,0,0]:
            return "FIST"

        elif fingers == [1,1,1,1,1]:
            return "OPEN PALM"

        elif fingers == [0,1,0,0,0]:
            return "ONE"

        elif fingers == [0,1,1,0,0]:
            return "PEACE"

        elif fingers == [0,1,1,1,0]:
            return "THREE"

        elif fingers == [0,1,1,1,1]:
            return "FOUR"

        elif fingers == [1,0,0,0,0]:
            return "THUMBS UP"

        else:
            return "UNKNOWN"