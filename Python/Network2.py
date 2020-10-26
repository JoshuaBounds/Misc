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

    def __sub__(self, other: 'NodeContainer') -> 'NodeContainer':
        if self._nodes and other._nodes:
            self._nodes[-1] << other._nodes[0]
        return self.__class__(*self._nodes + other._nodes)

    def __add__(self, other: 'NodeContainer') -> 'NodeContainer':
        if self._nodes and other._nodes:
            self._nodes[0] << other._nodes[-1]
        return self.__class__(*self._nodes + other._nodes)

    def __mul__(self, other: 'NodeContainer') -> 'NodeContainer':
        for node_a in self._nodes:
            for node_b in other._nodes:
                node_a << node_b
        return self.__class__(*self._nodes + other._nodes)

    def __xor__(self, other: 'NodeContainer') -> 'NodeContainer':
        if self._nodes and other._nodes:
            self._nodes[-1] << other._nodes[0]
            self._nodes[0] << other._nodes[-1]
        return self.__class__(*self._nodes + other._nodes)

    def __or__(self, other: 'NodeContainer') -> 'NodeContainer':
        return self.__class__(*self._nodes + other._nodes)

    def __isub__(self, other: 'NodeContainer') -> 'NodeContainer':
        if self._nodes and other._nodes:
            self._nodes[-1] << other._nodes[0]
        self._nodes += other._nodes
        return self

    def __iadd__(self, other: 'NodeContainer') -> 'NodeContainer':
        if self._nodes and other._nodes:
            self._nodes[0] << other._nodes[-1]
        self._nodes += other._nodes
        return self

    def __imul__(self, other: 'NodeContainer') -> 'NodeContainer':
        for node_a in self._nodes:
            for node_b in other._nodes:
                node_a << node_b
        self._nodes += other._nodes
        return self

    def __ixor__(self, other: 'NodeContainer') -> 'NodeContainer':
        if self._nodes and other._nodes:
            self._nodes[-1] << other._nodes[0]
            self._nodes[0] << other._nodes[-1]
        self._nodes += other._nodes
        return self

    def __ior__(self, other: 'NodeContainer') -> 'NodeContainer':
        self._nodes += other._nodes
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
    N = A-B-E+C-F
    print('')
    N.print_connections()
    N.clear_connections()
