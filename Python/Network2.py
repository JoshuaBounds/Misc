
"""
Node syntax:

    OPP : CONNECT TO
    ----------------
    (-) : CLOSEST
    (|) : CLOSEST AND FURTHEST
    (*) : ALL

Examples:

    A-B
    |
    C

    : C-A-B

    A-B
    |/
    C

    : A-B|C

    A-B
    |/|
    C-D

    : B-A|C|D

      A
      |
    B-C-D

    : (A,B,D)*C

    A-B
    |X|
    C-D

    : A-B|C*D

    A-B-C
    | | |
    D-E-F

    B-A-D|E-F|C

    A-B
    | |
    C-D-E
      | |
      F-G

    C-A-B|D-E-G-F

"""


from typing import *


__all__ = 'Node',


class Node:

    connections: Set = None
    data: Any = None

    def __init__(self, data: Any = None):
        self.data = data
        self.connections = set()

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            self.connections.add(other)
            other.connections.add(self)
            return self, other
        else:
            self.connections.add(other[0])
            other[0].connections.add(self)
            return (self,) + other

    def __rsub__(self, other):
        if isinstance(other, self.__class__):
            self.connections.add(other)
            other.connections.add(self)
            return other, self
        else:
            self.connections.add(other[0])
            other[0].connections.add(self)
            return other + (self,)
