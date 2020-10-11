
class Region:
    def __init__(self, name):
        self._id = name
        self.name = name

        # current statistics
        self.confirmed = None
        self.active = None
        self.recoveries = None
        self.mortalities = None

        # list of historical statistics
        self.daily = None
        self.cumualtive = None

        self.cities = None
