"""
Objects for creating and editing node networks.
"""


from typing import *


__all__ = (
    'Node'
)


class Node:
    """
    Base node for building node networks.
    """

    data: Any = None
    connections: Set = None

    def __init__(self, data=None):
        super(Node, self).__init__()
        self.data = data
        self.connections = set()

    def __str__(self):
        """
        :return:
            String representation of the node's stored data.
        """
        return str(self.data)

    def __repr__(self):
        """
        :return:
            Formal representation of the node's stored data.
        """
        return repr(self.data)

    def __gt__(self, other: 'Node') -> 'Node':
        """
        Adds a one way connection from the left node to the right node.
        :return:
            Object on the right.
        """
        self.connections.add(other)
        return other

    def __lt__(self, other: 'Node') -> 'Node':
        """
        Adds a one way connection from the right node to the left node.
        :return:
            Object on the right.
        """
        other.connections.add(self)
        return other

    def __mul__(self, other: 'Node') -> 'Node':
        """
        Adds a two way connection between both nodes.
        :return:
            Object on the right.
        """
        self.connections.add(other)
        other.connections.add(self)
        return other

    def __rmul__(self, other: 'Node') -> 'Node':
        """
        Adds a two way connection between both nodes.
        :return:
            Object on the right.
        """
        self.connections.add(other)
        other.connections.add(self)
        return self

    def __lshift__(self, other: Iterable['Node']) -> Iterable['Node']:
        """
        Adds one way connections from an iterable of nodes on the right,
        to the single node on the left.
        :return:
            Object on the right.
        """
        for node in other:
            node.connections.add(self)
        return other

    def __rlshift__(self, other: Iterable['Node']) -> 'Node':
        """
        Adds one way connections from the single node on the right,
        to an iterable of nodes on the left.
        :return:
            Object on the right.
        """
        for node in other:
            self.connections.add(node)
        return self

    def __rshift__(self, other: Iterable['Node']) -> Iterable['Node']:
        """
        Adds one way connections from the single node on the left,
        to an iterable of nodes on the right.
        :return:
            Object on the right.
        """
        for node in other:
            self.connections.add(node)
        return other

    def __rrshift__(self, other: Iterable['Node']) -> 'Node':
        """
        Adds one way connections from an iterable of nodes on the left,
        to a single node on the right.
        :return:
            Object on the right.
        """
        for node in other:
            node.connections.add(self)
        return self

    def __pow__(self, other: Iterable['Node']) -> Iterable['Node']:
        """
        Adds two way connections between a single node on the left,
        and an iterable of nodes on the right.
        :return:
            Object on the right.
        """
        for node in other:
            self.connections.add(node)
            node.connections.add(self)
        return other

    def __rpow__(self, other: Iterable['Node']) -> 'Node':
        """
        Adds two way connections between a signal node on the right,
        and an iterable of nodes on the left.
        :return:
            Object on the right.
        """
        for node in other:
            self.connections.add(node)
            node.connections.add(self)
        return self

    def __call__(
            self,
            data: Any,
            connections: Iterable['Node'] = None
    ) -> 'Node':
        """
        Created a new node with the given data, and connections.
        :param data:
            Data for the new node.
        :param connections:
            If given: New node will be have two way connections to every
            node in the given iterable.
            If not given: New node will have a two way connection to
            this node.
        :return:
            Newly created node.
        """
        return (
            connections and connections ** self.__class__(data)
            or self * self.__class__(data)
        )

    def create_two_way_connections(self, *nodes: 'Node') -> List['Node']:
        """
        Creates two way connections between neighbouring nodes in the
        given sequence.
        Equivalent to [ Node * Node * ... ].
        :return:
            All nodes connected.
        """
        previous_node = self
        result = [self]
        for node in nodes:
            previous_node = previous_node * node
            result.append(node)
        return result

    def create_two_way_connections_all(self, *nodes: 'Node') -> List['Node']:
        """
        Creates two way connections between every node in the given
        sequence.
        :return:
            All nodes connected.
        """
        connected_nodes = [self]
        for node in nodes:
            connected_nodes ** node
            connected_nodes.append(node)
        return connected_nodes

    def create_one_way_connections_left(self, *nodes: 'Node') -> List['Node']:
        """
        Creates one way connections between neighbouring nodes in the
        given sequence.
        Equivalent to: [ Node < Node < ... ]
        :return:
            All nodes connected.
        """
        previous_node = self
        result = [self]
        for node in nodes:
            previous_node = previous_node < node
            result.append(node)
        return result

    def create_one_way_connections_right(self, *nodes: 'Node') -> List['Node']:
        """
        Creates one way connections between neighbouring nodes in the
        given sequence.
        Equivalent to: [ Node > Node > ... ]
        :return:
            All nodes connected.
        """
        previous_node = self
        result = [self]
        for node in nodes:
            previous_node = previous_node > node
            result.append(node)
        return result

    def generate_spread_levels(self) -> List[Set]:
        """
        :return:
            Sets of nodes ordered by distance from this node.
            (closest -> furthest).
        """
        def recurse(nodes, _result=[], _all_connections=set()):
            _result.append(nodes)
            _all_connections |= nodes
            new_connections = {
                connection
                for node in nodes
                for connection in node.connections
            }
            new_unique_connections = new_connections - _all_connections
            return (
                new_unique_connections and recurse(new_unique_connections)
                or _result
            )
        return recurse({self})


if __name__ == '__main__':

    a = Node('A')
    b = Node('B')
    c = Node('C')

    print(a.connections)
    print(b.connections)
    print(c.connections)

    Node.create_one_way_connections_right(a, b, c)

    print(a, a.connections)
    print(b, b.connections)
    print(c, c.connections)
