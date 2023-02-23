class Dishes:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.initials = ""  # 首字母
        self.cook_time = 0
        self.ingredients = []
        self.seasonings = []
        self.additive_steps = []  # {additive_id : "", time: ""}
        self.stir_fry_steps = []  # {stir_fry_id : "", time: ""}
        self.fire_steps = []  # {fire_id : "", time: ""}
