import random
from itertools import starmap
from operator import eq
from typing import Sequence, Iterable, Tuple

import numpy as np


from hesearch.algorithms.search import HeuristicEstimator
from hesearch.framework.problem import SearchState, SearchSpace


class NPuzzleState(SearchState):

    BLANK_VALUE = 0

    @staticmethod
    def get_goal_state(n: int) -> 'NPuzzleState':
        goal_tiles = list(range(n ** 2))
        return NPuzzleState(goal_tiles)

    def __init__(self, tiles: Sequence[int]):
        self.n = int(np.sqrt(len(tiles)))
        self.tiles = tuple(tiles)
        self.__blank_pos = tiles.index(self.BLANK_VALUE)
        self.state_id = ",".join(map(str, tiles))

    def get_id(self) -> str:
        return self.state_id

    def display(self) -> str:
        return repr(np.array(self.tiles).reshape((self.n, self.n)))

    def get_blank_position(self):
        return self.__blank_pos


class NPuzzleProblem(SearchSpace):

    RELATIVE_LEFT = -1
    RELATIVE_RIGHT = 1

    def __init__(self, nsize: int, seed: int = None, optimal_depth: int = 100):
        self.n = nsize
        self.num_tiles = nsize ** 2
        self.goal = NPuzzleState.get_goal_state(nsize)
        self.optimal_depth = optimal_depth
        self.random = random.Random(seed)

        self.relative_top = -self.n
        self.relative_bottom = self.n
        self.__possible_relative_moves = (self.RELATIVE_LEFT, self.RELATIVE_RIGHT, self.relative_top, self.relative_bottom)

    def get_initial_state(self) -> NPuzzleState:
        # chooses randonly but carefully the initial state, due to the fact that not all initial states are solvable
        current_state = self.goal
        for _ in range(self.optimal_depth):
            children = list(self.generate_children(current_state))
            current_state, _ = self.random.choice(children)

        return current_state

    def generate_children(self, state: NPuzzleState) -> Iterable[Tuple[SearchState, float]]:
        blank_pos = state.get_blank_position()
        state_tiles = state.tiles
        possible_moves = self.__get_move_possibilities(blank_pos)
        for is_possible, relative_pos in zip(possible_moves, self.__possible_relative_moves):
            if not is_possible:
                continue

            abs_pos = blank_pos + relative_pos
            new_state_tiles = list(state_tiles)
            new_state_tiles[blank_pos] = new_state_tiles[abs_pos]
            new_state_tiles[abs_pos] = NPuzzleState.BLANK_VALUE
            new_state = NPuzzleState(new_state_tiles)
            yield new_state, 1

    def __get_move_possibilities(self, blank_pos) -> Sequence[bool]:
        """
        check the possible moves from the given [blank_pos].
        :param blank_pos: the position of the blank tile
        :return:
        """
        return (
            self.__is_left_move_possible(blank_pos),
            self.__is_right_move_possible(blank_pos),
            self.__is_up_move_possible(blank_pos),
            self.__is_bottom_move_possible(blank_pos)
        )

    def __is_left_move_possible(self, blank_pos: int) -> bool:
        """
        does the blank can move left (or the left tile can fill the blank)
        :param blank_pos: the position of the blank tile
        :return:
        """
        return (blank_pos % self.n) != 0

    def __is_right_move_possible(self, blank_pos: int) -> bool:
        """
        does the blank can move right (or the right tile can fill the blank)
        :param blank_pos: the position of the blank tile
        :return:
        """
        return (blank_pos % self.n) != (self.n - 1)

    def __is_up_move_possible(self, blank_pos: int) -> bool:
        """
        does the blank can move up (or the top tile can fill the blank)
        :param blank_pos: the position of the blank tile
        :return:
        """
        return (blank_pos // self.n) != 0

    def __is_bottom_move_possible(self, blank_pos: int) -> bool:
        """
        does the blank can move down (or the bottom tile can fill the blank)
        :param blank_pos: the position of the blank tile
        :return:
        """
        return (blank_pos // self.n) != self.n - 1

    def is_goal(self, state: NPuzzleState) -> bool:
        return all(starmap(eq, zip(range(self.num_tiles), state.tiles)))


class NPuzzleManhattanDistanceHeuristicEstimator(HeuristicEstimator):

    def __init__(self, nsize: int):
        self.n = nsize
        self.goal = NPuzzleState.get_goal_state(nsize)

    def estimate(self, state: NPuzzleState) -> float:
        sum_distances = 0
        for pos, tile in enumerate(state.tiles):
            if tile != 0:
                position_diff = abs(tile - pos)
                vertical_moves = position_diff // self.n
                horizontal_moves = position_diff % self.n
                tile_distance = vertical_moves + horizontal_moves
                sum_distances += tile_distance

        return sum_distances
