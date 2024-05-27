class Cell:
    type_list = ['building', 'start', 'jail', 'go_to_jail', 'chance', 'community_chest']

    def __init__(self, position, name,  type, details):
        self.position = position
        self.name = name
        self.details = details
        self.item = []

        if type not in Cell.type_list:
            raise ValueError(f"Invalid cell type: {type}")
        self.type = type
        match type:
            case 'building':
                self.price = details['price']
                self.rent = details['rent']
                self.owner = None
            case 'start':
                pass
            case 'jail':
                self.stayTerms = details['stayTerms']
            case 'go_to_jail':
                self.target_position = details['target_position']
            case 'chance':
                pass
            case 'community_chest':
                self.reward = details['reward']
            case _:
                raise ValueError(f"Invalid cell type: {type}")

    def __repr__(self):
        return f"Cell('{self.name}', {self.position}, {self.type}, {self.details})"
