from src.env.board.pattern_lines import PatternLines


def test_init():
    size = 5
    lines = PatternLines(size)

    assert [l.size for l in lines._lines] == [n + 1 for n in range(size)]
    assert sum(l.filled for l in lines._lines) == 0
