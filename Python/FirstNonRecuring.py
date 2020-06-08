
def first_non_recurring(item):

    too_many = set()
    found = []
    for char in item:

        if char in too_many:
            continue

        if char in found:
            too_many.add(char)
            found.remove(char)
        else:
            found.append(char)

    return found


if __name__ == '__main__':

    ITEM = 'aadeefgg'

    for x in first_non_recurring(ITEM):
        print(x)
