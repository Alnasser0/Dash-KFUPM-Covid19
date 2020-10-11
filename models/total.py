
class Total:
    def __init__(self, id):
        self._id = id

        # current statistics
        self.confirmed = None
        self.active = None
        self.recoveries = None
        self.mortalities = None
        self.critical = None
        self.tested = None

        # list of historical statistics
        self.daily = None
        self.cumualtive = None
