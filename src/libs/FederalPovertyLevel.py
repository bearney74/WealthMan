import logging

logger = logging.getLogger(__name__)

# fix me.. put in data file in data directory...
#  Family Size: Income limit
fpl = {1: 15060, 2: 20400, 3: 25820, 4: 31200}


class FederalPovertyLevel:
    def __init__(self, family_size: int = 1):
        # Family Size: Income limit
        _fpl = {1: 15060, 2: 20400, 3: 25820, 4: 31200}

        if family_size in _fpl.keys():
            self._level = _fpl[family_size]
        else:
            logging.error("FPL family size of '%s' is too large" % family_size)
            self._level = _fpl[4]

    def calc_percent(self, income):
        return float(int(100.0 * income / self._level))
