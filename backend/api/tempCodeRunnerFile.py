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