from dataclasses import dataclass, field


@dataclass
class Messages:
    welcome_message: str = field(init=False)
    action_draw_success: str = field(init=False)
    action_draw_fail_board: str = field(init=False)
    action_draw_fail_factory: str = field(init=False)


class DefaultMessages(Messages):
    welcome_message = "Welcome to Azul Engine :D"
    action_draw_success = "Action successful"
    action_draw_fail_board = "Action failed: can't fill row {row} with {tile}"
    action_draw_fail_factory = "Action failed: factory {factory_no} has no {tile}"


class PLMessages(Messages):
    welcome_message = "Witaj w Azulu :D"
    action_draw_success = "Wykonano ruch"
    action_draw_fail_board = "Nie wykonano ruchu: nie mozna wypełnić wiersza {row} płytką {tile}"
    action_draw_fail_factory = "Nie wykonano ruchu: fabryka {factory_no} nie ma płytki {tile}"


def get_messages(name: str = "default"):
    messages = {
        "default": DefaultMessages,
        "pl": PLMessages,
    }
    return messages[name]
