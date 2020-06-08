
from typing import Any, Hashable, Set, Tuple, Dict


class Network:

    table = {}

    def _setdefault_node(self, key):
        return self.table.setdefault(key, {'data': None, 'links': set()})

    def set_data(self, key, data=None):
        self._setdefault_node(key)['data'] = data

    def get_data(self, key):
        return self._setdefault_node(key)['data']

    def add_links(self, key, links):
        self._setdefault_node(key)['links'] |= links
        for link in links:
            self._setdefault_node(link)['links'].add(key)

    def discard_links(self, key, links):
        self._setdefault_node(key)['links'] -= links
        for link in links:
            self._setdefault_node(link)['links'].discard(key)

    def set_links(self, key, links):
        self.discard_links(key, self._setdefault_node(key)['links'] - links)
        self.add_links(key, links - self._setdefault_node(key)['links'])

    def get_links(self, key):
        return set(self._setdefault_node(key)['links'])

    def get_connection_island(self, keys):

        def recurse(links, all_links=set()):
            new_links = (
                set.union(*(self._setdefault_node(x)['links'] for x in links))
                - all_links
                - links
            )
            all_links |= new_links
            if new_links:
                return recurse(new_links)
            else:
                return all_links

        return recurse(keys)

    def get_shortest_path(self, key_a, key_b):
        pass


if __name__ == '__main__':

    network = Network()

    network.set_data('a', [1, 2, 3])
    network.set_data('b', [1, 2, 3])
    network.set_data('c', [1, 2, 3])
    network.set_data('d', [1, 2, 3])
    network.set_data('e', [1, 2, 3])

    network.add_links('a', {'b'})
    network.add_links('b', {'c'})
    network.add_links('c', {'d'})
    network.add_links('d', {'e'})

    print(network.get_connection_island({'a'}))
    print(network.get_connection_island({'a'}))
