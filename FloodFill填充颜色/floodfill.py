from __future__ import annotations
from enum import IntEnum
from typing import List, NamedTuple, Generic, Optional, TypeVar, Set
import matplotlib.pyplot as plt
import numpy as np
import cv2

from utils import Stack


class Cell(IntEnum):
    EMPTY = 255
    BLOCKED = 0
    START = 100
    END = 200
    PATH = 150


class Color(IntEnum):
    EMPTY = 0
    BLOCKED = 255
    START = 100
    END = 200
    FILL = 150


class MazeLocation(NamedTuple):
    row: int
    col: int


T = TypeVar('T')


class Maze:
    class _Node(Generic[T]):
        def __init__(self, state: T, parent: Optional[T], cost: float = 0.0, heuristic: float = 0.0) -> None:
            self.state: T = state
            self.parent: Optional[T] = parent
            self.cost: float = cost
            self.heuristic: float = heuristic

        def __lt__(self, other: Maze._Node) -> bool:
            return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def __init__(self, rows: int = 10, cols: int = 10,
                 sparse: float = 0.2, seed: int = 365,
                 start: MazeLocation = MazeLocation(0, 0),
                 end: MazeLocation = MazeLocation(9, 9), *,
                 grid: Optional[np.array] = None) -> None:
        np.random.seed(seed)
        self._start: MazeLocation = start
        self._end: MazeLocation = end
        if grid is None:
            self._grid: np.array = np.random.choice([Cell.BLOCKED, Cell.EMPTY],
                                                    (rows, cols), p=[sparse, 1 - sparse])
        else:
            self._grid: np.array = grid
        self._grid[start] = Cell.START
        self._grid[end] = Cell.END

    def _test_goal(self, m1: MazeLocation) -> bool:
        return m1 == self._end

    def _success(self, m1: MazeLocation) -> List[MazeLocation]:
        location: List[MazeLocation] = []
        row, col = self._grid.shape
        if m1.row + 1 < row and self._grid[m1.row + 1, m1.col] != Cell.BLOCKED:
            location.append(MazeLocation(m1.row + 1, m1.col))
        if m1.row - 1 >= 0 and self._grid[m1.row - 1, m1.col] != Cell.BLOCKED:
            location.append(MazeLocation(m1.row - 1, m1.col))
        if m1.col + 1 < col and self._grid[m1.row, m1.col + 1] != Cell.BLOCKED:
            location.append(MazeLocation(m1.row, m1.col + 1))
        if m1.col - 1 >= 0 and self._grid[m1.row, m1.col - 1] != Cell.BLOCKED:
            location.append(MazeLocation(m1.row, m1.col - 1))
        return location

    def _draw(self, pause: float) -> None:
        plt.imshow(self._grid, cmap='rainbow', interpolation='nearest')
        plt.xticks([])
        plt.yticks([])
        plt.pause(interval=pause)
        plt.cla()

    def draw(self, colormap='rainbow') -> None:
        plt.close()
        fig, ax = plt.subplots()
        ax.imshow(self._grid, cmap=colormap)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()


class FloodFill(Maze):
    def _fill(self, pause, plot) -> None:
        stack: Stack = Stack()
        initial: Maze._Node = self._Node(self._start, None)
        marked: Set[MazeLocation] = {initial.state}
        stack.push(initial)
        while stack:
            parent: Maze._Node = stack.pop()
            state: MazeLocation = parent.state
            self._grid[state] = Cell.PATH
            if plot:
                self._draw(pause)
            children: List[MazeLocation] = self._success(state)
            for child in children:
                if child not in marked:
                    marked.add(child)
                    stack.push(self._Node(child, parent))

    def show_path(self, pause: float = 0.5, *, plot: bool = True) -> None:
        self._fill(pause, plot=plot)


if __name__ == "__main__":
    file = 'D://QQPCMgr/Desktop/test1.bmp'
    bmp = cv2.imread(file)[:, :, 0]
    d = FloodFill(rows=100, cols=100, start=MazeLocation(145, 145), end=MazeLocation(146, 146), grid=bmp)
    d.show_path(pause=0.0000001)
    d.draw()
