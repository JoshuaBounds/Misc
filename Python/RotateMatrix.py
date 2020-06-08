
def rotate_matrix(matrix):
    return zip(*reversed(matrix))


if __name__ == '__main__':

    from pprint import pprint

    MATRIX = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]

    pprint(
        list(rotate_matrix(MATRIX)),
        width=20
    )
