from datetime import datetime, date

import logging

logger = logging.getLogger(__name__)


class ImportHelper:
    def str2float(self, s: str):
        s = s.strip()
        if s == "":
            return None

        try:
            return float(s)
        except ValueError:
            _str = "Cannot convert '%s' to a float" % s
            logger.error(_str)
            raise ValueError(_str)

    def strpct2float(self, s: str):
        """convert a percent string to a float value"""
        s = s.strip()
        if s.endswith("%"):
            s = s[:-1]
        if s == "":
            return None
        return self.str2float(s)

    def strpct2int(self, s: str):
        """convert a percent string to a float value"""
        s = s.strip()
        if s.endswith("%"):
            s = s[:-1]
        if s == "":
            return None
        return self.str2int(s)

    def str2int(self, s: str):
        s = s.strip()
        if s is None or s == "":
            return None

        try:
            return int(s)
        except ValueError:
            _str = "Cannot convert '%s' to an integer" % s
            logger.error(_str)
            raise ValueError(_str)

    def str2date(self, s: str):
        if s is None or s in ("", "None"):
            return None

        try:
            _dt = datetime.strptime(s, "%m/%d/%Y")
            return date(_dt.year, _dt.month, _dt.day)
        except ValueError:
            _str = "Cannot convert '%s' to a date" % s
            logger.error(_str)
            raise ValueError(_str)
