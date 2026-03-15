import pyqtgraph as pg
import numpy as np

pg.setConfigOption("foreground", "k")  # black foreground
pg.setConfigOption("background", "w")  # white background
pg.setConfigOptions(antialias=True)  # prettier plots


class ChartBase(pg.PlotWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

    def setTitle(self, title):
        self.plotItem.setTitle(title, size="20pt")

    def setSubTitle(self, subtitle):
        pass

    def setXLabel(self, text, units=""):
        _style = {"font-size": "15pt"}
        self.setLabel("bottom", text, units=units, **_style)

    def setYLabel(self, text, units=""):
        _style = {"font-size": "15pt"}
        self.setLabel("left", text, units=units, **_style)

    # def plot(self, x, y, **kwargs):
    #    self.plotItem.plot(x, y, kwargs)

    def show(self, flag: bool):
        if flag:
            super().show()
        else:
            super().hide()


class LineChart(ChartBase):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def plot_data(self, x, y, pen=None):
        self.clear()
        _color = pg.mkColor(0, 0, 255)  # blue
        if pen is None:
            pen = pg.mkPen(color=_color, width=2)
        self.plot(x, y, pen=pen, clear=True, fillLevel=0, fillBrush=_color)


class MultiLineChart(ChartBase):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def plot_data(self, x, y, names, pen=None, median=False):
        self.clear()
        if isinstance(y[0], list):
            # _max=len(names)
            if len(y) > 10:
                for _i, _y in enumerate(y):
                    self.plot(x, _y, pen=pg.mkPen(_i, width=3))
            else:
                for _i, _y in enumerate(y):
                    self.plot(x, _y, pen=pg.mkPen(_i, width=3), name=names[_i])

            if median:  # plot median line?
                result = np.array(y).T
                x = np.arange(result.shape[0])
                _median = np.median(result, axis=1)

                self.plot(x, _median, pen=pg.mkPen("k", width=3), name="median")

        else:  # single line
            _color = pg.mkColor(0, 0, 255)  # blue
            if pen is None:
                pen = pg.mkPen(color=_color, width=2)
            self.plot(x, y, pen=pen, clear=True)  # , fillLevel=0, fillBrush=_color)


class StackChart(ChartBase):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

    def plot_data(self, x, y, names):
        self.clear()
        stacked_y = np.cumsum(y, axis=0)

        if isinstance(y[0], list):
            _max = len(names)
            for _i, _y in enumerate(stacked_y):
                # _color=pg.intColor(_i, hues=_max, minHue=200, maxHue=260, minValue=100)
                _line = self.plot(
                    x, _y, pen=None, fillLevel=0, fillBrush=(_i, _max), name=names[_i]
                )
                _line.setZValue(_max - _i)
        else:  # really a line chart
            _color = pg.mkColor(0, 0, 255)  # blue
            pen = pg.mkPen(color=_color, width=2)
            self.plot(x, y, pen=pen, clear=True, fillLevel=0, fillBrush=_color)


class MonteCarloChart(ChartBase):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

    def plot_data(self, x, y):
        self.clear()
        # put an y axis on the right side of the chart.
        _style = {"font-size": "15pt"}
        self.setLabel("right", "Dollars", units="$", **_style)

        result = np.array(y).T
        x = np.arange(result.shape[0])
        median = np.median(result, axis=1)
        offsets = (10, 20, 30, 40)

        # print(median[-1])
        self.addLegend()

        for offset in offsets:
            low = np.percentile(result, 50 - offset, axis=1)
            high = np.percentile(result, 50 + offset, axis=1)

            _alpha = 2.5 * (55 - offset)
            _curve1 = self.plot(x, low)
            _curve2 = self.plot(x, high)
            _fill = pg.FillBetweenItem(_curve1, _curve2, brush=(100, 100, 255, _alpha))
            self.addItem(_fill)

        # plot the median values
        self.plot(x, median, pen=pg.mkPen(color="k", width=3), name="median")
