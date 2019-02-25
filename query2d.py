import numpy as np


#store any object
#object is a tuple like (list_of_lines, something)
#line: ((x1, y1), (x2, y2))
#box: ((x1, y1), (x2, y2))

class SparseGrid:
    def __init__(self, step):
        self.step = step
        self.grid = {}

    def insert(self, item):
        for line in item[0]:
            self._insert_line(line, item[1])

    def query(self, box):
        idx_box = self._line2box(box)
        ret_dict = {}
        for x in range(idx_box[0][0], idx_box[1][0] + 1):
            for y in range(idx_box[0][1], idx_box[1][1] + 1):
                self._query((x, y), ret_dict)
        ret = []
        for key in ret_dict:
            ret.append(ret_dict[key])
        return ret

    def _insert_line(self, line, item):
        box = self._line2box(line)
        for x in range(box[0][0], box[1][0] + 1):
            for y in range(box[0][1], box[1][1] + 1):
                self._insert_point((x, y), item)

    def _insert_point(self, point, item):
        x = point[0]
        y = point[1]
        if x not in self.grid:
            self.grid[x] = {}
        if y not in self.grid[x]:
            self.grid[x][y] = list()
        self.grid[x][y].append(item)

    def _query(self, idx, ret_dict):
        if idx[0] not in self.grid:
            return
        if idx[1] not in self.grid[idx[0]]:
            return
        for item in self.grid[idx[0]][idx[1]]:
            if id(item) not in ret_dict:
                ret_dict[id(item)] = item

    def _line2box(self, line):
        linebox = np.array(line)
        ul = np.minimum(linebox[0], linebox[1])
        tr = np.maximum(linebox[0], linebox[1])
        return self._index(ul), self._index(tr)

    def _index(self, point):
        return int(point[0]/self.step), int(point[1]/self.step)


def test():
    grid = SparseGrid(10)
    grid.insert(([((1,3), (31, -62))], 'this is a dog'))
    grid.insert(([((102, 77), (187, 203))], 'this is a cat'))
    print('first query')
    for st in grid.query(((11, 15), (18, 23))):
        print(st)

    print('second query')
    for st in grid.query(((11, -5), (-18, 23))):
        print(st)

    print('third query')
    for st in grid.query(((0, 0), (200, 200))):
        print(st)

#test()