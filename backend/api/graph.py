from collections import defaultdict
import unittest
from typing import List

class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data

class Graph:
    def __init__(self):
        """ Undirected graph implementation"""
        self._graph = defaultdict(set)
    
    def add_connection(self, key1: str, key2: str) -> None:
        self._graph[key1].add(key2)
        self._graph[key2].add(key1)
    
    def add_node(self, node: Node) -> None:
        self._graph[node.key] = set()
    
    def remove_node(self, key: str) -> None:
        if key in self._graph:
            del self._graph[key]
            for connections in self._graph.values():
                connections.discard(key)
    
    def remove_connection(self, key1: str, key2: str) -> None:
        if key1 in self._graph and key2 in self._graph:
            self._graph[key1].discard(key2)
            self._graph[key2].discard(key1)
    
    def are_connected(self, key1: str, key2: str) -> bool:
        return key2 in self._graph[key1]
    
    def get_shortest_path(start_key: str, end_key: str) -> List[str]:
        pass
    
    def __str__(self) -> str:
        return '\n'.join(f"{node}: {', '.join(connections)}" for node, connections in self._graph.items())


class TestGraph(unittest.TestCase):
    def test_add_connection(self):
        graph = Graph()
        graph.add_connection('A', 'B')
        self.assertTrue('B' in graph._graph['A'])
        self.assertTrue('A' in graph._graph['B'])

    def test_add_node(self):
        graph = Graph()
        node = Node('A', 'Data A')
        graph.add_node(node)
        self.assertTrue('A' in graph._graph)
        self.assertEqual(len(graph._graph['A']), 0)

    def test_remove_node(self):
        graph = Graph()
        graph.add_connection('A', 'B')
        graph.add_connection('B', 'C')
        graph.remove_node('B')
        self.assertNotIn('B', graph._graph)
        self.assertNotIn('B', graph._graph['A'])
        self.assertNotIn('B', graph._graph['C'])

    def test_are_connected(self):
        graph = Graph()
        graph.add_connection('A', 'B')
        graph.add_connection('B', 'C')
        self.assertTrue(graph.are_connected('A', 'B'))
        self.assertTrue(graph.are_connected('B', 'C'))
        self.assertFalse(graph.are_connected('A', 'C'))

if __name__ == '__main__':
    unittest.main()


