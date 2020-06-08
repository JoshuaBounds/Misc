from typing import *


class Node:

    data: Any = None
    connections: Set = None

    def __init__(self, data=None):
        super(Node, self).__init__()
        self.data = data
        self.connections = set()

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

    def __gt__(self, other: 'Node') -> 'Node':
        other.connections.add(self)
        return other

    def __lt__(self, other: 'Node') -> 'Node':
        self.connections.add(other)
        return other

    def __mul__(self, other: 'Node') -> 'Node':
        self.connections.add(other)
        other.connections.add(self)
        return other

    def __rmul__(self, other: 'Node') -> 'Node':
        self.connections.add(other)
        other.connections.add(self)
        return self

    def __lshift__(self, other: Iterable['Node']) -> Iterable['Node']:
        for node in other:
            self.connections.add(node)
        return other

    def __rlshift__(self, other: Iterable['Node']) -> 'Node':
        for node in other:
            node.connections.add(self)
        return self

    def __rshift__(self, other: Iterable['Node']) -> Iterable['Node']:
        for node in other:
            node.connections.add(self)
        return other

    def __rrshift__(self, other: Iterable['Node']) -> 'Node':
        for node in other:
            self.connections.add(node)
        return self

    def __pow__(self, other: Iterable['Node']) -> Iterable['Node']:
        for node in other:
            self.connections.add(node)
            node.connections.add(self)
        return other

    def __rpow__(self, other: Iterable['Node']) -> 'Node':
        for node in other:
            self.connections.add(node)
            node.connections.add(self)
        return self

    def __call__(self, data: Any, *connections: 'Node') -> 'Node':
        return (
            connections and connections ** self.__class__(data)
            or self * self.__class__(data)
        )

    def generate_route_spread_levels(self) -> List[Set]:
        """
        :return:
            Sets of nodes ordered by distance from `self`
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
    d = a('B')('C')('D')
    a('E', d)

    print(a.generate_route_spread_levels())