from display import Display
from search import Search

d = Display(55,55,20)
grid, inicio, objetivo = d.make_grid(weight=True)

# inicio_ = (0,0)
# grilla = grid

s = Search(grid,inicio, objetivo)
print(s)
# print("*******************************")
d.reset_grid()
visited = s.BFS()
# print(visited)
path = s.make_path()
# print("+++++++++++++++++++++++++++")
print(path)
d.draw_visited(visited, distance=True)
d.draw_path(path)



