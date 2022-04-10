from statistics import geometric_mean, mean, quantiles, stdev
from PyQt5.QtWidgets import QPushButton
from plots.base import Base_app
from numpy import arange


class Histo_app(Base_app):
    """Pie app that shows a pie chart of all the datas provided.
        The datas on the pie is for datas that aren't numbers.

        #####################################################
        #           #                                       #
        #           #                                       #
        #           #                                       #
        #           #                                       #
        #           #               Histo                   #
        #   DATA    #               CHART                   #
        #   LIST    #                                       #
        #           #                                       #
        #           #                                       #
        #           #                                       #
        #           #                                       #
        #           #########################################
        #           #               FILTERS          #Gran +#
        #           #               BUTTONS          #Gran -#
        #####################################################
        """
    def plot_inter_widgets(self):

        self.keys = []  # Look if I need self
        for x, value in self.data[0].items():
            if isinstance(value, (int, float)):
                self.keys.append(x)

        buttons = []
        for x in self.keys:
            dropbox = QPushButton(x)
            dropbox.clicked.connect(lambda checked, a=x : self.update_plot(number=a))
            buttons.append(dropbox)
        return buttons

    def update_plot(self, **kargs):
        def trim_data(to_trim):
            # IQR vs. Geometric???
            quantilles = quantiles(to_trim)
            IQ1 = quantilles[0]
            IQ3 = quantilles[2]
            IQR = IQ3 - IQ1
            trimmed =  [x for x in to_trim if IQ1 - IQR < x < (IQ3 + IQR)]
            if len(trimmed) != len(to_trim):
                trimmed = trim_data(trimmed)
            return trimmed


        def labels():
            self.ax.set_title(f'{self.data[0].__class__.__name__} - {"time"}')
            self.ax.set_xlabel(kargs["number"])
            self.ax.set_ylabel("Frequency")

        def set_xticks():
            if len(set(to_plot)) == 1:
                return

            self.ax.set_xticks(arange(
                                        min(to_plot),
                                        max(to_plot),
                                        (max(to_plot)-min(to_plot))/5
                                        )[1:])
            self.ax.set_xlim([min(to_plot), max(to_plot)])

            if kargs["number"] in ["time", "delta WR", "WR time"]:
                time_str = lambda x : f'{int(x//3600):>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
                self.ax.set_xticklabels([time_str(float(x)) for x in self.ax.get_xticks()], horizontalalignment="center")

            elif kargs["number"] in ["WR %", "LB %"]:
                perc_str = lambda x : f'{x:.1%}'
                self.ax.set_xticklabels([perc_str(float(x)) for x in self.ax.get_xticks()], horizontalalignment="center")
            elif kargs["number"] in ["place"]:
                self.ax.set_xticklabels([int(x) for x in self.ax.get_xticks()], horizontalalignment="center")
            else:
                raise KeyError(f'{kargs["number"]} is not assigned.')  # pragma: no cover
            self.canvas.draw()

        def set_yticks():
            self.ax.set_yticks([x for x in range(0, int(max(self.ax.get_yticks()) + 1), int(max(self.ax.get_yticks()) + 1) // 14 + 1)][1:])
            self.canvas.draw()

        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()


        to_plot = [x[kargs["number"]] for x in self.data]
        if len(set(to_plot)) > 1:
            to_plot = trim_data([x[kargs["number"]] for x in self.data])

        self.ax.hist(to_plot, range=(min(to_plot), max(to_plot)))
        labels()
        set_xticks()
        set_yticks()
