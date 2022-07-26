"""
Tests the difference in compute time between comparing str and int
"""


from timeit import timeit


def a():
    return 'thing' == 'thing'

def b():
    return 1 == 1


def main():
    print(timeit(a, number=100000000))
    print(timeit(b, number=100000000))


if __name__ == '__main__':
    main()
