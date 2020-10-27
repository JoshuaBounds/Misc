"""
Network syntax:

    OOO : OPP : CONNECT TO
    ----------------------------
    1   : (-) : CLOSEST
    1   : (+) : FURTHEST
    2   : (&) : NOTHING
    3   : (^) : CLOSEST AND FURTHEST
    4   : (|) : ALL

"""


from itertools import *
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

    def __lshift__(self, other: 'Node') -> 'Node':
        self.connections.add(other)
        other.connections.add(self)
        return self


class NodeContainer:

    _nodes: Tuple[Node] = None

    def __init__(self, others: Iterable[Any]):
        ts = (
            [other]
            if isinstance(other, Node) else
            other.nodes
            if isinstance(other, self.__class__) else
            [Node(other)]
            for other in others
        )
        self._nodes = tuple(n for t in ts for n in t)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        nodes = ', '.join(repr(n.data) for n in self._nodes)
        return 'Network(' + nodes + ')'

    def extend(self, others: Iterable['NodeContainer']) -> NoReturn:
        """
        Extends the network using nodes from given networks.

        :param others:
            Networks from which nodes will be gathered from and then
            added to this network.
        """
        nodes = (
            n
            for t in others
            if isinstance(t, self.__class__)
            for n in t.nodes
        )
        self._nodes += tuple(nodes)

    def combine(self, others: Iterable['NodeContainer']) -> 'NodeContainer':
        return self.__class__(chain([self], others))

    def connect_inside(self, other: 'NodeContainer') -> NoReturn:
        if self.nodes and other.nodes:
            self.nodes[-1] << other.nodes[0]

    def connect_outside(self, other: 'NodeContainer') -> NoReturn:
        if self.nodes and other.nodes:
            self.nodes[0] << other.nodes[-1]

    def connect_all(self, other: 'NodeContainer') -> NoReturn:
        for node_a in self.nodes:
            for node_b in other.nodes:
                node_a << node_b

    def connect_both_sides(self, other: 'NodeContainer') -> NoReturn:
        if self.nodes and other.nodes:
            self.nodes[-1] << other.nodes[0]
            self.nodes[0] << other.nodes[-1]

    def __sub__(self, other):
        self.connect_inside(other)
        return self.combine([other])

    def __add__(self, other):
        self.connect_outside(other)
        return self.combine([other])

    def __mul__(self, other):
        self.connect_all(other)
        return self.combine([other])

    def __xor__(self, other):
        self.connect_both_sides(other)
        return self.combine([other])

    def __or__(self, other):
        return self.combine([other])

    def __isub__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_inside(other)
        self.extend([other])
        return self

    def __iadd__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_outside(other)
        self.extend([other])
        return self

    def __imul__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_all(other)
        self.extend([other])
        return self

    def __ixor__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_both_sides(other)
        self.extend([other])
        return self

    def __ior__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.extend([other])
        return self

    @property
    def nodes(self) -> Tuple[Node]:
        return self._nodes

    def clear_connections(self) -> NoReturn:
        for n in self._nodes:
            n.connections.clear()

    def print_connections(self):
        lines = (
            str(node) + ' -> ' + ', '.join(map(str, node.connections))
            for node in self._nodes
        )
        print('\n'.join(lines))


if __name__ == '__main__':

    A, B, C, D, E, F, G, H = map(NodeContainer, 'ABCDEFGH')

    # A-B
    # |/
    # C
    N = A-B ^ C
    print('')
    N.print_connections()
    N.clear_connections()

    # A-B
    # | |
    # C-D
    N = A-B-C ^ D
    print('')
    N.print_connections()
    N.clear_connections()

    # A-B
    # |/|
    # C-D
    N = B-A ^ C ^ D
    print('')
    N.print_connections()
    N.clear_connections()

    # A-B
    # |X|
    # C-D
    N = (B-A ^ C) * D
    print('')
    N.print_connections()
    N.clear_connections()

    # A-B-C
    # | | |
    # D-E-F
    N = B-A-D ^ E ^ F-C
    print('')
    N.print_connections()
    N.clear_connections()

    # A-B
    # | |
    # C-D-E
    #   | |
    #   F-G
    N = (D ^ B-A-C) + E-G ^ F
    print('')
    N.print_connections()
    N.clear_connections()

    #   A
    #  /|\
    # B C D
    #  \|/
    #   E
    N = (A | E) * (B | C | D)
    print('')
    N.print_connections()
    N.clear_connections()

    #   A
    #  /|\
    # B C D
    # | | |
    # E F G
    #  \|/
    #   H
    # N = B-E & C-F & D-G
    N = A-B-E + C-F
    print('')
    N.print_connections()
    N.clear_connections()
