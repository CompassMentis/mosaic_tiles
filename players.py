from settings import Settings


class Player:
    def __init__(self, name, order, is_human):
        self.name = name
        self.order = order
        self.is_human = is_human
