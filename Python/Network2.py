
"""
Node syntax:

    OPP : CONNECT TO
    ----------------
    (-) : CLOSEST
    (+) : FURTHEST
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

    : C+B+A+D

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

    D|(C-A-B)+E-G|F

"""


from typing import *


__all__ = 'Node',


_T_OPP_S = Union['Node', List['Node'], Tuple['Node', ...]]
_T_OPP_R = Tuple['Node', ...]


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

    def __lshift__(self, other: 'Node') -> 'Node':
        self.connections.add(other)
        other.connections.add(self)
        return self

    def __add__(self, other: _T_OPP_S) -> _T_OPP_R:
        if isinstance(other, self.__class__):
            self << other
            return self, other
        else:
            self << other[-1]
            return (self,) + other

    def __radd__(self, other: _T_OPP_S) -> _T_OPP_R:
        if isinstance(other, self.__class__):
            self << other
            return other, self
        else:
            self << other[0]
            return other + (self,)

    def __sub__(self, other: _T_OPP_S) -> _T_OPP_R:
        if isinstance(other, self.__class__):
            self << other
            return self, other
        else:
            self << other[0]
            return (self,) + other

    def __rsub__(self, other: _T_OPP_S) -> _T_OPP_R:
        if isinstance(other, self.__class__):
            self << other
            return other, self
        else:
            self << other[-1]
            return other + (self,)

    def __or__(self, other: _T_OPP_S) -> _T_OPP_R:
        if isinstance(other, self.__class__):
            self << other
            return self, other
        else:
            self << other[0] << other[-1]
            return (self,) + other

    def __ror__(self, other: _T_OPP_S) -> _T_OPP_R:
        if isinstance(other, self.__class__):
            self << other
            return other, self
        else:
            self << other[0] << other[-1]
            return other + (self,)

    def __mul__(self, other: _T_OPP_S) -> _T_OPP_R:
        if isinstance(other, self.__class__):
            self << other
            return self, other
        else:
            for n in other:
                self << n
            return (self,) + other

    def __rmul__(self, other: _T_OPP_S) -> _T_OPP_R:
        if isinstance(other, self.__class__):
            self << other
            return self, other
        else:
            for n in other:
                self << n
            return other + (self,)

    def get_network(self) -> Set['Node']:
        """
        Returns all nodes in the network.

        :return:
            Set of all nodes in the network.
        """

        def recurse(cl, _a=set()):
            _a |= cl
            nl = {c for n in cl for c in n.connections} - _a
            return recurse(nl) if nl else _a

        return recurse({self})

    def get_network_propagation(self):
        """
        Returns all nodes in the network ordered by distance from self.

        :return:
             List of sets, where each set represents another connection
             level moving away from self.
        """

        def recurse(cl, _a=set()):
            _a |= cl
            nl = {c for n in cl for c in n.connections} - _a
            return (cl,) + recurse(nl) if nl else (cl,)

        return recurse({self})


if __name__ == '__main__':

    N = Node

    a, b, c, d = N('A') - N('B') - N('C') - N('D')

    # for n in a.get_network_propagation():
    #     print(n)

    # for n in a.get_network():
    #     print(n, n.connections)

    # for n in N('A')-N('B')-N('C'):
    #     print(n, n.connections)
    #
    # print('')
    # for n in N('A')-(N('B')-N('C')):
    #     print(n, n.connections)
    #
    # print('')
    # for n in N('A')+N('B')+N('C'):
    #     print(n, n.connections)
    #
    # print('')
    # for n in N('A')+(N('B')+N('C')):
    #     print(n, n.connections)
    #
    # print('')
    # for n in N('A')-(N('B'), N('C'), N('D')):
    #     print(n, n.connections)
