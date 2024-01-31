from collections import defaultdict
import unittest
from typing import List
from py2neo import Graph as NeoGraph, Node, Relationship

class Graph:
    def __init__(self):
        """ Undirected graph implementation"""
        self._graph = defaultdict(set)
    
    def add_connection(self, key1: str, key2: str) -> None:
        self._graph[key1].add(key2)
        self._graph[key2].add(key1)
    
    def add_node(self, key) -> None:
        self._graph[key] = set()
    
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
    
    def search(self, start: str, condition: callable, algorithm: str = 'DFS') -> List[str]:
        assert algorithm in ('DFS', 'BFS')
        if algorithm == 'DFS':
            return self.DFS(start, condition)
        else:
            return self.BFS(start, condition)

    def DFS(self, start: str, condition: callable = lambda x: True, max_depth: int = -1) -> List[str]:
        visited = set()
        stack = [(start, 0)]
        result = []
        while stack:
            node, depth = stack.pop()
            if node not in visited and (max_depth == -1 or depth <= max_depth):
                visited.add(node)
                if condition(node):
                    result.append((node, depth))
                stack.extend((neighbour, depth + 1) for neighbour in self._graph[node])
        return result

    def BFS(self, start: str, condition: callable = lambda x: True, max_depth: int = -1) -> List[str]:
        print(self)
        visited = set()
        queue = [(start, 0)]  
        result = []
        while queue:
            node, depth = queue.pop(0) 
            if node not in visited:
                visited.add(node)
                if condition(node):
                    result.append((node, depth))
                if max_depth == -1 or depth < max_depth:  
                    queue.extend((neighbour, depth + 1) for neighbour in self._graph[node])
        return result
    
    def __str__(self) -> str:
        return '\n'.join(f"{node}: {', '.join(connections)}" for node, connections in self._graph.items())
    
    def save_to_neo4j(self, uri: str="bolt://localhost:7687", user: str="neo4j", password: str="123456789") -> None:
        neo_graph = NeoGraph(uri, auth=(user, password))

        neo_graph.delete_all()

        neo_nodes = {}

        for node in self._graph:
            neo_nodes[node] = Node("GraphNode", name=node)
            neo_graph.create(neo_nodes[node])

        for node, connections in self._graph.items():
            for connection in connections:
                relationship = Relationship(neo_nodes[node], "CONNECTED_TO", neo_nodes[connection])
                neo_graph.create(relationship)


class TestGraph(unittest.TestCase):
    def test_add_connection(self):
        graph = Graph()
        graph.add_connection('A', 'B')
        self.assertTrue('B' in graph._graph['A'])
        self.assertTrue('A' in graph._graph['B'])

    def test_add_node(self):
        graph = Graph()
        node = 'A'
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
    
    def test_bfs_depth(self):
        graph = Graph()
        graph.add_connection('A', 'B')
        graph.add_connection('A', 'C')
        graph.add_connection('B', 'D')
        graph.add_connection('B', 'E')
        graph.add_connection('C', 'F')
        graph.add_connection('C', 'G')
        graph.add_connection('D', 'H')
        graph.add_connection('E', 'I')
        graph.add_connection('F', 'J')
        graph.add_connection('G', 'K')

        # Test BFS with max depth 3
        result = graph.BFS('A', max_depth=3)
        self.assertEqual(result, [('A', 0), ('B', 1), ('C', 1), ('D', 2), ('E', 2), ('F', 2), ('G', 2)])

        # Test BFS with max depth 4
        result = graph.BFS('A', max_depth=4)
        self.assertEqual(result, [('A', 0), ('B', 1), ('C', 1), ('D', 2), ('E', 2), ('F', 2), ('G', 2), ('H', 3), ('I', 3), ('J', 3), ('K', 3)])

        # Test BFS with max depth 5
        result = graph.BFS('A', max_depth=5)
        self.assertEqual(result, [('A', 0), ('B', 1), ('C', 1), ('D', 2), ('E', 2), ('F', 2), ('G', 2), ('H', 3), ('I', 3), ('J', 3), ('K', 3)])

        # Test BFS with max depth 6
        result = graph.BFS('A', max_depth=6)
        self.assertEqual(result, [('A', 0), ('B', 1), ('C', 1), ('D', 2), ('E', 2), ('F', 2), ('G', 2), ('H', 3), ('I', 3), ('J', 3), ('K', 3)])

if __name__ == '__main__':
    unittest.main()


