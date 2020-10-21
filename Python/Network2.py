"""
Network syntax:

    OPP : CONNECT TO
    ----------------
    (-) : CLOSEST
    (+) : FURTHEST
    (^) : CLOSEST AND FURTHEST
    (|) : ALL

Examples:

    A-B
    |
    C

    : C-A-B

    A-B
    |/
    C

    : A-B^C

    A-B
    |/|
    C-D

    : B-A^C^D

      A
      |
    B-C-D

    : C+B+A+D

    A-B
    |X|
    C-D

    : A-B^C|D

    A-B-C
    | | |
    D-E-F

    B-A-D^E-F^C

    A-B
    | |
    C-D-E
      | |
      F-G

    D^(C-A-B)+E-G^F

      A
     /|\
    B C D
     \|/
      E

    ?

"""


from typing import *


__all__ = 'Node',


class Node:

    data: Any = None
    connections: Set['Node'] = None

    def __init__(self, data: Any = None):
        self.data = data
        self.connections = set()

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return f'Node(' + repr(self.data) + ')'

    def __sub__(self, other: 'Node') -> 'Node':
        self.connections.add(other)
        other.connections.add(self)
        return self


class Network:

    _nodes: Tuple[Node] = None

    def __init__(self, *others: Any):
        self._nodes = tuple(
            other if isinstance(other, Node) else Node(other)
            for other in others
        )

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        nodes = ', '.join(repr(n.data) for n in self._nodes)
        return 'Network(' + nodes + ')'

    def __sub__(self, other: 'Network') -> 'Network':
        if self._nodes and other._nodes:
            self._nodes[-1] - other._nodes[0]
        return self.__class__(*self._nodes + other._nodes)

    def __add__(self, other: 'Network') -> 'Network':
        if self._nodes and other._nodes:
            self._nodes[0] - other._nodes[-1]
        return self.__class__(*self._nodes + other._nodes)

    def __xor__(self, other: 'Network') -> 'Network':
        if self._nodes and other._nodes:
            self._nodes[-1] - other._nodes[0]
            self._nodes[0] - other._nodes[-1]
        return self.__class__(*self._nodes + other._nodes)

    def __or__(self, other: 'Network') -> 'Network':
        for node_a in self._nodes:
            for node_b in other._nodes:
                node_a - node_b
        return self.__class__(*self._nodes + other._nodes)

    def __isub__(self, other: 'Network') -> 'Network':
        if self._nodes and other._nodes:
            self._nodes[-1] - other._nodes[0]
        self._nodes += other._nodes
        return self

    def __iadd__(self, other: 'Network') -> 'Network':
        if self._nodes and other._nodes:
            self._nodes[0] - other._nodes[-1]
        self._nodes += other._nodes
        return self

    def __ixor__(self, other: 'Network') -> 'Network':
        if self._nodes and other._nodes:
            self._nodes[-1] - other._nodes[0]
            self._nodes[0] - other._nodes[-1]
        self._nodes += other._nodes
        return self

    def __ior__(self, other: 'Network') -> 'Network':
        for node_a in self._nodes:
            for node_b in other._nodes:
                node_a - node_b
        self._nodes += other._nodes
        return self

    @property
    def nodes(self) -> Tuple[Node]:
        return self._nodes

    def print_connections(self) -> NoReturn:
        for n in self._nodes:
            print(str(n) + ' -> ' + ', '.join(map(str, n.connections)))


if __name__ == '__main__':

    A, B, C, D, E, F, G, H = map(Network, 'ABCDEFGH')

    # A - B
    # |   |
    # C - D
    (A - B - C ^ D).print_connections()
