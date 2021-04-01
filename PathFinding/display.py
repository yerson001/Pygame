import pygame as pg
import random

class Display:
    def __init__(self, cols, rows, cellw):
        self.columns, self.rows = cols, rows
        self.cellw = cellw
        self.width, self.height = size = cols*cellw+1, rows*cellw+1

        self.grid = {}
        self.inicio, self.objetivo = (0, 0), (cols - 1, rows - 1)

        pg.init()
        self.screen = pg.display.set_mode(size)
        pg.display.set_caption('Pathfinding Algorithms')
        self.clock = pg.time.Clock()

        # colors
        self.c_bg = (0,0,0)
        self.c_fg = (200,200,200)
        self.c_walls = (100, 100, 100)
        self.c_inicio = (0, 200, 0)
        self.c_objetivo = (200, 0, 0)
        self.cg_inicio = (200, 50, 0)
        self.cg_end = (0, 50, 200)
        self.c_path = (20, 20, 20)

        self.running = True

    def make_grid(self, rndwalls=True, weight=False):
        self.create_empty_grid()
        if rndwalls:
            self.random_walls()
        self.create_walls(weight=weight)
        return self.grid, self.inicio, self.objetivo

    def reset_grid(self, weight=False):
        for pos in self.grid:
            w = self.grid[pos][2]
            self.grid[pos] = (0, None, w)
        self.screen.fill(self.c_bg)
        self.draw_grid(walls=True, weight=weight)

    def draw_grid(self, walls=False, weight=False):
        cellw = self.cellw
        sx, sy = self.inicio
        tx, ty = self.objetivo
        font = pg.font.SysFont(None, 12)

        for col in range(self.columns):
            for row in range(self.rows):
                if walls and (col, row) not in self.grid:
                    pg.draw.rect(self.screen, self.c_walls, (col * cellw, row * cellw, cellw, cellw))
                if weight and (col, row) in self.grid:
                    text = font.render(str(self.grid[(col, row)][2]), True, self.c_fg)
                    text_rect = text.get_rect()
                    text_rect.center = (col * cellw + cellw // 2, row * cellw + cellw // 2)
                    self.screen.blit(text, text_rect)

        pg.draw.circle(self.screen, self.c_inicio, (sx*cellw + cellw//2, sy*cellw + cellw//2), int(cellw*0.3))
        pg.draw.circle(self.screen, self.c_objetivo, (tx * cellw + cellw // 2, ty * cellw + cellw // 2), int(cellw * 0.3))

        for col in range(self.columns + 1):
            pg.draw.line(self.screen, self.c_fg, (col*cellw, 0), (col*cellw, self.width), 1)
        for row in range(self.rows + 1):
            pg.draw.line(self.screen, self.c_fg, (0, row * cellw), (self.height, row * cellw), 1)

    def create_empty_grid(self):
        # grid[(x,y)] = (distance, parent, weight)
        for x in range(self.columns):
            for y in range(self.rows):
                self.grid[(x,y)] = (0, None, random.randrange(1, 6))

    def random_walls(self):
        cols, rows = self.columns, self.rows
        directions = [(1,0), (0,1), (-1,0), (0,-1)]
        while len(self.grid)/(cols * rows) > 0.85:
            x, y = random.randrange(cols), random.randrange(rows)
            length = random.randrange(1, (cols * rows)**0.5 // 2 )
            d = random.randrange(4)
            for i in range(length):
                x += directions[d][0]
                y += directions[d][1]
                if (x, y) in self.grid and not (x,y) in (self.inicio, self.objetivo):
                    del self.grid[(x, y)]

    def create_walls(self, weight=False):
        cellw = self.cellw
        inicio = loop = True
        while loop:
            self.screen.fill(self.c_bg)
            mpos = pg.mouse.get_pos()
            pos = mpos[0] // cellw, mpos[1] // cellw

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    loop = False

                if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_MIDDLE:
                    if pos in self.grid:
                        if inicio:
                            self.inicio = pos
                        else:
                            self.objetivo = pos
                        inicio = not inicio

            if pg.mouse.get_pressed()[0]:
                if pos in self.grid and pos not in (self.inicio, self.objetivo):
                    del self.grid[pos]
            if pg.mouse.get_pressed()[2]:
                if pos not in self.grid:
                    self.grid[pos] = (0, None, random.randrange(1,6))

            self.draw_grid(walls=True, weight=weight)

            pg.display.update()

    def draw_visited(self, visited, distance=False):
        cellw = self.cellw
        max_d = max([d for d ,_ ,_ in self.grid.values()])
        i = 0
        font = pg.font.SysFont(None, 14, bold=True)
        while self.quit_loop():
            x, y = visited[i]
            d, _, _ = self.grid[(x, y)]
            color = self.get_color(d, max_d)
            pg.draw.rect(self.screen, color, (x * cellw, y * cellw, cellw, cellw))

            if distance:
                text = font.render(str(d), True, self.c_fg)
                text_rect = text.get_rect()
                text_rect.center = (x * cellw + cellw//2, y * cellw + cellw//2)
                self.screen.blit(text, text_rect)

            self.draw_grid()

            i = min(i + 1, len(visited) - 1)
            pg.display.update()
            self.clock.tick(30)

    def draw_path(self, path):
        cellw = self.cellw
        i = 0
        while self.quit_loop():
            x, y = path[i]
            pg.draw.circle(self.screen, self.c_path, (x*cellw + cellw//2, y*cellw+cellw//2), int(cellw*0.15))

            i = min(i+1, len(path)-1)
            pg.display.update()
            self.clock.tick(10)

    def quit_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return False
        return True

    def get_color(self, d, max_d):
        csr, csg, csb = self.cg_inicio
        cer, ceg, ceb = self.cg_end
        if max_d > 0:
            cr = abs(csr - d * (csr - cer) // max_d)
            cg = abs(csg - d * (csg - ceg) // max_d)
            cb = abs(csb - d * (csb - ceb) // max_d)
            return cr, cg, cb

        return self.cg_inicio

