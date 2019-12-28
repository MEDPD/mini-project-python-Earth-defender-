
class EarthDefenderError(Exception):
    def __init__(self, error):
        self.error = error