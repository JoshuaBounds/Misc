
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

    def get_connection_island(self) -> Set['Node']:
        """
        Gets all nodes that share the same connection island with self.

        A connection island is a group of nodes that are connected so
        that a path can be drawn from any one node to another, including
        passing through other nodes.
        :return:
            Set of nodes sharing the same connection island with self.
        """

        collector = {self}
        new_nodes = [self]
        while new_nodes:
            new_nodes[:] = (
                c for n in new_nodes for c in n.connections
                if c not in collector
            )
            collector.update(new_nodes)

        return collector

    def get_connection_propagation(self):
        """
        Gets propagation levels moving away from self.

        Returns a tuple of sets where each set contains nodes that all
        share the same connection distance away from self. The index of
        each set in the return tuple represents the connection distance.
        :return:
            Tuple of sets that represent the connection propagation from
            self.
        """

        levels = []
        collector = {self}
        next_level = {self}
        while next_level:
            levels.append(next_level)
            next_level = {
                c for n in next_level for c in n.connections
                if c not in collector
            }
            collector.update(next_level)

        return levels

    def find_path(self, node: 'Node') -> Union[List['Node'], None]:
        """
        Finds the shortest path from self to the given node.

        Uses two point propagation method.
        :param node:
            Target node find a path towards.
        :return:
            List representing the path from self to the target node.
            Returns None if no path could be found.
        """

        # Propagates outwards from both self and the target node until
        # the covered area overlaps.
        collector_a = {self}
        collector_b = {node}
        next_nodes_a = {self}
        next_nodes_b = {node}
        levels_a = [next_nodes_a]
        levels_b = [next_nodes_b]
        while next_nodes_a or next_nodes_b:

            next_nodes_a = {
                c for n in next_nodes_a for c in n.connections
                if c not in collector_a
            }
            collector_a.update(next_nodes_a)
            levels_a.append(next_nodes_a)

            if collector_a & collector_b:
                break

            next_nodes_b = {
                c for n in next_nodes_b for c in n.connections
                if c not in collector_b
            }
            collector_b.update(next_nodes_b)
            levels_b.append(next_nodes_b)

            if collector_a & collector_b:
                break

        else:
            # If no more unique nodes could be found, signifying that no
            # path exists between self, and the target node.
            return None

        # Propagates backwards from the overlapping areas back to both
        # self, and the target node.
        epicenter = (collector_a & collector_b).pop()

        back_node = epicenter
        path_a = [back_node]
        for level in reversed(levels_a[:-1]):
            back_node = (back_node.connections & level).pop()
            path_a.append(back_node)

        back_node = epicenter
        path_b = [back_node]
        for level in reversed(levels_b[:-1]):
            back_node = (back_node.connections & level).pop()
            path_b.append(back_node)

        return path_a[:0:-1] + path_b


class NodeContainer:

    _nodes: Tuple[Node] = None

    def __init__(self, others: Iterable[Any]):
        node_containers = (
            [other]
            if isinstance(other, Node) else
            other.nodes
            if isinstance(other, self.__class__) else
            [Node(other)]
            for other in others
        )
        self._nodes = tuple(chain(*node_containers))

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        nodes = ', '.join(repr(n.data) for n in self._nodes)
        return 'Network(' + nodes + ')'

    def __sub__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_series([other])
        return self.combine([other])

    def __add__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_heads([other])
        return self.combine([other])

    def __mul__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_all([other])
        return self.combine([other])

    def __mod__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_endings([other])
        return self.combine([other])

    def __xor__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_parallel([other])
        return self.combine([other])

    def __or__(self, other: 'NodeContainer') -> 'NodeContainer':
        return self.combine([other])

    def __isub__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_series([other])
        self.extend([other])
        return self

    def __iadd__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_heads([other])
        self.extend([other])
        return self

    def __imul__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_all([other])
        self.extend([other])
        return self

    def __imod__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_endings([other])
        self.extend([other])
        return self

    def __ixor__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.connect_parallel([other])
        self.extend([other])
        return self

    def __ior__(self, other: 'NodeContainer') -> 'NodeContainer':
        self.extend([other])
        return self

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

        Can also be accessed via the (|) operator.

        :param others:
            Networks from which nodes will be gathered from and then
            added to the new network.
        """
        return self.__class__(chain([self], others))

    def connect_series(self, others: Iterable['NodeContainer']) -> NoReturn:
        """
        Creates a connection in between each network.

        Can also be accessed via the (-) operator.

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

    def connect_heads(self, others: Iterable['NodeContainer']) -> NoReturn:
        """
        Creates a connection on the outside of each network.

        Can also be accessed via the (+) operator.

        Starting with self, then followed by each given network:
        Connects the first node of the current network to the first node
        of the next network.
        :param others:
            Node networks that should contain at least one node, but is
            not required.
        """
        ts = list(chain([self], others))
        for ta, tb in zip(ts[::2], ts[1::2]):
            if ta.nodes and tb.nodes:
                ta.nodes[0].connect(tb.nodes[0])

    def connect_all(self, others: Iterable['NodeContainer']) -> NoReturn:
        """
        Creates connections between every node in bordering networks.

        Can also be accessed via the (*) operator.

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

    def connect_parallel(self, others: Iterable['NodeContainer']) -> NoReturn:
        """
        Creates connections between network heads and tails.

        Can also be accessed via the (^) operator.

        Starting with self, then followed by each given network:
        Connects the first node of the current network to the first node
        of the next network. Then connects the last node of the current
        network to the last node of the next network.
        :param others:
            Node networks that should contain at least one node, but is
            not required.
        """
        ts = list(chain([self], others))
        for ta, tb in zip(ts[::2], ts[1::2]):
            if ta.nodes and tb.nodes:
                ta.nodes[0].connect(tb.nodes[0])
                ta.nodes[-1].connect(tb.nodes[-1])

    def connect_endings(self, others: Iterable['NodeContainer']) -> NoReturn:
        """
        Creates connections between ending nodes in bordering networks.

        Can also be accessed via the (%) operator.

        An ending node is any node that has less than two connections.
        Starting with self, then followed by each given network:
        Connects every ending node of the current network to every
        ending node of the next network.
        :param others:
            Node networks that should contain at least one node, but is
            not required.
        """
        ts = list(chain([self], others))
        tails = [[n for n in t.nodes if len(n.connections) < 2] for t in ts]
        for ta, tb in zip(tails[::2], tails[1::2]):
            for a, b in product(ta, tb):
                a.connect(b)

    @property
    def nodes(self) -> Tuple[Node]:
        return self._nodes

    @property
    def node(self) -> Node:
        return self._nodes and self._nodes[0] or None


def clear_connections(network) -> NoReturn:
    """
    Clears all connections between all nodes in the network.
    """
    for n in network.nodes:
        n.connections.clear()


def print_connections(network):
    """
    Prints out connections for each node in the network.
    """
    lines = (
        str(node) + ' -> ' + ', '.join(map(str, node.connections))
        for node in network.nodes
    )
    print('\n'.join(lines))


def print_all_paths(network):
    root, others = network.nodes[0], network.nodes[1:]
    for node in others:
        pprint(root.find_path(node))


if __name__ == '__main__':

    from pprint import pprint

    A, B, C, D, E, F, G, H, I, J = map(NodeContainer, 'ABCDEFGHIJ')

    #   A
    #  /|\
    # B D F
    # | | |
    # C E G
    #  \|/
    #   H
    N = (A-B-C + D-E + F-G) % H
    print('')
    print_connections(N)
    pprint(A.node.find_path(H.node))
    clear_connections(N)

    # A-B
    # |/
    # C
    N = A-B ^ C
    print('')
    print_connections(N)
    pprint(A.node.find_path(B.node))
    clear_connections(N)

    # A-B
    # | |
    # D-C
    N = A-B-C ^ D
    print('')
    print_connections(N)
    pprint(A.node.find_path(C.node))
    pprint(A.node.find_path(C.node))
    pprint(A.node.find_path(C.node))
    clear_connections(N)

    # A-B
    # |\|
    # C-D
    N = (A-B + C) * D
    print('')
    print_connections(N)
    pprint(A.node.find_path(B.node))
    pprint(A.node.find_path(C.node))
    pprint(A.node.find_path(D.node))
    clear_connections(N)

    # A-B
    # |X|
    # D-C
    N = (A-B ^ C) * D
    print('')
    print_connections(N)
    pprint(A.node.find_path(C.node))
    pprint(A.node.find_path(B.node))
    pprint(A.node.find_path(D.node))
    clear_connections(N)

    # B-A-E
    # | | |
    # C-D-F
    N = A-B-C ^ D ^ E-F
    print('')
    print_connections(N)
    pprint(B.node.find_path(A.node))
    pprint(B.node.find_path(C.node))
    pprint(B.node.find_path(D.node))
    pprint(B.node.find_path(E.node))
    pprint(B.node.find_path(F.node))
    clear_connections(N)

    # C-B
    # | |
    # D-A-E
    #   | |
    #   G-F
    N = (A ^ B-C-D) + E-F ^ G
    print('')
    print_connections(N)
    pprint(C.node.find_path(B.node))
    pprint(C.node.find_path(D.node))
    pprint(C.node.find_path(A.node))
    pprint(C.node.find_path(E.node))
    pprint(C.node.find_path(G.node))
    pprint(C.node.find_path(F.node))
    clear_connections(N)

    #   A
    #  /|\
    # C D E
    #  \|/
    #   B
    N = (A | B) * (C | D | E)
    print('')
    print_connections(N)
    clear_connections(N)

    #   A
    #  /|\
    # B D F
    # | | |
    # C E G
    #  \|/
    #   H
    N = A-B-C + D-E + F-G % H
    print('')
    print_connections(N)
    clear_connections(N)

    #     A---H-I
    #    / \   \
    #   B   E   J
    #  /|  /|
    # C D F G
    N = A - (B-C + D) + (E-F + G) + (H-I + J)
    print('')
    print_connections(N)
    pprint(A.node.find_path(G.node))
    clear_connections(N)
