import pytest

from src.env.tiles import Tile, SingleTileLine, MultiTileLine


def test_empty_line():
    m = MultiTileLine()
    assert m.total_size == 0
    assert m.tiles == {}


def test_line_init():
    t = [Tile.BLACK, Tile.BLACK, Tile.BLUE]
    m = MultiTileLine(t)

    assert Tile.BLACK in m.tiles
    assert Tile.BLUE in m.tiles
    assert Tile.YELLOW not in m.tiles

    assert m.total_size == 3
    assert m.tiles[Tile.BLACK].filled == 2
    assert m.tiles[Tile.BLUE].filled == 1
    assert m.tiles[Tile.YELLOW].filled == 0


def test_extend_empty():
    m = MultiTileLine()
    s = SingleTileLine()

    s.add_one(Tile.BLACK)
    m.extend(s)

    assert m.total_size == 1
    assert Tile.BLACK in m.tiles
    assert m.tiles[Tile.BLACK].filled == 1


def test_extend_non_empty():
    m = MultiTileLine([Tile.BLACK])
    s = SingleTileLine()

    s.add_one(Tile.BLACK)
    m.extend(s)

    assert m.total_size == 2
    assert Tile.BLACK in m.tiles
    assert m.tiles[Tile.BLACK].filled == 2


def test_merge():
    m = MultiTileLine([Tile.BLACK, Tile.BLUE])
    other = MultiTileLine([Tile.BLACK, Tile.YELLOW])
    m.merge(other)

    assert m.total_size == 4
    assert m.tiles[Tile.BLACK].filled == 2
    assert m.tiles[Tile.BLUE].filled == 1
    assert m.tiles[Tile.YELLOW].filled == 1
    assert m.tiles[Tile.SNOW].filled == 0


def test_merge_to_empty():
    m = MultiTileLine()
    other = MultiTileLine([Tile.BLACK, Tile.BLUE])
    m.merge(other)

    assert m.total_size == 2
    assert m.tiles[Tile.BLACK].filled == 1
    assert m.tiles[Tile.BLUE].filled == 1
    assert m.tiles[Tile.YELLOW].filled == 0


def test_merge_other_empty():
    m = MultiTileLine([Tile.BLACK, Tile.BLUE])
    other = MultiTileLine()
    m.merge(other)

    assert m.total_size == 2
    assert m.tiles[Tile.BLACK].filled == 1
    assert m.tiles[Tile.BLUE].filled == 1
    assert m.tiles[Tile.YELLOW].filled == 0


def test_merge_both_empty():
    m = MultiTileLine()
    other = MultiTileLine()
    m.merge(other)

    assert m.total_size == 0
    assert m.tiles[Tile.BLACK].filled == 0
    assert m.tiles[Tile.BLUE].filled == 0
    assert m.tiles[Tile.YELLOW].filled == 0


def test_get_existing():
    m = MultiTileLine([Tile.BLACK, Tile.BLACK, Tile.BLUE])
    l = m.get(Tile.BLACK)

    assert m.total_size == 1
    assert m.tiles[Tile.BLACK].filled == 0
    assert m.tiles[Tile.BLUE].filled == 1
    assert l.tile == Tile.BLACK
    assert l.filled == 2


def test_get_not_existing():
    m = MultiTileLine([Tile.BLACK, Tile.BLACK, Tile.BLUE])
    l = m.get(Tile.YELLOW)

    assert m.total_size == 3
    assert m.tiles[Tile.BLACK].filled == 2
    assert m.tiles[Tile.BLUE].filled == 1
    assert l.tile == None
    assert l.filled == 0


def test_reset():
    m = MultiTileLine([Tile.BLACK, Tile.BLACK, Tile.BLUE])
    m.reset()

    assert m.total_size == 0
    assert Tile.BLACK in m.tiles
    assert Tile.BLUE in m.tiles
