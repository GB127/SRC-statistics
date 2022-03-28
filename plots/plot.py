from PyQt5.QtWidgets import QLineEdit, QPushButton
from plots.base import Base_app

class Plot_app(Base_app):
    def __init__(self, data_list):
        self.threshold = QLineEdit()
        self.threshold.setText("300")
        super().__init__(data_list)

        self.layout.addWidget(self.threshold,1,1)
        self.button = QPushButton("Update")
        self.button.clicked.connect(self.update_plot)
        self.layout.addWidget(self.button, 1,2)

    def list_clicked(self):
        self.update_plot(list=self.listwidget.currentRow())

    def update_plot(self, **kargs):
        new_id = kargs["list"]
        def data_f():
            data = [x["time"] for x in self.data[new_id]["leaderboard"]]
            adjusted = [x for x in data if 100*x/min(data) <= float(self.threshold.text())]
            return adjusted

        def prep():
            self.canvas.figure.clf()
            self.ax = self.canvas.figure.subplots()
            self.ax.plot(data_f())
            self.ax.invert_xaxis()
            self.ax.set_title(f'{self.data[new_id]["game"]}\n{self.data[new_id]["category"]}')


        def data_plot():
            # Moyenne
            self.ax.axhline(sum(data_f()) / len(data_f()),linestyle="--", color="darkblue", label="Mean")
            # WR
            self.ax.axhline(min(data_f()),linestyle="--",label="WR", color="gold")
            self.ax.plot(0, min(data_f()),"o", color="gold")
            # Médiane
            self.ax.axvline(len(data_f())//2,linestyle="--", color="green", label="Median")
            # PB
            if self.data[new_id]["WR %"] * 100 <= float(self.threshold.text()):
                self.ax.plot(self.data[new_id]["place"] -1, self.data[new_id]["time"], "o", color="red", label="PB")
            self.ax.legend()

        def y_axis():
            time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{x % 3600 % 60 % 60:02}'
            self.canvas.draw()
            self.ax.set_yticks(self.ax.get_yticks())  # Noise code to remove a warning from matplotlib
            self.ax.set_yticklabels([time_str(float(x.get_text().replace("−", "-"))) for x in self.ax.get_yticklabels()])
            self.ax.set_ybound(lower=0.9 * min(data_f()), upper=1.02 * max(data_f()))
            self.canvas.draw()

        prep()
        data_plot()
        y_axis()


if __name__ == "__main__":
    from handler import window_handler, Mockery

    data = [Mockery(x) for x in range(20)]
    window_handler(data, Plot_app, debug=False)