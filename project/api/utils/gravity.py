from random import choices

from project.api.utils.metrics import timing


class Gravity:
    @staticmethod
    def _falling_rock(segment):
        """
        orders the list based on "falling_rocks" rules. Super
        slow algorithm comparable to bubble sort.
        """
        for _ in range(len(segment)):
            for i in range(len(segment) - 1):
                if segment[i] == "." and segment[i + 1] == ".":
                    segment[i], segment[i + 1] = " ", ":"
                if segment[i] == "." and segment[i + 1] == " ":
                    segment[i], segment[i + 1] = " ", "."
                if segment[i] == ":" and segment[i + 1] == " ":
                    segment[i], segment[i + 1] = " ", ":"
                if segment[i] == ":" and segment[i + 1] == ".":
                    segment[i], segment[i + 1] = ".", ":"
        return segment

    @staticmethod
    def _transpose_list(lists):
        """
        transposes a 2d array
        """
        return [list(x) for x in zip(*lists)]

    @staticmethod
    @timing
    def falling_rocks(initialState):
        # convert string into list of strings
        fState = initialState.split(",")
        # transpose list of strings into segments
        fState = Gravity._transpose_list(fState)
        # simulate "falling rock" in each segment
        fState = [Gravity._falling_rock(segment) for segment in fState]
        # transpose back into original format
        fState = [list(left) for left in zip(*fState)]
        # remove empty rows
        fState_copy = fState
        for row, _ in enumerate(fState_copy):
            if set(fState[row]) == ({" "}):
                del fState[row]
        # return as string
        return ",".join(["".join(row) for row in fState])


class RandomWorld:
    @staticmethod
    @timing
    def generate(rows, columns):
        return ["".join(choices(" .:T", k=int(columns))) for i in range(int(rows))]
