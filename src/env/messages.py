from dataclasses import dataclass, field


@dataclass
class Messages:
    action_draw_success: str = field(init=False)
    action_draw_fail_board: str = field(init=False)
    action_draw_fail_factory: str = field(init=False)


class DefaultMessages(Messages):
    action_draw_success = "Action successful"
    action_draw_fail_board = "Action failed: can't fill row {row} with {tile}"
    action_draw_fail_factory = "Action failed: factory {factory_no} has no {tile}"


def get_messages(name: str = "default"):
    messages = {
        "default": DefaultMessages,
    }
    return messages[name]
