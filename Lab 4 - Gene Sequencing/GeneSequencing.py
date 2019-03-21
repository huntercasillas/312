#!/usr/bin/python3

import math

# Used to compute the bandwidth for banded version
MAXINDELS = 3
# Bandwidth is calculated with (MAXINDELS * 2) + 1
BANDWIDTH = 7

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1


# Unrestricted algorithm for calculating alignment and score
# Time and space complexity are both O(nm)
# Where m is the number of rows and n is the number of columns in the matrix
def calc_unrestricted(top_sequence, side_sequence, maximum):

    # Sets the number of columns and rows
    # Will be either the length of the corresponding sequence or the align_length (maximum)
    # Whichever is smaller plus one O(1)
    columns = min(len(top_sequence), maximum) + 1
    rows = min(len(side_sequence), maximum) + 1

    # Sets the sequences (cuts off at the maximum letter/index) O(1)
    top_sequence = top_sequence[:maximum]
    side_sequence = side_sequence[:maximum]

    # Initializes the matrix of tuples with 0 for the score and "-" for its origin/source O(nm)
    matrix = [[(0, "-") for _ in range(columns)] for _ in range(rows)]

    # Set the top left corner of the matrix with the corresponding values O(1)
    matrix[0][0] = (0, "empty")

    # Sets the first row with increasing multiples of the INDEL value O(m)
    for i in range(1, rows):
        score = i * INDEL
        matrix[i][0] = (score, "top")

    # Sets the first column with increasing multiples of the INDEL value O(n)
    for j in range(1, columns):
        score = j * INDEL
        matrix[0][j] = (score, "side")

    # Total time and space complexity is O(nm)
    # O(m) where m is the number of letters in the side sequence
    for i in range(1, rows):
        # O(n) where n is the number of letters in the top sequence
        for j in range(1, columns):
            # Top, side, and corner positions in the matrix relative to matrix[i][j] O(1)
            top = matrix[i - 1][j]
            side = matrix[i][j - 1]
            corner = matrix[i - 1][j - 1]
            # Current letters in the sequences O(1)
            side_letter = side_sequence[i - 1]
            top_letter = top_sequence[j - 1]

            # Check to see if the letters match O(1)
            if side_letter == top_letter:
                # If they do, update the score with the MATCH value O(1)
                score = corner[0] + MATCH
                matrix[i][j] = (score, "corner")
            else:
                # Otherwise, update the score with the SUB value O(1)
                score = corner[0] + SUB
                matrix[i][j] = (score, "corner")

            # Set the score to the correct minimum for the side position O(1)
            if side[0] + INDEL < score:
                score = side[0] + INDEL
                matrix[i][j] = (score, "side")

            # Set the score to the correct minimum for the top position O(1)
            if top[0] + INDEL < score:
                score = top[0] + INDEL
                matrix[i][j] = (score, "top")

    # Get the final alignments from the sequences O(nm)
    alignment1, alignment2 = alignment_unrestricted(top_sequence, side_sequence, matrix)
    # Get the final score from the matrix O(1)
    score = matrix[rows - 1][columns - 1][0]

    # Return the final variables O(1)
    return score, alignment1, alignment2


# Finds the character-by-character alignment of the two sequences
# Time complexity is O(nm) and space complexity is O(s) where s is the length of whichever alignment is longer
def alignment_unrestricted(top_sequence, side_sequence, matrix):

    # Get the current side and top positions in the matrix O(1)
    side = len(side_sequence)
    top = len(top_sequence)
    # Initial alignments are empty O(1)
    alignment1 = ""
    alignment2 = ""
    # The end value is 100 because we only show the first 100 characters O(1)
    end = 100

    # This while loop iterates through the entire matrix O(nm)
    while matrix[side][top][1] != "empty":
        # Set the source/origin to the second value in the tuple for the current matrix position O(1)
        origin = matrix[side][top][1]

        # Check to see if there was a match/substitution O(1)
        if origin == "corner":
            # Update the alignments O(1)
            alignment1 = top_sequence[top - 1] + alignment1
            alignment2 = side_sequence[side - 1] + alignment2
            # Decrement the top and side positions by one O(1)
            top -= 1  # O(1)
            side -= 1  # O(1)

        # Check to see if there was a deletion O(1)
        elif origin == "side":
            # Update the alignments O(1)
            alignment1 = top_sequence[top - 1] + alignment1
            alignment2 = "-" + alignment2
            # Decrement the top position by one (move over one column) O(1)
            top -= 1

        # Check to see if there was an insertion O(1)
        elif origin == "top":
            # Update the alignments O(1)
            alignment1 = "-" + alignment1
            alignment2 = side_sequence[side - 1] + alignment2
            # Decrement the side position by one (move up one row) O(1)
            side -= 1

    # Check to see if the alignment was updated or not O(1)
    if alignment1 != "":
        # Only show the first 100 characters O(1)
        alignment1 = alignment1[:end]
    # If the alignment wasn't updated, there is no alignment possible O(1)
    else:
        alignment1 = "No Alignment Possible"

    # Check to see if the alignment was updated or not O(1)
    if alignment2 != "":
        # Only show the first 100 characters O(1)
        alignment2 = alignment2[:end]
    # If the alignment wasn't updated, there is no alignment possible O(1)
    else:
        alignment2 = "No Alignment Possible"

    # Return the final correct alignments O(1)
    return alignment1, alignment2


# Banded algorithm for calculating alignment
# Time complexity and space complexity are both O(kn)
# Where k is the bandwidth constant and n is the length of the shorter sequence
def calc_banded(top_sequence, side_sequence, maximum):

    # Sets the number of columns and rows
    # Will be either the length of the corresponding sequence or the align_length (maximum)
    # Whichever is smaller plus one O(1)
    columns = min(len(top_sequence), maximum) + 1
    rows = min(len(side_sequence), maximum) + 1

    # Sets the sequences (cuts off at the maximum letter/index) O(1)
    top_sequence = top_sequence[:maximum]
    side_sequence = side_sequence[:maximum]

    # Set the infinity, initial, and difference variables O(1)
    # Initial is just a specific value I use to initialize the matrix
    # Difference is how many rows are needed to make the sequences equal lengths
    infinity = math.inf
    initial = 54321.12345
    difference = abs(len(top_sequence) - len(side_sequence))

    # Sequences with significant length discrepancies cannot be aligned O(1)
    if (columns - rows) > MAXINDELS or (columns - rows) < -MAXINDELS:
        # Set the alignments and return them with infinity as the score O(1)
        alignment1 = "No Alignment Possible"
        alignment2 = "No Alignment Possible"
        return infinity, alignment1, alignment2

    # If the top sequence is larger O(1)
    if len(top_sequence) > len(side_sequence):
        # Update the rows with the difference and swap the two sequences O(1)
        rows = len(side_sequence) + 1 + difference
        top_sequence, side_sequence = side_sequence, top_sequence
    # Otherwise, if the side sequence is larger O(1)
    else:
        # Update the rows with the difference O(1)
        rows = len(top_sequence) + 1 + difference

    # Set the columns equal to the bandwidth O(1)
    columns = BANDWIDTH

    # Initializes the matrix of tuples with my initial value for the score and "-" for its origin/source O(kn)
    # Where k is the bandwidth constant of 7
    matrix = [[(initial, "-") for _ in range(columns)] for _ in range(rows)]

    # Set the corner of the matrix with the corresponding values O(1)
    matrix[0][3] = (0, "empty")

    # Set the first row and column with increasing multiples of the INDEL value O(1)
    matrix[0][4] = (5, "side")
    matrix[0][5] = (10, "side")
    matrix[0][6] = (15, "side")
    matrix[1][2] = (5, "top")
    matrix[2][1] = (10, "top")
    matrix[3][0] = (15, "top")

    # Set the upper and lower sections to infinity for the score O(1)
    # The second value (origin) is just set to whatever it already is
    matrix[0][0] = (infinity, matrix[0][0][1])
    matrix[0][1] = (infinity, matrix[0][1][1])
    matrix[0][2] = (infinity, matrix[0][2][1])
    matrix[1][0] = (infinity, matrix[1][0][1])
    matrix[1][1] = (infinity, matrix[1][1][1])
    matrix[2][0] = (infinity, matrix[2][0][1])
    matrix[rows - 1][6] = (infinity, matrix[rows - 1][6][1])
    matrix[rows - 1][5] = (infinity, matrix[rows - 1][5][1])
    matrix[rows - 1][4] = (infinity, matrix[rows - 1][4][1])
    matrix[rows - 2][6] = (infinity, matrix[rows - 2][6][1])
    matrix[rows - 2][5] = (infinity, matrix[rows - 2][5][1])
    matrix[rows - 3][6] = (infinity, matrix[rows - 3][6][1])

    # Total time and space complexity is O(kn)
    # O(n) where n is the number of letters in the shorter sequence
    for i in range(0, rows):
        # O(k) where k is the number of columns, which is only the BANDWIDTH of 7
        for j in range(0, columns):
            # Check to see if the matrix still has the arbitrary initial value of 54321.12345 O(1)
            if matrix[i][j][0] == initial:
                # Set the current score to infinity O(1)
                score = infinity
                # Check to see where we are in the matrix and update the corresponding score values O(1)
                if j == 0:
                    # Top, side, and corner scores in the matrix relative to matrix[i][j] O(1)
                    top = matrix[i - 1][j + 1][0]
                    side = infinity
                    corner = matrix[i - 1][j][0]
                elif j == 6:
                    # Top, side, and corner scores in the matrix relative to matrix[i][j] O(1)
                    top = infinity
                    side = matrix[i][j - 1][0]
                    corner = matrix[i - 1][j][0]
                else:
                    # Top, side, and corner scores in the matrix relative to matrix[i][j] O(1)
                    top = matrix[i - 1][j + 1][0]
                    side = matrix[i][j - 1][0]
                    corner = matrix[i - 1][j][0]

                # If the corner score isn't infinity O(1)
                if corner != infinity:
                    # Set the current matrix position to infinity O(1)
                    if i - (4 - j) > len(top_sequence) - 1:
                        origin = matrix[i][j][1]
                        matrix[i][j] = (infinity, origin)
                        # Skip to the next iteration in the for loop O(1)
                        continue
                    # Otherwise, check to see if we have a match O(1)
                    else:
                        # If they do, update the score with the MATCH value O(1)
                        if top_sequence[i - (4 - j)] == side_sequence[i - 1]:
                            score = corner + MATCH  # O(1)
                            matrix[i][j] = (matrix[i][j][0], "corner")
                        # Otherwise, update the score with the SUB value O(1)
                        else:
                            score = corner + SUB  # O(1)
                            matrix[i][j] = (score, "corner")

                # If the side score isn't infinity O(1)
                if side != infinity:
                    # Set the score to the correct minimum for the side position O(1)
                    if (side + INDEL) < score:
                        score = side + INDEL
                        matrix[i][j] = (score, "side")

                # If the top score isn't infinity O(1)
                if top != infinity:
                    # Set the score to the correct minimum for the top position O(1)
                    if (top + INDEL) < score:
                        score = top + INDEL
                        matrix[i][j] = (score, "top")

                # Grab the current origin from the matrix O(1)
                origin = matrix[i][j][1]
                # Update the matrix at [i][j] with the new minimum and current origin O(1)
                matrix[i][j] = (score, origin)

    # Set the columns value back to MAXINDELS O(1)
    columns = MAXINDELS

    # Loops through the columns, which reduces to constant O(1)
    while matrix[rows - 1][columns][0] == infinity:
        columns -= 1

    # Get the final alignments from the sequences O(kn)
    alignment1, alignment2 = alignment_banded(top_sequence, side_sequence, matrix, rows, columns)
    # Get the final score from the matrix O(1)
    score = matrix[rows - 1][columns][0]

    # Return the final variables O(1)
    return score, alignment1, alignment2


# Finds the character-by-character alignment of the two sequences
# Time complexity is O(kn) and space complexity is O(s) where s is the length of whichever alignment is longer
def alignment_banded(top_sequence, side_sequence, matrix, side, top):

    # Initial alignments are empty O(1)
    alignment1 = ""
    alignment2 = ""
    # The end value is 100 because we only show the first 100 characters O(1)
    end = 100

    # This while loop iterates to (O,3) in the matrix O(kn)
    while matrix[side - 1][top][1] != "empty":
        # Set the source/origin to the second value in the tuple for the current matrix position O(1)
        origin = matrix[side - 1][top][1]

        # Check to see if there was a match/substitution O(1)
        if origin == "corner":
            # Update the alignments O(1)
            alignment1 = top_sequence[side - (4 - top) - 1] + alignment1
            alignment2 = side_sequence[side - 2] + alignment2
            # Decrement the side position by one (move up one row) O(1)
            side -= 1

        # Check to see if there was a deletion O(1)
        elif origin == "side":
            # Update the alignments O(1)
            alignment1 = top_sequence[side - (4 - top) - 1] + alignment1
            alignment2 = "-" + alignment2
            # Decrement the top position by one (move over one column) O(1)
            top -= 1

        # Check to see if there was an insertion O(1)
        elif origin == "top":
            # Update the alignments O(1)
            alignment1 = "-" + alignment1
            alignment2 = side_sequence[side - 2] + alignment2
            # Increment the top and decrement the side positions by one O(1)
            top += 1
            side -= 1

    # Check to see if the alignment was updated or not O(1)
    if alignment1 != "":
        # Only show the first 100 characters O(1)
        alignment1 = alignment1[:end]
    # If the alignment wasn't updated, there is no alignment possible O(1)
    else:
        alignment1 = "No Alignment Possible"

    # Check to see if the alignment was updated or not O(1)
    if alignment2 != "":
        # Only show the first 100 characters O(1)
        alignment2 = alignment2[:end]
    # If the alignment wasn't updated, there is no alignment possible O(1)
    else:
        alignment2 = "No Alignment Possible"

    # Return the final correct alignments O(1)
    return alignment1, alignment2


class GeneSequencing:
    def __init__(self):
        pass

    # This is the method called by the GUI.  _sequences_ is a list of the ten sequences, _table_ is a
    # handle to the GUI so it can be updated as you find results, _banded_ is a boolean that tells
    # you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
    # how many base pairs to use in computing the alignment
    def align(self, sequences, table, banded, align_length):
        self.banded = banded
        self.MaxCharactersToAlign = align_length
        results = []

        # Total time and space complexity is O(1)
        # O(10) because there are 10 rows, reduces to constant time
        for i in range(len(sequences)):
            jresults = []
            # O(10) because there are 10 columns, reduces to constant time
            for j in range(len(sequences)):
                if j < i:
                    s = {}
                else:
                    # If we have a match, just calculate the alignments and score manually O(1)
                    if i == j:
                        alignment1 = sequences[i][:align_length]
                        alignment2 = sequences[j][:align_length]
                        # The score is just the length of either alignment * -3
                        score = len(alignment1) * MATCH

                    # If we don't have a match, check to see which algorithm we will be using
                    # O(nm) for unrestricted and O(kn) for banded
                    elif self.banded:
                        score, alignment1, alignment2 = calc_banded(sequences[i], sequences[j], align_length)
                    else:
                        score, alignment1, alignment2 = calc_unrestricted(sequences[i], sequences[j], align_length)

                    alignment1 = alignment1.format(i + 1, len(sequences[i]), align_length, ',BANDED' if banded else '')
                    alignment2 = alignment2.format(j + 1, len(sequences[j]), align_length, ',BANDED' if banded else '')
                    s = {'align_cost': score, 'seqi_first100': alignment1, 'seqj_first100': alignment2}
                    table.item(i, j).setText('{}'.format(int(score) if score != math.inf else score))
                    table.repaint()
                jresults.append(s)
            results.append(jresults)
        return results
