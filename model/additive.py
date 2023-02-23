class Additive:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.measure = 0


class Ingredient(Additive):
    def __init__(self):
        super(Ingredient, self).__init__()
        self.shape = ""


class Seasoning(Additive):
    def __init__(self):
        super(Seasoning, self).__init__()
