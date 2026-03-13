import matplotlib

matplotlib.use("QtAgg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from PyQt6.QtWidgets import QWidget, QVBoxLayout

import logging

logger = logging.getLogger(__name__)


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.axes = plt.subplots()
        super(MplCanvas, self).__init__(self.fig)

    # fix me...
    # when running unittests, I get the following error (warning):
    # /home/earney/projects/WealthMan/src/libs/gui/Analysis/ChartBase.py:19: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`). Consider using `matplotlib.pyplot.close()`.
    # self.fig, self.axes = plt.subplots()
    def __del__(self):
        plt.close(self.fig)


class ChartBase(QWidget):
    def __init__(self, parent, width=5, height=45, dpi=100):
        super(ChartBase, self).__init__(parent)
        self.title = ""
        self.subtitle = ""

        _layout = QVBoxLayout()
        self.canvas = MplCanvas(self, width=width, height=height, dpi=dpi)
        self.canvas.axes.set_xlabel("Year")
        self.canvas.axes.set_ylabel("Dollars")
        _layout.addWidget(self.canvas)
        self.setLayout(_layout)

    def __del__(self):
        print("Running ChartBase.__del__")
        self.canvas.__del__()

    def setTitle(self, title):
        self.title = title

    def setSubTitle(self, subtitle):
        self.subtitle = subtitle

    def show(self, flag: bool):
        assert isinstance(flag, bool)

        if flag:
            self.canvas.show()
        else:
            self.canvas.hide()

    def plot(self, data):
        pass


class LineChart(ChartBase):
    def __init__(self, parent, width=5, height=45, dpi=100):
        # super(ChartBase, self).__init__(parent)
        super().__init__(parent)

    def plot(self, data):
        _x_data = []
        _y_data = []
        for _x, _y in data:
            _x_data.append(_x)
            _y_data.append(_y)

        self.canvas.axes.clear()
        self.canvas.fig.suptitle(self.title)
        if self.subtitle != "":
            self.canvas.fig.text(0.5, 0.9, self.subtitle, horizontalalignment="center")
        (_line,) = self.canvas.axes.plot(_x_data, _y_data)

        self.setLabels(self.title)

        self.canvas.axes.fill_between(_x_data, 0, _y_data, alpha=0.7)
        _line.figure.canvas.draw()


class StackChart(ChartBase):
    def __init__(self, parent, width=5, height=45, dpi=100):
        # super(ChartBase, self).__init__(parent)
        super().__init__(parent)

    def plot(self, years, values, labels, legend_location="upper left"):
        self.canvas.axes.clear()

        try:
            _output = self.canvas.axes.stackplot(
                years, values, labels=labels, alpha=0.8
            )
        except ValueError as e:
            logger.error(
                "Please enter data into income/asset tabs to generate custom charts"
            )
            logger.error("%s" % e)
            logger.error(
                "plot arugments: years=%s, values=%s, labels=%s"
                % (years, values, labels)
            )
            self.canvas.fig.text(
                0.5,
                0.9,
                "",
                horizontalalignment="center",
            )
            self.canvas.fig.draw(self.canvas.fig.canvas.renderer)
            return

        self.canvas.fig.suptitle(self.title)
        if self.subtitle != "":
            self.canvas.fig.text(0.5, 0.9, self.subtitle, horizontalalignment="center")
        self.canvas.axes.legend(loc=legend_location)

        def format_string(x, pos):
            return "${:,d}".format(int(x))

        self.canvas.axes.yaxis.set_major_formatter(FuncFormatter(format_string))
        for _line in _output:
            if _line.figure is not None:
                _line.figure.canvas.draw()


class MultipleLinesChart(ChartBase):
    def __init__(self, parent, width=5, height=45, dpi=100):
        # super(ChartBase, self).__init__(parent)
        super().__init__(parent)

    def plot(self, years, data, labels, legend_location="upper left"):
        self.canvas.axes.clear()

        self.canvas.fig.suptitle(self.title)
        if self.subtitle != "":
            self.canvas.fig.text(0.5, 0.9, self.subtitle, horizontalalignment="center")

        def format_string(x, pos):
            return "${:,d}".format(int(x))

        self.canvas.axes.yaxis.set_major_formatter(FuncFormatter(format_string))

        # _num=len(labels)
        for _label in labels:
            _out = self.canvas.axes.plot(years, data[_label], label=_label)
            for _line in _out:
                if _line.figure is not None:
                    _line.figure.canvas.draw()

        self.canvas.axes.legend(loc=legend_location)
        # for some reason the legend does not get update unless we call the draw below...
        self.canvas.fig.draw(self.canvas.fig.canvas.renderer)
