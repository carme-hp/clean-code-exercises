# TODO: refactor & clean up this class.
#  - Familiarize yourself with the code and what it does (it is easiest to read the tests first)
#  - refactor ...
#     - give the functions/variables proper names
#     - make the function bodies more readable
#     - clean up the test code where beneficial
#     - make sure to put each individual change in a small, separate commit
#     - take care that on each commit, all tests pass
from typing import Tuple
from dataclasses import dataclass

class Point:
    def __init__(self,
                 x: float,
                 y: float) -> None:
        self.x = x
        self.y = y
class RasterGrid:
    @dataclass
    class Cell:
        _ix: int
        _iy: int

    def __init__(self,
                 x0: float,
                 y0: float,
                 x1: float,
                 y1: float,
                 nx: int,
                 ny: int) -> None:
        self._point0 = Point(x0,y0)
        self._point1 = Point(x1,y1)
        self._nx = nx
        self._ny = ny
        self.nc = nx*ny
        self.cells = [
            self.Cell(i, j) for i in range(nx) for j in range(ny)
        ]

    def get_cell_center(self, cell: Cell) -> Tuple[float, float]:
        return (
            self._point0.x + (float(cell._ix) + 0.5)*(self._point1.x - self._point0.x)/self._nx,
            self._point0.y + (float(cell._iy) + 0.5)*(self._point1.y - self._point0.y)/self._ny
        )

    def get_cell(self, x: float, y: float) -> Cell:
        eps = 1e-6*max(
            (self._point1.x-self._point0.x)/self._nx,
            (self._point1.y-self._point0.y)/self._ny
        )
        if abs(x - self._point1.x) < eps:
            ix = self._nx - 1
        elif abs(x - self._point0.x) < eps:
            ix = 0
        else:
            ix = int((x - self._point0.x)/((self._point1.x - self._point0.x)/self._nx))
        if abs(y - self._point1.y) < eps:
            iy = self._ny - 1
        elif abs(y - self._point0.y) < eps:
            iy = 0
        else:
            iy = int((y - self._point0.y)/((self._point1.y - self._point0.y)/self._ny))
        return self.Cell(ix, iy)


def test_number_of_cells():
    x0 = 0.0
    y0 = 0.0
    dx = 1.0
    dy = 1.0
    assert RasterGrid(x0, y0, dx, dy, 10, 10).nc == 100
    assert RasterGrid(x0, y0, dx, dy, 10, 20).nc == 200
    assert RasterGrid(x0, y0, dx, dy, 20, 10).nc == 200
    assert RasterGrid(x0, y0, dx, dy, 20, 20).nc == 400


def test_locate_cell():
    grid = RasterGrid(0.0, 0.0, 2.0, 2.0, 2, 2)
    cell = grid.get_cell(0, 0)
    assert cell._ix == 0 and cell._iy == 0
    cell = grid.get_cell(1, 1)
    assert cell._ix == 1 and cell._iy == 1
    cell = grid.get_cell(0.5, 0.5)
    assert cell._ix == 0 and cell._iy == 0
    cell = grid.get_cell(1.5, 0.5)
    assert cell._ix == 1 and cell._iy == 0
    cell = grid.get_cell(0.5, 1.5)
    assert cell._ix == 0 and cell._iy == 1
    cell = grid.get_cell(1.5, 1.5)
    assert cell._ix == 1 and cell._iy == 1


def test_cell_center():
    grid = RasterGrid(0.0, 0.0, 2.0, 2.0, 2, 2)
    cell = grid.get_cell(0.5, 0.5)
    assert abs(grid.get_cell_center(cell)[0] - 0.5) < 1e-7 and abs(grid.get_cell_center(cell)[1] - 0.5) < 1e-7
    cell = grid.get_cell(1.5, 0.5)
    assert abs(grid.get_cell_center(cell)[0] - 1.5) < 1e-7 and abs(grid.get_cell_center(cell)[1] - 0.5) < 1e-7
    cell = grid.get_cell(0.5, 1.5)
    assert abs(grid.get_cell_center(cell)[0] - 0.5) < 1e-7 and abs(grid.get_cell_center(cell)[1] - 1.5) < 1e-7
    cell = grid.get_cell(1.5, 1.5)
    assert abs(grid.get_cell_center(cell)[0] - 1.5) < 1e-7 and abs(grid.get_cell_center(cell)[1] - 1.5) < 1e-7


def test_cell_iterator() -> None:
    grid = RasterGrid(0.0, 0.0, 2.0, 2.0, 2, 2)
    count = sum(1 for _ in grid.cells)
    assert count == grid.nc

    cell_indices_without_duplicates = set(list(
        (cell._ix, cell._iy) for cell in grid.cells
    ))
    assert len(cell_indices_without_duplicates) == count
