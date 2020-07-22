import csv
from bokeh.plotting import figure, output_file, show, Figure
from typing import List, Tuple


class BloodPressureReading(object):
    def __init__(self, raw_str: str):
        self.systole, self.diastole, self.hr = raw_str.split('/')


class BloodPressureDataManager(object):
    def __init__(self):
        self.hands_curled_list, self.hands_straight_list = self.parse_data()

    @classmethod
    def parse_data(cls) -> Tuple[List[BloodPressureReading], List[BloodPressureReading]]:
        with open('blood-pressure.csv', newline='') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')
            next(reader)
            hands_curled_data, hands_straight_data = [], []
            for row in reader:
                row = row[0]
                row = row.split(',')
                hands_curled_data.append(cls.convert_raw_blood_pressure_data_into_struct(row[1:4]))
                hands_straight_data.append(row[4:])
            return hands_curled_data, hands_straight_data

    @classmethod
    def convert_raw_blood_pressure_data_into_struct(cls, data: List[str]) -> List[BloodPressureReading]:
        pass

    def get_wrist_avgs(self, drop_highest_systole=False, drop_highest_diastole=False):
        pass

    def get_hands_straight_avgs(self, drop_highest_systole=False, drop_highest_diastole=False):
        pass

    def get_heart_rate_avgs(self):
        pass

    def create_range_plots(self):
        pass

    def create_basic_line_graph(self) -> Figure:
        p = figure(plot_width=800, plot_height=400)
        p.multi_line([x_line, x_line, x_line, x_line], [wrist_sys, wrist_dia, hand_sys, hand_dia],
                     color=["firebrick", "navy", 'orange', 'green'], alpha=[0.8, 0.3, 0.8, 0.3], line_width=4)

        return p



if __name__ == '__main__':
    manager = BloodPressureDataManager()
    graph = manager.create_basic_line_graph()
    # output_file("patch.html")
    show(graph)
