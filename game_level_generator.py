'''
This module provides a custom implementation (with some modifications) of the algorithm proposed in
L. Johnson, G. N. Yannakakis, and J. Togelius, "Cellular automata for real-time generation of infinite cave levels," Jun. 2010.
(https://dl.acm.org/citation.cfm?id=1814266)
'''
import random
import sys

'''
Algorithm parameters:
1. R - rock cells rate
2. N - number of CA iterations per grid
3. T - CA rock expansion threshold
4. M - CA Moore neighborhood range
5. S - length of grid side
These parameters are regarded as constants; if needed, the user should alter them only once after loading the module and before using any of its functions.
'''
R, N, T, M, S = (0.5, 4, 5, 1, 50)# default algorithm parameters

class Cell(object):
    Floor, Rock = range(2)

class Position(object):
    Current, North, South, West, East = range(5)

class _Map(object):
    def __init__(self):
        self.map_ = {}
        self.__y, self.__x = (0, 0)# coordinates of current grid
        self.__expand()

    def __assign_random(self, key):
        if key not in self.map_:
            random.seed(None)
            self.map_[key] = random.getrandbits(128)

    def get_position(self, position):
        if position == Position.Current:
            return (self.__y, self.__x)
        elif position == Position.North:
            return (self.__y + 1, self.__x)
        elif position == Position.South:
            return (self.__y - 1, self.__x)
        elif position == Position.West:
            return (self.__y, self.__x - 1)
        elif position == Position.East:
            return (self.__y, self.__x + 1)

    def __expand(self):
        list(map(self.__assign_random, map(self.get_position, range(5))))

    def go_position(self, position):
        self.__y, self.__x = self.get_position(position)
        self.__expand()

def _get_random_grid(seed):
    random.seed(seed)
    return [[Cell.Floor if random.random() >= R else Cell.Rock for j in range(S)] for i in range(S)]

def _count_rock_neighbors(grid, i, j, ss = None):
    if ss == None:
        ss = S
    counter = 0
    for ii in range(i - M, i + M + 1):
        for jj in range(j - M, j + M + 1):
            if 0 <= ii < ss and 0 <= jj < ss and grid[ii][jj] == Cell.Rock:
                counter += 1
    return counter

def _apply_CA(grid):
    for k in range(N):
        grid = [[Cell.Rock if _count_rock_neighbors(grid, i, j) >= T else Cell.Floor for j in range(S)] for i in range(S)]
    return grid

def _get_CA_pentagrid(map_):
    return (_apply_CA(_get_random_grid(map_.map_[map_.get_position(Position.Current)])),
            _apply_CA(_get_random_grid(map_.map_[map_.get_position(Position.North)])),
            _apply_CA(_get_random_grid(map_.map_[map_.get_position(Position.South)])),
            _apply_CA(_get_random_grid(map_.map_[map_.get_position(Position.West)])),
            _apply_CA(_get_random_grid(map_.map_[map_.get_position(Position.East)])))

def _reinforce_local_continuity(pentagrid, neighbor, is_x_outer, current_range_params, neighbor_range_params):
    min_index, min_value = (-1, sys.maxsize)
    for outer in range(S):
        counter = 0
        for inner in range(*current_range_params):
            if is_x_outer:
                if pentagrid[Position.Current][inner][outer] == Cell.Floor:
                    break
                else:
                    counter += 1
            else:
                if pentagrid[Position.Current][outer][inner] == Cell.Floor:
                    break
                else:
                    counter += 1
        for inner in range(*neighbor_range_params):
            if is_x_outer:
                if pentagrid[neighbor][inner][outer] == Cell.Floor:
                    break
                else:
                    counter += 1
            else:
                if pentagrid[neighbor][outer][inner] == Cell.Floor:
                    break
                else:
                    counter += 1
        min_index, min_value = min((min_index, min_value), (outer, counter), key = lambda arg: arg[1])
    for inner in range(*current_range_params):
        if is_x_outer:
            if pentagrid[Position.Current][inner][min_index] == Cell.Floor:
                break
            else:
                pentagrid[Position.Current][inner][min_index] = Cell.Floor
        else:
            if pentagrid[Position.Current][min_index][inner] == Cell.Floor:
                break
            else:
                pentagrid[Position.Current][min_index][inner] = Cell.Floor
    for inner in range(*neighbor_range_params):
        if is_x_outer:
            if pentagrid[neighbor][inner][min_index] == Cell.Floor:
                break
            else:
                pentagrid[neighbor][inner][min_index] = Cell.Floor
        else:
            if pentagrid[neighbor][min_index][inner] == Cell.Floor:
                break
            else:
                pentagrid[neighbor][min_index][inner] = Cell.Floor

def _reinforce_continuity(pentagrid):
    _reinforce_local_continuity(pentagrid, Position.North, True, (S,), (S - 1, -1, -1))# current-north continuity
    _reinforce_local_continuity(pentagrid, Position.South, True, (S - 1, -1, -1), (S,))# current-south continuity
    _reinforce_local_continuity(pentagrid, Position.West, False, (S,), (S - 1, -1, -1))# current-west continuity
    _reinforce_local_continuity(pentagrid, Position.East, False, (S - 1, -1, -1), (S,))# current-east continuity

'''def _unify_pentagrid(pentagrid):
    unified_pentagrid = [[pentagrid[Position.North][y][x - S] if S <= x < 2 * S else -1 for x in range(3 * S)] for y in range(S)]
    unified_pentagrid += [[pentagrid[Position.West][y][x] if x < S else pentagrid[Position.Current][y][x - S] if S <= x < 2 * S else pentagrid[Position.East][y][x - 2 * S] for x in range(3 * S)] for y in range(S)]
    unified_pentagrid += [[pentagrid[Position.South][y][x - S] if S <= x < 2 * S else -1 for x in range(3 * S)] for y in range(S)]
    return unified_pentagrid

def _apply_CA_on_unified_pentagrid(unified_pentagrid):
    for k in range(N):
        unified_pentagrid = [[-1 if unified_pentagrid[i][j] == -1 else Cell.Rock if _count_rock_neighbors(unified_pentagrid, i, j, 3 * S) >= T else Cell.Floor for j in range(S)] for i in range(S)]
    return unified_pentagrid

def _get_final_current_grid(unified_pentagrid):
    return [[unified_pentagrid[y][x] for x in range(S, 2 * S)] for y in range(S, 2 * S)]'''# experimental code section

'''
Instantiates a game map, and returns it.
'''
def get_new_map():
    return _Map()

'''
Changes the current grid in the given map to the neighbor grid in the given position.
The user may use the following positions:
1. Position.North
2. Position.South
3. Position.West
4. Position.East
'''
def go_to(map_, position):
    map_.go_position(position)

'''
Returns the current grid as a list of S lists of S cells.
Each of the cells is either Cell.Floor or Cell.Rock.
'''
def get_current_grid(map_):
    pentagrid = _get_CA_pentagrid(map_)
    _reinforce_continuity(pentagrid)
    return pentagrid[Position.Current]
