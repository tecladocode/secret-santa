from utils.localisation import localise


class Error(Exception):
    def __init__(self, key, should_localise=True, **kwargs):
        self.message = localise(key, **kwargs) if should_localise else key
