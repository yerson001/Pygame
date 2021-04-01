class Search:
    def __init__(self, grid, inicio, objetivo):
        self.grid = grid
        self.inicio, self.objetivo = inicio, objetivo
        self.visited = []

    def neighbours(self, pos):
        x, y = pos
        return [(x + dx, y + dy) for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + dx, y + dy) in self.grid]

    def make_path(self):
        path = [self.objetivo]
        node = self.objetivo
        while self.grid[node][1] is not None:
            _, parent, _ = self.grid[node]
            path.append(parent)
            node = parent
        return path

    def BFS(self):
        queue = [self.inicio]
        visited = [self.inicio]
        while queue:
            node = queue.pop(0)
            if node == self.objetivo:
                print('BFS TARGET FOUND AT', node, 'DISTANCE', self.grid[node][0], 'VISITED', len(visited))
                break
            nbs = [nb for nb in self.neighbours(node) if nb not in visited]
            for nb in nbs:
                self.grid[nb] = (self.grid[node][0] + 1, node, self.grid[nb][2])
                queue.extend(nbs)
            visited.extend(nbs)
        return visited

