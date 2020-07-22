import csv
from bokeh.models import Range1d
from bokeh.plotting import figure, show, Figure
from typing import List, Tuple

class BloodPressureReading(object):
    def __init__(self, raw_data: str):
        self.systole, self.diastole, self.hr = map(int, raw_data.split('/'))

    def __repr__(self):
        string = "{0}/{1}/{2}".format(self.systole, self.diastole, self.hr)
        return string

class BloodPressureDataPoint(object):
    def __init__(self, input_data: List[str]):
        self.readings = tuple([BloodPressureReading(i) for i in input_data])

    def __repr__(self):
        return " ".join([reading.__str__() for reading in self.readings])

    def get_avgs(self, drop_highest_systole: bool, drop_highest_diastole: bool, drop_highest_hr: bool):
        systoles, diastoles, heart_rates = [], [], []
        for reading in self.readings:
            systoles.append(reading.systole)
            diastoles.append(reading.diastole)
            heart_rates.append(reading.hr)
        if  drop_highest_systole:
            systoles.remove(max(systoles))
        if drop_highest_diastole:
            diastoles.remove(max(diastoles))
        if drop_highest_hr:
            heart_rates.remove(max(heart_rates))

        systole_avg = sum(systoles)/len(systoles)
        diastole_avg = sum(diastoles)/len(diastoles)
        hr_avg = sum(heart_rates)/len(heart_rates)
        return systole_avg, diastole_avg, hr_avg


class BloodPressureDataManager(object):
    def __init__(self):
        self.hands_curled_list, self.hands_straight_list = self.parse_data()
        print('')

    @classmethod
    def parse_data(cls) -> Tuple[List[BloodPressureDataPoint], List[BloodPressureDataPoint]]:
        with open('blood-pressure.csv', newline='') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')
            next(reader)
            hands_curled_data, hands_straight_data = [], []
            for row in reader:
                row = row[0]
                row = row.split(',')
                hands_curled_data.append(BloodPressureDataPoint(row[1:4]))
                hands_straight_data.append(BloodPressureDataPoint(row[4:]))
            return hands_curled_data, hands_straight_data

    def get_avgs(self, array: List[BloodPressureDataPoint]):
        sys_array, diastole_array, hr_array = [], [], []
        for data in array:
            systole, diastole, hr = data.get_avgs(False, False, False)
            sys_array.append(systole)
            diastole_array.append(diastole)
            hr_array.append(hr)
        return sys_array, diastole_array, hr_array

    def get_hands_curled_avgs(self):
        return self.get_avgs(self.hands_curled_list)

    def get_hands_straight_avgs(self):
        return self.get_avgs(self.hands_straight_list)

    def create_basic_line_graph(self) -> Figure:
        x_line = list(range(len(self.hands_curled_list)))
        a, b, c = self.get_hands_curled_avgs()
        d, e, f = self.get_hands_straight_avgs()
        p = figure(plot_width=800, plot_height=400)
        p.y_range = Range1d(65, 145)
        p.multi_line([x_line, x_line, x_line, x_line], [a, b, d, e],
                     color=["firebrick", "navy", 'orange', 'green'], alpha=[0.8, 0.3, 0.8, 0.3], line_width=4)

        return p



if __name__ == '__main__':
    manager = BloodPressureDataManager()
    graph = manager.create_basic_line_graph()
    show(graph)
