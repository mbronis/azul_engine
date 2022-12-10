import pytest

from src.env.tiles import Tile, SingleTileLine, MultiTileLine


def test_empty_line():
    m = MultiTileLine()
    assert m.total_filled == 0
    assert m.tiles == {}


def test_line_init():
    t = [Tile.BLACK, Tile.BLACK, Tile.BLUE]
    m = MultiTileLine(t)

    assert Tile.BLACK in m.tiles
    assert Tile.BLUE in m.tiles
    assert Tile.YELLOW not in m.tiles

    assert m.total_filled == 3
    assert m.tiles[Tile.BLACK].filled == 2
    assert m.tiles[Tile.BLUE].filled == 1
    assert m.tiles[Tile.YELLOW].filled == 0


def test_extend_empty():
    m = MultiTileLine()
    s = SingleTileLine()

    s.add_one(Tile.BLACK)
    m.extend(s)

    assert m.total_filled == 1
    assert Tile.BLACK in m.tiles
    assert m.tiles[Tile.BLACK].filled == 1


def test_extend_non_empty():
    m = MultiTileLine([Tile.BLACK])
    s = SingleTileLine()

    s.add_one(Tile.BLACK)
    m.extend(s)

    assert m.total_filled == 2
    assert Tile.BLACK in m.tiles
    assert m.tiles[Tile.BLACK].filled == 2


def test_merge():
    m = MultiTileLine([Tile.BLACK, Tile.BLUE])
    other = MultiTileLine([Tile.BLACK, Tile.YELLOW])
    m.merge(other)

    assert m.total_filled == 4
    assert m.tiles[Tile.BLACK].filled == 2
    assert m.tiles[Tile.BLUE].filled == 1
    assert m.tiles[Tile.YELLOW].filled == 1
    assert m.tiles[Tile.SNOW].filled == 0


def test_merge_to_empty():
    m = MultiTileLine()
    other = MultiTileLine([Tile.BLACK, Tile.BLUE])
    m.merge(other)

    assert m.total_filled == 2
    assert m.tiles[Tile.BLACK].filled == 1
    assert m.tiles[Tile.BLUE].filled == 1
    assert m.tiles[Tile.YELLOW].filled == 0


def test_merge_other_empty():
    m = MultiTileLine([Tile.BLACK, Tile.BLUE])
    other = MultiTileLine()
    m.merge(other)

    assert m.total_filled == 2
    assert m.tiles[Tile.BLACK].filled == 1
    assert m.tiles[Tile.BLUE].filled == 1
    assert m.tiles[Tile.YELLOW].filled == 0


def test_merge_both_empty():
    m = MultiTileLine()
    other = MultiTileLine()
    m.merge(other)

    assert m.total_filled == 0
    assert m.tiles[Tile.BLACK].filled == 0
    assert m.tiles[Tile.BLUE].filled == 0
    assert m.tiles[Tile.YELLOW].filled == 0


@pytest.fixture
def multi_line() -> MultiTileLine:
    return MultiTileLine([Tile.BLACK, Tile.BLACK, Tile.BLUE])


def test_get_existing(multi_line: MultiTileLine):
    l = multi_line.get_all(Tile.BLACK)

    assert multi_line.total_filled == 1
    assert multi_line.tiles[Tile.BLACK].filled == 0
    assert multi_line.tiles[Tile.BLUE].filled == 1
    assert l.tile == Tile.BLACK
    assert l.filled == 2


def test_get_not_existing(multi_line: MultiTileLine):
    l = multi_line.get_all(Tile.YELLOW)

    assert multi_line.total_filled == 3
    assert multi_line.tiles[Tile.BLACK].filled == 2
    assert multi_line.tiles[Tile.BLUE].filled == 1
    assert l.tile == None
    assert l.filled == 0


def test_reset(multi_line: MultiTileLine):
    multi_line.reset()

    assert multi_line.total_filled == 0
    assert Tile.BLACK in multi_line.tiles
    assert Tile.BLUE in multi_line.tiles


def test_get_one(multi_line: MultiTileLine):
    t = multi_line.get_one(Tile.BLACK)

    assert t == Tile.BLACK
    assert multi_line.total_filled == 2


def test_get_random(multi_line: MultiTileLine):
    selected = multi_line.get_random(n=2)

    assert selected.total_filled == 2
    assert multi_line.total_filled == 1


def test_get_random_from_with_too_few(multi_line: MultiTileLine):
    _ = multi_line.get_random(n=2)
    selected = multi_line.get_random(n=2)

    assert selected.total_filled == 1
    assert multi_line.total_filled == 0


def test_get_random_from_empty():
    multi_line = MultiTileLine()
    selected = multi_line.get_random(n=1)

    assert selected.total_filled == 0
