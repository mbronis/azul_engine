def print_state(s: dict):
    for n, f in s["factories"].items():
        print(f"{n}: {f}")
    print(f"mid: {s['mid_factory']}")
    for b in s["boards"].values():
        print_board(b)


def print_board(s: dict):
    print(f"{s['player_name']} board, score: {s['score']}")
    print(f"  filled:   {s['wall']['filled']}")
    print(f"  expected: {s['wall']['expected']}")
    print(f"  pattern:  {s['pattern_lines']}")
    print(f"  floor:    {s['floor_line']['tiles']}")
