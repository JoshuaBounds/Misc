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

    def connect(self, other: 'Node') -> NoReturn:
        """
        Creates a connection between self and the given node.

        :param other:
            Other node to create a connection between.
        """
        self.connections.add(other)
        other.connections.add(self)

    def __lshift__(self, other):
        self.connect(other)
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
        """
        Creates a new network using nodes from self, and given networks.

        :param others:
            Networks from which nodes will be gathered from and then
            added to the new network.
        """
        return self.__class__(chain([self], others))

    def connect_inside(self, others: Iterable['NodeContainer']) -> NoReturn:
        """
        Creates a connection in between each network.

        Starting with self, then followed by each given network:
        Connects the last node of the current network to the first node
        of the next network.
        :param others:
            Node networks that should contain at least one node, but is
            not required.
        """
        ts = list(chain([self], others))
        for ta, tb in zip(ts[::2], ts[1::2]):
            if ta.nodes and tb.nodes:
                ta.nodes[-1].connect(tb.nodes[0])

    def connect_outside(self, others: Iterable['NodeContainer']) -> NoReturn:
        """
        Creates a connection on the outside of each network.

        Starting with self, then followed by each given network:
        Connects the first node of the current network to the last node
        of the next network.
        :param others:
            Node networks that should contain at least one node, but is
            not required.
        """
        ts = list(chain([self], others))
        for ta, tb in zip(ts[::2], ts[1::2]):
            if ta.nodes and tb.nodes:
                ta.nodes[0].connect(tb.nodes[-1])

    def connect_all(self, others: Iterable['NodeContainer']) -> NoReturn:
        """
        Creates connections between every node in bordering networks.

        Starting with self, then followed by each given network:
        Connects every node of the current network to every node of the
        next network.
        :param others:
            Node networks that should contain at least one node, but is
            not required.
        """
        ts = list(chain([self], others))
        for ta, tb in zip(ts[::2], ts[1::2]):
            for a, b in product(ta.nodes, tb.nodes):
                a.connect(b)

    def connect_both_sides(self, others: Iterable['NodeContainer']) -> NoReturn:
        """
        Performs both connect_inside and connect_outside.

        :param others:
            Node networks that should contain at least one node, but is
            not required.
        """
        ts = list(chain([self], others))
        for ta, tb in zip(ts[::2], ts[1::2]):
            if ta.nodes and tb.nodes:
                ta.nodes[0].connect(tb.nodes[-1])
                ta.nodes[-1].connect(tb.nodes[0])

    def connect_tails(self, others: Iterable['NodeContainer']) -> NoReturn:
        """
        Creates connections between tail nodes in bordering networks.

        A tail node is any node that has less than two connections.
        Starting with self, then followed by each given network:
        Connects every tail node of the current network to every tail
        node of the next network.
        :param others:
            Node networks that should contain at least one node, but is
            not required.
        """
        ts = list(chain([self], others))
        tails = [[n for n in t.nodes if len(n.connections) < 2] for t in ts]
        for ta, tb in zip(tails[::2], tails[1::2]):
            for a, b in product(ta, tb):
                a.connect(b)

    def __sub__(self, other):
        self.connect_inside([other])
        return self.combine([other])

    def __add__(self, other):
        self.connect_outside([other])
        return self.combine([other])

    def __mul__(self, other):
        self.connect_all([other])
        return self.combine([other])

    def __mod__(self, other):
        self.connect_tails([other])
        return self.combine([other])

    def __xor__(self, other):
        self.connect_both_sides([other])
        return self.combine([other])

    def __or__(self, other):
        return self.combine([other])

    def __isub__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_inside([other])
        self.extend([other])
        return self

    def __iadd__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_outside([other])
        self.extend([other])
        return self

    def __imul__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_all([other])
        self.extend([other])
        return self

    def __imod__(self, other):
        self.connect_tails([other])
        self.extend([other])
        return self

    def __ixor__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_both_sides([other])
        self.extend([other])
        return self

    def __ior__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.extend([other])
        return self

    @property
    def nodes(self) -> Tuple[Node]:
        return self._nodes

    def clear_connections(self) -> NoReturn:
        """
        Clears all connections between all nodes in the network.
        """
        for n in self._nodes:
            n.connections.clear()

    def print_connections(self):
        """
        Prints out connections for each node in the network.
        """
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
    N = (A-B-E + C-F + D-G) % H
    print('')
    N.print_connections()
    N.clear_connections()
